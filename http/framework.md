---
name: http-framework
description: HTTP 测试配方（repeater/intruder/spider/rules/scope）
when_to_use: 需要重放、改包、爆破参数、爬站
---
# HTTP 测试框架（Burp 替代，纯 shell）

## Repeater
```bash
U='https://target/api/x?id=1'
curl -sSk -D $RUN/raw/repeater.hdr -o $RUN/raw/repeater.body \
  -w 'status=%{http_code} size=%{size_download} time=%{time_total}s\n' \
  -X GET "$U" -H 'X-Test: 1'
head -20 $RUN/raw/repeater.hdr
```

## 响应漏洞分析
```bash
# 安全头
for h in X-Frame-Options X-Content-Type-Options X-XSS-Protection Strict-Transport-Security Content-Security-Policy; do
  grep -qi "^$h:" $RUN/raw/repeater.hdr || { echo "MISSING $h"; add_finding medium missing_security_header "$h missing" "$U" curl ""; }
done
# 敏感信息
grep -oiE '(password|api[_-]?key|secret|token)[[:space:]]*[:=][[:space:]]*["'"'"']?[^"'"'"'[:space:]]+' $RUN/raw/repeater.body | head -5
# SQL 错误
grep -oiE 'SQL syntax error|mysql_fetch_array|ORA-01756|Microsoft OLE DB Provider|PostgreSQL query failed' $RUN/raw/repeater.body
```

## Intruder（Sniper：逐 payload 替换单参数）
```bash
U='https://target/api?uid=1'; PARAM=uid
base_sz=$(curl -sSk -o /dev/null -w '%{size_download}' "$U")
base_code=$(curl -sSk -o /dev/null -w '%{http_code}' "$U")
while IFS= read -r p; do
  sz=$(curl -sSk -o $RUN/raw/intruder.body -w '%{size_download}' --get --data-urlencode "$PARAM=$p" "$U")
  code=$(curl -sSk -o /dev/null -w '%{http_code}' --get --data-urlencode "$PARAM=$p" "$U")
  d=$((sz-base_sz)); ad=${d#-}
  if [ "$code" != "$base_code" ] || [ "$ad" -gt 150 ] || grep -qF -- "$p" $RUN/raw/intruder.body; then
    echo "HIT code=$code delta=$d payload=$p"
    add_finding high http_intruder_anomaly "param $PARAM reacted to [$p]" "$U" curl "code=$code delta=$d"
  fi
done <<'P'
<hexstrikeXSSTest123>
' OR 1=1--
1' AND SLEEP(5)-- -
../../../../etc/passwd
P
```
判定阈值：状态码变化 / 长度差 >150B / payload 回显，三者任一即"值得关注"。

## Spider（有 katana 优先，否则 curl+grep）
```bash
U='https://target/'
if command -v katana >/dev/null; then
  katana -u "$U" -d 3 -jc -silent -o $RUN/parsed/urls.txt
else
  curl -sSk "$U" | grep -oE 'href="[^"]+"' | cut -d'"' -f2 | sort -u > $RUN/parsed/urls.txt
  curl -sSk "$U" | grep -oE 'action="[^"]+"' | cut -d'"' -f2 | sort -u >> $RUN/parsed/urls.txt
fi
sort -u $RUN/parsed/urls.txt -o $RUN/parsed/urls.txt; wc -l $RUN/parsed/urls.txt
```

## Match/Replace 规则（发请求前套用，需 `source "$SKILLS/scripts/hx.sh"`）
```bash
U2=$(rule "$U" 's/uid=[0-9]+/uid=1/')     # rule <input> <sed-expr>
# 批量规则：写进变量，重放前统一应用
```

## Scope 校验（越界直接拒绝）
```bash
SCOPE='target.com'
in_scope "$U" && curl -sSk "$U" || echo "out of scope: $U"
```

## 历史（自己维护即可）
```bash
echo "$(date -u +%FT%TZ) GET $U $(awk '/^HTTP/{print $2}' $RUN/raw/repeater.hdr | head -1)" >> $RUN/parsed/http_history.tsv
```

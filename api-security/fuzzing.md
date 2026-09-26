---
name: api-fuzzing
description: API 端点模糊测试配方（端点发现 + 多方法测试）
when_to_use: 目标是 API 或发现 /api/ 路径
---
# API 端点模糊测试

## 已知端点：逐方法测试
```bash
BASE='https://api.target.com'
for ep in v1/users v1/login v1/admin graphql; do
  for m in GET POST PUT DELETE; do
    out=$(curl -sSk -o /dev/null -w '%{http_code}|%{size_download}' -X $m "$BASE/${ep#/}")
    printf '%-6s %-20s %s\n' "$m" "$ep" "$out"
    case "$out" in
      2*|3*) [ "$m" = PUT ] || [ "$m" = DELETE ] && \
        add_finding high api_dangerous_method "$m $ep allowed" "$BASE" curl "$out" ;;
    esac
  done
done | tee $RUN/raw/api_methods.txt
```

## 未知端点：ffuf（判定码 200/201/202/204/301/302/307/401/403/405）
```bash
WL=/usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt
[ -f "$WL" ] || WL=/usr/share/seclists/Discovery/Web-Content/common.txt
[ -f "$WL" ] || WL=/usr/share/wordlists/dirb/common.txt
ffuf -u "$BASE/FUZZ" -w "$WL" -mc 200,201,202,204,301,302,307,401,403,405 \
     -t 50 -of json -o $RUN/parsed/ffuf_api.json -s
jq -r '.results[] | [.status, (.length|tostring), .url] | @tsv' $RUN/parsed/ffuf_api.json
```

## 无 ffuf 时的 bash 兜底
```bash
for w in users login admin health status config swagger openapi graphql v1 v2; do
  code=$(curl -sSk -o /dev/null -w '%{http_code}' "$BASE/$w")
  case $code in 200|201|204|301|302|307|401|403|405) echo "$code /$w";; esac
done
```
后续：参数发现 `tools/arjun.md`、`tools/x8.md`；新端点回填 `parsed/`。

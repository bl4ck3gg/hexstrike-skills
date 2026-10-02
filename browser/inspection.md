---
name: browser-inspection
description: 浏览器检查（chromium 单命令优先；深度 JS 状态给可粘贴片段）
when_to_use: 需要 JS 渲染后的页面分析
---
# 浏览器检查（不需要预置脚本，不需要 CDP）

## 能力阶梯（按需要选，优先用第一条）
| 需求 | 做法 | 依赖 |
|---|---|---|
| 渲染后 DOM / 链接 / 表单 / 内联 JS | `chromium --headless --dump-dom` | 系统 chromium |
| 截图 | `chromium --headless --screenshot` | 同上 |
| JS 爬虫（补全路由） | `katana -headless` | katana |
| localStorage/sessionStorage/console/network | 现场写 ~15 行 playwright 片段 | pip playwright |
| 极致控制（拦截改包） | CDP over websocket | 没必要，跳过 |

**CDP 不是必需的**：`--dump-dom` 能覆盖大部分"JS 渲染检查"；
只有需要读 storage/console/network 时才值得上 playwright 片段。

## 1) 纯 CLI（零代码）
```bash
U='https://target/'
chromium --headless --no-sandbox --disable-gpu --virtual-time-budget=5000 \
  --dump-dom "$U" > $RUN/artifacts/dom.html 2>/dev/null \
  || google-chrome --headless --no-sandbox --disable-gpu --virtual-time-budget=5000 --dump-dom "$U" > $RUN/artifacts/dom.html
chromium --headless --no-sandbox --disable-gpu --screenshot="$RUN/artifacts/page.png" \
  --window-size=1920,1080 "$U" 2>/dev/null
# 有 katana 时顺带 JS 爬
command -v katana >/dev/null && katana -u "$U" -headless -d 2 -jc -silent -o $RUN/parsed/rendered_urls.txt
```

## 2) 从 DOM 做安全检查
```bash
D=$RUN/artifacts/dom.html
# 表单：POST 且无 csrf/token 字段 -> medium
grep -oiE '<form[^>]*>' "$D" | while read -r f; do
  echo "$f" | grep -qi 'method="\?post' && ! grep -qiE 'csrf|token' <<< "$(sed -n "/${f//\//\\/}/,/<\/form>/p" "$D")" \
    && echo "POST form without CSRF: $f"
done
# 内联 script 数量 -> low
echo "inline scripts: $(grep -c '<script[^>]*>' "$D")"
# 外链脚本（无 SRI 提示）
grep -oE '<script[^>]+src="[^"]+"' "$D" | head
```
安全头 / cookie 标志来自 HTTP 响应：
```bash
curl -sSk -D $RUN/raw/headers.txt -o /dev/null "$U"
for h in X-Frame-Options X-Content-Type-Options X-XSS-Protection Strict-Transport-Security Content-Security-Policy; do
  grep -qi "^$h:" $RUN/raw/headers.txt || add_finding medium missing_security_header "$h missing" "$U" curl ""
done
grep -oiE '^set-cookie:.*' $RUN/raw/headers.txt   # 看 Secure/HttpOnly/SameSite
```

## 3) 需要 storage/console/network 时：用 scripts/playwright_probe.py
```bash
python3 "$SKILLS/scripts/playwright_probe.py" '<url>' $RUN/artifacts/page.png --json-out $RUN/parsed/browser.json
```
输出含 `local_storage` / `session_storage` / `console` / `network` / `forms`，
并附 `assessment.issues` 与 `security_score`。安装：
`pip3 install --break-system-packages playwright && python3 -m playwright install chromium`。
（不装 playwright 时 `--help` 仍可用；其他文档仍可零依赖运行。）

判定（脚本已内置，人工复核用）：
```
storage key 含 password/token/secret/key -> high
POST 表单无 csrf/token -> medium
内联 JS 数量 -> low
security_score = max(0, 100 - issues*5)
```

## 4) 反射 XSS 主动测试（GET 表单，最多 5 个，保守）
```bash
P='<hexstrikeXSSTest123>'
grep -oiE '<form[^>]*method="\?get"[^>]*>' "$D" | head -5 | while read -r f; do
  act=$(echo "$f" | grep -oE 'action="[^"]+"' | cut -d'"' -f2)
  qs=$(grep -oE '<input[^>]+name="[^"]+"' <<< "$(sed -n "/${f//\//\\/}/,/<\/form>/p" "$D")" \
       | grep -oE 'name="[^"]+"' | cut -d'"' -f2 | head -3 | sed "s/$/=$P/" | paste -sd'&')
  [ -n "$qs" ] || continue
  curl -sSk "${act:-$U}?$qs" | grep -qF "$P" && echo "reflected XSS: ${act:-$U}?$qs"
done
```

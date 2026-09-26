---
name: burpsuite-alternative
category: 综合 Web
description: HTTP 测试 + 浏览器检查的组合评估
when_to_use: 需要完整 Web 手工测试面
---
组合两项能力：
```bash
# 1) 浏览器侧：渲染后 DOM / 表单 / 安全头 / 反射 XSS
chromium --headless --dump-dom '<url>' > dom.html
curl -sSk -D hdr.txt -o /dev/null '<url>'
# 2) HTTP 侧：爬站 / 改包 / 参数爆破
katana -u '<url>' -d 3 -jc -o urls.txt
curl -sSk -D hdr.txt -o body.html '<url>'
base=$(curl -sSk -o /dev/null -w '%{size_download}' '<url>')
for p in "<hexstrikeXSSTest123>" "' OR 1=1--"; do
  sz=$(curl -sSk -o b -w '%{size_download}' --get --data-urlencode "id=$p" '<url>'); echo "delta=$((sz-base)) $p"
done
```
工作流见 `workflows/http-testing.md`。
有 Burp Professional 许可时走真 Burp：`tools/burpsuite.md`（headless/REST）。

---
name: http-framework
category: 综合 Web
description: Burp 替代（repeater / intruder / spider / rules / scope）
when_to_use: 需要手工改包与参数爆破
---
**配方**: `http/framework.md`

```bash
# repeater
curl -sSk -D hdr.txt -o body.html -w 'status=%{http_code} size=%{size_download}\n' '<url>'
# intruder（Sniper）
base=$(curl -sSk -o /dev/null -w '%{size_download}' '<url>'); p='<payload>'
sz=$(curl -sSk -o b -w '%{size_download}' --get --data-urlencode "param=$p" '<url>')
echo "delta=$((sz-base))"
# spider
katana -u '<url>' -d 3 -jc -o urls.txt || curl -sSk '<url>' | grep -oE 'href="[^"]+"' | cut -d'"' -f2 | sort -u
```

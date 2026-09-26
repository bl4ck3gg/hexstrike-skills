---
name: http-testing
when_to_use: Burp 式手工测试（替代 burpsuite_alternative / http_framework_test）
---
# HTTP 手工测试编排

| # | 步骤 | 配方 |
|---|---|---|
| 1 | 设 scope | `http/framework.md` 的 in_scope 函数 |
| 2 | 爬站 | katana / curl+grep 列 URL |
| 3 | 基线 | curl 取 headers + body，存 raw/ |
| 4 | 规则 | 重放前用 sed 改写参数 |
| 5 | 爆破 | intruder 循环（阈值：状态码变 / 长度差>150B / payload 回显） |
| 6 | 浏览器 | chromium --dump-dom + 安全检查 |
| 7 | 汇总 | reporting/deliverables.md |

## 判定口径
- intruder：状态码变化 / 长度差 >150B / payload 回显 —— 任一即"值得关注"
- repeater：自动跑安全头、敏感信息、SQL 错误三类检查
- browser：安全头、cookie 标志、混合内容、CSRF、反射 XSS

## 与 API 分支的衔接
先按 `api-security/schema-analysis.md` 找到 schema/graphql，
再回到本流程做端点级手工测试。

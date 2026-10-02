---
name: error-classifier
description: 错误分类正则表
when_to_use: 工具失败后第一步
---
# 错误分类（按表内顺序，首个命中即返回）

> 顺序陷阱：`TARGET_UNREACHABLE` 必须排在 `TOOL_NOT_FOUND` **之前**，
> 否则 `host not found` 会被 `not found` 抢先匹配成 TOOL_NOT_FOUND。
> 可执行版：`scripts/hx.sh` 的 `classify()`（唯一真相源）。

| ErrorType | 正则 |
|---|---|
| TIMEOUT | `timeout\|timed out\|connection timeout\|read timeout` |
| TIMEOUT | `operation timed out\|command timeout` |
| PERMISSION_DENIED | `permission denied\|access denied\|forbidden\|not authorized` |
| PERMISSION_DENIED | `sudo required\|root required\|insufficient privileges` |
| NETWORK_UNREACHABLE | `network unreachable\|host unreachable\|no route to host` |
| NETWORK_UNREACHABLE | `connection refused\|connection reset\|network error` |
| RATE_LIMITED | `rate limit\|too many requests\|throttled\|429` |
| RATE_LIMITED | `request limit exceeded\|quota exceeded` |
| **TARGET_UNREACHABLE** | `target unreachable\|target not responding\|target down` |
| **TARGET_UNREACHABLE** | `host not found\|dns resolution failed\|name or service not known` |
| TOOL_NOT_FOUND | `command not found\|executable not found\|binary not found` |
| TOOL_NOT_FOUND | `no such file or directory\|not found` |
| INVALID_PARAMETERS | `invalid argument\|invalid option\|unknown option` |
| INVALID_PARAMETERS | `bad parameter\|invalid parameter\|syntax error` |
| RESOURCE_EXHAUSTED | `out of memory\|memory error\|disk full\|no space left` |
| RESOURCE_EXHAUSTED | `resource temporarily unavailable\|too many open files` |
| AUTHENTICATION_FAILED | `authentication failed\|login failed\|invalid credentials` |
| AUTHENTICATION_FAILED | `unauthorized\|invalid token\|expired token` |
| PARSING_ERROR | `parse error\|parsing failed\|invalid format\|malformed` |
| PARSING_ERROR | `json decode error\|xml parse error\|invalid json` |
| UNKNOWN | 兜底 |

## 用法
```bash
source "$SKILLS/scripts/hx.sh"   # 引入 classify()
err=$(sed -n '/--- stderr ---/,$p' $RUN/raw/<x>.log); t=$(classify "$err"); echo "$t"
```
`exit=124` 一律 TIMEOUT。

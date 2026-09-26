---
name: error-classifier
description: 错误分类正则表
when_to_use: 工具失败后第一步
---
# 错误分类（按表内顺序，首个命中即返回）

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
| TOOL_NOT_FOUND | `command not found\|no such file or directory\|not found` |
| TOOL_NOT_FOUND | `executable not found\|binary not found` |
| INVALID_PARAMETERS | `invalid argument\|invalid option\|unknown option` |
| INVALID_PARAMETERS | `bad parameter\|invalid parameter\|syntax error` |
| RESOURCE_EXHAUSTED | `out of memory\|memory error\|disk full\|no space left` |
| RESOURCE_EXHAUSTED | `resource temporarily unavailable\|too many open files` |
| AUTHENTICATION_FAILED | `authentication failed\|login failed\|invalid credentials` |
| AUTHENTICATION_FAILED | `unauthorized\|invalid token\|expired token` |
| TARGET_UNREACHABLE | `target unreachable\|target not responding\|target down` |
| TARGET_UNREACHABLE | `host not found\|dns resolution failed` |
| PARSING_ERROR | `parse error\|parsing failed\|invalid format\|malformed` |
| PARSING_ERROR | `json decode error\|xml parse error\|invalid json` |
| UNKNOWN | 兜底 |

## 纯 shell 分类
```bash
classify() {  # $1 = stderr + exit code 文本
  case "$1" in
    *timeout*|*"timed out"*|*"exit=124"*)                 echo TIMEOUT;;
    *"permission denied"*|*"access denied"*|*forbidden*) echo PERMISSION_DENIED;;
    *"no route to host"*|*"connection refused"*)          echo NETWORK_UNREACHABLE;;
    *"rate limit"*|*"too many requests"*|*429*)           echo RATE_LIMITED;;
    *"command not found"*|*"not found"*)                  echo TOOL_NOT_FOUND;;
    *"invalid option"*|*"invalid argument"*)              echo INVALID_PARAMETERS;;
    *"no space left"*|*"out of memory"*)                  echo RESOURCE_EXHAUSTED;;
    *"authentication failed"*|*unauthorized*)             echo AUTHENTICATION_FAILED;;
    *"host not found"*|*"target unreachable"*)            echo TARGET_UNREACHABLE;;
    *"parse error"*|*"invalid json"*|*malformed*)         echo PARSING_ERROR;;
    *)                                                    echo UNKNOWN;;
  esac
}
# 用法
err=$(cat $RUN/raw/<x>.log | sed -n '/--- stderr ---/,$p'); t=$(classify "$err"); echo "$t"
```
`exit=124` 一律 TIMEOUT。

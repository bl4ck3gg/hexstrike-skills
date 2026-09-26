---
name: error-patterns
when_to_use: 判断错误类型
---
# 错误分类
timeout|timed out|connection timeout → TIMEOUT
permission denied|access denied|forbidden → PERMISSION_DENIED
network unreachable|host unreachable|no route → NETWORK_UNREACHABLE
connection refused|connection reset → NETWORK_UNREACHABLE
rate limit|too many requests|429 → RATE_LIMITED
command not found|no such file → TOOL_NOT_FOUND
invalid argument|unknown option → INVALID_PARAMETERS
out of memory|disk full|no space → RESOURCE_EXHAUSTED
authentication failed|invalid credentials → AUTHENTICATION_FAILED
target unreachable|dns resolution failed → TARGET_UNREACHABLE
parse error|invalid json|malformed → PARSING_ERROR
其他 → UNKNOWN

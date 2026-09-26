---
name: recovery-engine
description: 恢复策略矩阵与最优策略打分
when_to_use: 已知 ErrorType，选下一步动作
---
# 恢复引擎

## 策略矩阵
| ErrorType | action | max_att | backoff | p | t(s) |
|---|---|---|---|---|---|
| TIMEOUT | RETRY_WITH_BACKOFF 5→60 | 3 | 2.0 | 0.7 | 30 |
| TIMEOUT | RETRY_WITH_REDUCED_SCOPE | 2 | 1.0 | 0.8 | 45 |
| TIMEOUT | SWITCH_TO_ALTERNATIVE_TOOL(faster) | 1 | 1.0 | 0.6 | 60 |
| PERMISSION_DENIED | ESCALATE_TO_HUMAN | 1 | 1.0 | 0.9 | 300 |
| PERMISSION_DENIED | SWITCH_TO_ALTERNATIVE_TOOL(no_priv) | 1 | 1.0 | 0.5 | 30 |
| NETWORK_UNREACHABLE | RETRY_WITH_BACKOFF 10→120 | 3 | 2.0 | 0.6 | 60 |
| NETWORK_UNREACHABLE | SWITCH_TO_ALTERNATIVE_TOOL(offline) | 1 | 1.0 | 0.4 | 30 |
| RATE_LIMITED | RETRY_WITH_BACKOFF 30→300 | 5 | 1.5 | 0.9 | 180 |
| RATE_LIMITED | ADJUST_PARAMETERS(reduce_rate) | 2 | 1.0 | 0.8 | 120 |
| TOOL_NOT_FOUND | SWITCH_TO_ALTERNATIVE_TOOL | 1 | 1.0 | 0.7 | 15 |
| TOOL_NOT_FOUND | ESCALATE_TO_HUMAN | 1 | 1.0 | 0.9 | 600 |
| INVALID_PARAMETERS | ADJUST_PARAMETERS(defaults) | 3 | 1.0 | 0.8 | 10 |
| INVALID_PARAMETERS | SWITCH_TO_ALTERNATIVE_TOOL(simpler) | 1 | 1.0 | 0.6 | 30 |
| RESOURCE_EXHAUSTED | RETRY_WITH_REDUCED_SCOPE | 2 | 1.0 | 0.7 | 60 |
| RESOURCE_EXHAUSTED | RETRY_WITH_BACKOFF 60→300 | 2 | 2.0 | 0.5 | 180 |
| AUTHENTICATION_FAILED | ESCALATE_TO_HUMAN(high) | 1 | 1.0 | 0.9 | 300 |
| AUTHENTICATION_FAILED | SWITCH_TO_ALTERNATIVE_TOOL(no_auth) | 1 | 1.0 | 0.4 | 30 |
| TARGET_UNREACHABLE | RETRY_WITH_BACKOFF 15→180 | 3 | 2.0 | 0.6 | 90 |
| TARGET_UNREACHABLE | GRACEFUL_DEGRADATION(skip) | 1 | 1.0 | 1.0 | 5 |
| PARSING_ERROR | ADJUST_PARAMETERS(output) | 2 | 1.0 | 0.7 | 20 |
| PARSING_ERROR | SWITCH_TO_ALTERNATIVE_TOOL | 1 | 1.0 | 0.6 | 30 |
| UNKNOWN | RETRY_WITH_BACKOFF 5→30 | 2 | 2.0 | 0.3 | 45 |
| UNKNOWN | ESCALATE_TO_HUMAN | 1 | 1.0 | 0.9 | 300 |

## 选择算法
```
viable = 策略中 attempt_count <= max_attempts 的
若为空 -> ESCALATE_TO_HUMAN(urgency=high)
否则  adjusted = p * 0.9^(attempt_count-1)
      score    = adjusted - t/1000
      取 score 最大者
```
`attempt_count` 从 1 开始，同类失败每次 +1；记在 `parsed/recovery_state.tsv`
（`tool \t error_type \t attempt \t actions`）。

## 动作落地
| action | 怎么做 |
|---|---|
| RETRY_WITH_BACKOFF | `sleep $((init * mult**(n-1)))`（封顶 max_delay）后重跑；`RETRY_WITH_BACKOFF 30→300` 即 init=30 max=300 |
| RETRY_WITH_REDUCED_SCOPE | 查 `recovery/parameter-adjustments.md`，降 `-t` / 缩端口范围 |
| SWITCH_TO_ALTERNATIVE_TOOL | 查 `recovery/tool-alternatives.md`，先 `command -v` 验证 |
| ADJUST_PARAMETERS | `optimization/parameter-optimizer.md` + `recovery/parameter-adjustments.md` |
| ESCALATE_TO_HUMAN | 通知用户上报：工具/目标/错误/尝试次数/建议 |
| GRACEFUL_DEGRADATION | `recovery/degradation.md` |
| ABORT_OPERATION | 记 raw/ 后跳过该分支 |

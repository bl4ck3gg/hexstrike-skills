---
name: agent-error-handler
description: 错误处理编排（表见 recovery/*）
when_to_use: 任何工具失败
---
# 错误处理器

任何工具失败后的统一处理流程。

## 流程
```
1. 收集证据
   err=$(sed -n '/--- stderr ---/,$p' raw/<x>.log); code=$(grep -o 'exit=[0-9]*' raw/<x>.log)
2. classify_error("$code $err")        -> recovery/error-classifier.md
3. 取该 ErrorType 的策略列表            -> recovery/recovery-engine.md 矩阵
4. attempt_count 过滤 + 打分选最优      -> recovery/recovery-engine.md 选择算法
5. 执行动作
   RETRY_WITH_BACKOFF       -> sleep 后重跑（记录 attempt_count）
   RETRY_WITH_REDUCED_SCOPE -> recovery/parameter-adjustments.md
   SWITCH_TO_ALTERNATIVE_TOOL -> recovery/tool-alternatives.md（先 command -v 验证）
   ADJUST_PARAMETERS        -> optimization/parameter-optimizer.md
   ESCALATE_TO_HUMAN        -> 通知用户：工具/目标/错误/尝试次数/建议
   GRACEFUL_DEGRADATION     -> recovery/degradation.md
   ABORT_OPERATION          -> 记 raw/ 后跳过
6. 全部策略耗尽 -> 上报（urgency=high）
```

## 状态维护
`parsed/recovery_state.tsv`：`tool \t error_type \t attempt \t actions`
```bash
echo -e "$TOOL\t$ETYPE\t$N\t$ACTION" >> $RUN/parsed/recovery_state.tsv
```
跨步骤可续，落盘后可随时回看历史失败与已尝试动作。

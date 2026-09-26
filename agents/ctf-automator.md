---
name: agent-ctf-automator
description: CTF 自动化解题编排（策略见 ctf/*）
when_to_use: CTF 挑战
---
# CTF 自动化

单人与团队两种模式的解题编排。

## 单人流程
```
1. 分类: 从题面/附件判断 web|crypto|pwn|forensics|rev|osint|misc
2. 取策略: ctf/<category>.md 的步骤表（含并行标记与预计耗时）
3. 并行执行: ctf/parallel-tasks.md 的分组
4. flag 提取（正则）:
   flag\{[^}]+\} | FLAG\{[^}]+\} | ctf\{[^}]+\} | CTF\{[^}]+\} | [a-zA-Z0-9_]+\{[^}]+\}
   [0-9a-f]{32} (MD5) | [0-9a-f]{40} (SHA1) | [0-9a-f]{64} (SHA256)
5. 验证: ctf/validation.md 的分类校验步骤
6. 卡住: ctf/<category>.md 的"回退"小节
```
```bash
grep -rhoE '(flag|FLAG|ctf|CTF)\{[^}]+\}|[a-zA-Z0-9_]+\{[^}]+\}|[0-9a-f]{32}|[0-9a-f]{40}|[0-9a-f]{64}' \
  $RUN/raw/ $RUN/artifacts/ 2>/dev/null | sort -u
```

## 团队分工 `optimize_team_strategy`
```
1. 建 skill_matrix: member × skill
2. 每 member × 每 challenge 打分:
   技能匹配 ×1.5；难度系数 easy 1.0 / medium 0.9 / hard 0.7 / insane 0.5
3. 贪心分配（分高者得）
4. 协作识别: hard/insane 且多人具备同一技能 -> 组队
5. solve_time 估算: 基准 × 难度倍数
```
难度倍数：easy 1.0 / medium 1.2 / hard 1.5 / insane 2.0 / unknown 1.3。
资源估算见 `ctf/validation.md` 末尾。

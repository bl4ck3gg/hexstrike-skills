---
name: hexstrike-ai
description: HexStrike AI 技能包 — 渗透测试/漏洞赏金/CTF/红队全工具命令与流程
---
# HexStrike AI 技能包

一套自成体系的攻防技能包：从目标判断、工具选择、参数决策，到漏洞验证、
情报利用与报告交付，全部以可直接执行的命令与判定规则给出。
命令块可直接粘贴运行，不需要先落成脚本文件。

## 渐进式加载
1. `basics/conventions.md` — 记录约定（运行目录、findings、结果落盘）（**先读**）
2. `basics/environment.md` — 工具探测与依赖
3. `intelligence/target-types.md` → 判断目标类型
4. `intelligence/scoring-algorithms.md` → 打分/选工具/调参
5. `intelligence/attack-patterns.md` → 选剧本
6. `workflows/<pattern>.md` → 工具顺序与参数
7. `tools/<tool>.md` → 单工具命令行；`api-security/` `http/` `browser/` → 无 CLI 等价物的配方
8. 失败 → `recovery/*`；调优 → `optimization/*`
9. 载荷 → `payloads/*`；CTF → `ctf/*`；漏洞赏金 → `bugbounty/*`
10. 情报/报告 → `vuln-intel/*`、`reporting/*`

## 三条使用规则
1. **先定记录位置再干活**：原始输出存 `raw/`，发现记 `findings.tsv` —— 输出丢了也能恢复。
2. **命令直接执行**：文档中的命令块可直接粘贴运行，无需先落成脚本文件。
3. **发现必须落 findings**，报告只读它。

## 约束
- 占位符 `<target>/<url>/<domain>` 必须替换为真实值。
- 只对已授权目标执行。

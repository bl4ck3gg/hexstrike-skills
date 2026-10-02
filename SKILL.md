---
name: hexstrike-ai
description: HexStrike AI 技能包 — 渗透测试/漏洞赏金/CTF/红队全工具命令与流程
---
# HexStrike AI 技能包

一套自成体系的攻防技能包：从目标判断、工具选择、参数决策，到漏洞验证、
情报利用与报告交付，全部以可直接执行的命令与判定规则给出。
命令块可直接粘贴运行；只有跨 shell 存活的函数与超过 20 行的程序放在 `scripts/`。

## 渐进式加载
1. `basics/conventions.md` — 记录约定（运行目录、findings、scripts/ 清单）（**先读**）
2. `basics/environment.md` — 工具探测与依赖 + `source "$SKILLS/scripts/hx.sh"`
3. `intelligence/target-types.md` → 判断目标类型
4. `intelligence/scoring-algorithms.md` → 打分/选工具/调参
5. `intelligence/attack-patterns.md` → 选剧本
6. `workflows/<pattern>.md` → 工具顺序与参数
7. `tools/<tool>.md` → 单工具命令行；`api-security/` `http/` `browser/` → 无 CLI 等价物的配方
8. 失败 → `recovery/*`；调优 → `optimization/*`
9. 载荷 → `payloads/*`；CTF → `ctf/*`（先 `ctf/strategy-matrix.md` 选策略/工具）
10. 情报/报告 → `vuln-intel/*`、`reporting/*`

## 三条使用规则
1. **先定记录位置再干活**：原始输出存 `raw/`，发现记 `findings.tsv` —— 输出丢了也能恢复。
2. **引导块先 source 一次**：`source "$SKILLS/scripts/hx.sh"` 拿到 `add_finding`/`classify`/`in_scope` 等跨 shell 函数；
   其余命令块可直接粘贴运行，不需要先落成脚本文件。
3. **发现必须落 findings**，报告只读它。

## scripts/
只有**跨 shell 存活**或**超过 20 行**的逻辑才放这里，其余保持文档内联。

| 脚本 | 用途 |
|---|---|
| `scripts/hx.sh` | `add_finding` / `dedupe_findings` / `classify` / `rule` / `in_scope` |
| `scripts/report_html.py` | findings.tsv → HTML 报告 |
| `scripts/nmap_xml.py` | nmap XML → JSON/TSV |
| `scripts/json_extract.py` | 从噪声输出里提取 JSON |
| `scripts/playwright_probe.py` | 浏览器 storage/console/network 检查（需 playwright） |
| `scripts/chain_score.py` | 攻击链复合概率与耗时 |

> `add_finding` 等函数**必须 source**：termcp 每次执行基本是独立 shell，
> 不 source 则函数不存在，findings 会丢。

## 约束
- 占位符 `<target>/<url>/<domain>` 必须替换为真实值。
- 只对已授权目标执行。

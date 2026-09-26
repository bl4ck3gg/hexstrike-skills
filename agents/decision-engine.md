---
name: agent-decision-engine
description: 决策引擎编排流程（算法见 intelligence/scoring-algorithms.md）
when_to_use: 需要端到端编排工具链
---
# 决策引擎

端到端编排工具链。**算法细节一律以 `intelligence/scoring-algorithms.md` 为准**，
本文件只定义编排顺序。

## 流程
```
1. 采集事实（写 parsed/）
   - 存活/端口:  tools/nmap.md、tools/rustscan.md      -> parsed/ports.json
   - 技术指纹:   intelligence/tech-fingerprints.md     -> parsed/tech.json
   - 子域:       tools/subfinder.md、tools/amass.md    -> parsed/subdomains.json
2. 目标画像      -> parsed/target_profile.json
   target_type(§1) / technologies / attack_surface_score(§2) / risk_level(§3) / confidence(§4)
3. 选工具(profile, objective) -> parsed/selected_tools.txt   (§5-6)
4. 优化参数(tool, profile)    -> parsed/params_<tool>.txt
   optimization/parameter-optimizer.md
5. 建攻击链(profile, objective) -> parsed/attack_chain.txt   (§7)
6. 逐步执行 workflows/<pattern>.md
   每步: 执行 -> 结果落 parsed/ -> 发现落 findings.tsv -> 失败走 recovery/
7. reporting/deliverables.md 出报告
```

## 两条硬规则
- **objective 决定工具集**：quick=评分前 3；comprehensive=评分>0.7；
  stealth=仅 amass/subfinder/httpx/nuclei（并套 stealth 参数）。
- **WAF 触发强制 stealth**：`parsed/tech.json` 的 security 含
  cloudflare/incapsula/sucuri 时，无论请求什么档位都套 stealth。

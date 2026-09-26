---
name: smart-scan
when_to_use: 一个入口跑完整流程
---
# 智能扫描编排

| # | 阶段 | 依据 | 产物 |
|---|---|---|---|
| 0 | 环境 | basics/environment.md | parsed/toolcheck.txt |
| 1 | 存活+端口 | tools/nmap.md / tools/rustscan.md | parsed/ports.json |
| 2 | 指纹 | intelligence/tech-fingerprints.md | parsed/tech.json |
| 3 | 画像 | intelligence/scoring-algorithms.md §1-4 | parsed/target_profile.json |
| 4 | 选工具 | 同上 §5-6（objective 决定集合） | parsed/selected_tools.txt |
| 5 | 建链 | 同上 §7 | parsed/attack_chain.txt |
| 6 | 执行 | workflows/<pattern>.md，按 basics/long-tasks.md 并发 | raw/ + findings.tsv |
| 7 | 恢复 | agents/error-handler.md | parsed/recovery_state.tsv |
| 8 | 报告 | reporting/deliverables.md | report/ |

## 启动序列
```bash
export TARGET='<target>'
export RUN=/tmp/hexstrike/$TARGET-$(date +%Y%m%d-%H%M%S)
export FINDINGS=$RUN/parsed/findings.tsv
mkdir -p $RUN/{raw,parsed,report,artifacts}
add_finding() { printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" "$5" "$6" >> "$FINDINGS"; }

# 端口（后台）
nohup nmap -sS -sV -T4 --top-ports 1000 -oA $RUN/raw/nmap_top "$TARGET" >/dev/null 2>&1 &
# 指纹
curl -sSk -D $RUN/raw/headers.txt -o $RUN/raw/body.html "https://$TARGET/"
```
之后每步把结果写进 `parsed/`，最后按 `reporting/deliverables.md` 汇总。

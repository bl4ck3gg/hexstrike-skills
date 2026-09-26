---
name: state
description: 运行状态管理：缓存复用、进程跟踪、遥测与仪表盘快照
when_to_use: 需要复用缓存、跟踪后台进程、生成运行快照时
---
# 运行状态管理

| 能力 | 做法 | 说明 |
|---|---|---|
| 缓存复用 | `$HX_ROOT/cache/` 目录 + 文件 mtime；`[ -f cache/x.json ] \|\| curl ... > cache/x.json` | 显式复用，无自动 TTL |
| 执行历史 | `raw/*.log`（命令+退出码+耗时） | 完整可回放 |
| 遥测 | `meta.txt` + `raw/` 统计 + 下方 dashboard 快照 | 按需生成，无实时指标流 |
| 异步/后台任务 | `nohup + $! + kill -0`（`basics/long-tasks.md`） | 无自动扩缩容 |
| 进程查看 | `ps -eo pid,etime,args`、`kill -TERM/-STOP/-CONT` | — |
| 进程仪表盘 | `ps ... \| grep "$RUN"` 快照 | 非实时 |
| 环境健康 | `command -v` 探测 + `df -h`/`free -m`/`uptime` | — |
| 报告产物 | `reporting/deliverables.md` 的报告（md/html） | — |
| 资源监测 | 静态规则 + `free`/`nproc`/`uptime` 判定（`optimization/parameter-optimizer.md`） | — |
| 错误历史 | `raw/` + `parsed/recovery_state.tsv` | — |

## 快照命令
```bash
{
  echo "# Run Dashboard"; echo
  echo "| field | value |"; echo "|---|---|"
  echo "| target | $TARGET |"; echo "| run | $HX_RUN_ID |"
  echo "| elapsed | $(( $(date +%s) - $(stat -c %Y $RUN/meta.txt) ))s |"
  echo "| commands | $(ls $RUN/raw | wc -l) |"
  echo "| findings | $(wc -l < $FINDINGS 2>/dev/null || echo 0) |"
  echo; echo "## Active processes"; echo '```'
  ps -eo pid,etime,pcpu,pmem,args | grep -E "$RUN|hexstrike" | grep -v grep || echo '(none)'
  echo '```'
} > $RUN/report/dashboard.md
df -h / | tail -1; free -m | sed -n 2p; uptime
```
原则：涉及"实时性"的能力按需重生成快照，不要假装实时。

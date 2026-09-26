---
name: long-tasks
description: 后台任务、并发、进度查看与崩溃恢复
when_to_use: 扫描预计超过 1 分钟，或需要并行跑多个工具
---
# 长任务与并发

## 后台执行
```bash
cd $RUN
nohup nmap -sS -p- -T4 -oA raw/nmap_full <target> > raw/nmap_full.console 2>&1 &
echo $! > raw/nmap_full.pid
```
- 进度：`tail -5 raw/nmap_full.console`
- 完成检测：`kill -0 $(cat raw/nmap_full.pid) 2>/dev/null && echo RUNNING || echo DONE`
- 等完成：`while kill -0 $(cat raw/nmap_full.pid) 2>/dev/null; do sleep 10; done; echo DONE`

## 并发
同一主机上并行跑多个工具，建议上限：
```
网络扫描     ≤2
Web 目录爆破 ≤3
信息收集类   4-5
```
```bash
nohup ffuf -u https://t/FUZZ -w list.txt -o raw/ffuf.json >/dev/null 2>&1 & echo $! > raw/ffuf.pid
nohup nuclei -u https://t -o raw/nuclei.txt     >/dev/null 2>&1 & echo $! > raw/nuclei.pid
wait $(cat raw/ffuf.pid) $(cat raw/nuclei.pid) 2>/dev/null
```
并发过高会触发目标限流（`optimization/rate-limit-detector.md`）或拖垮本机。

## 崩溃/中断恢复
```bash
ls $RUN/raw/*.log                          # 跑过哪些命令
grep -l "exit=0" $RUN/raw/*.log            # 成功的
```
失败命令按 `recovery/error-classifier.md` 分类后重跑，参数调整用
`recovery/parameter-adjustments.md`。

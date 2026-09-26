---
name: parameter-optimizer
description: 参数优化算法（基础→技术→资源→档位）
when_to_use: 为某个工具决定具体参数
---
# 参数优化算法（后一步覆盖前一步）

## 步骤 1 基础参数 `_get_base_parameters`
```
nmap     {-scan_type:"-sS", -p:"1-1000", -T4}
gobuster {mode:dir, -t:20, -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt}
sqlmap   {--batch --level 1 --risk 1}
nuclei   {-severity critical,high,medium -t 25}
```

## 步骤 2 技术优化
见 `intelligence/tech-fingerprints.md` 的"参数联动"。

## 步骤 3 资源优化
```bash
mem=$(free -m | awk '/Mem:/{print $7}'); cpu=$(nproc)
load=$(uptime | sed 's/.*load average: *//' | cut -d, -f1)
echo "avail=${mem}MB cpu=$cpu load=$load"
```
```
mem < 1024 或 load > cpu*1.5 -> 降并发: -t min(t,5)
mem < 512                    -> -t 3, 限内存
否则                          -> 保持
```

## 步骤 4 档位 `_apply_profile_optimizations`
```
nmap     stealth   -sS -T2 --max-retries 1 --host-timeout 300s
         normal    -sS -sV -T4 --max-retries 2
         aggressive -sS -sV -sC -O -T5 --max-retries 3 --min-rate 1000
gobuster stealth   -t 5 --delay 1s --timeout 30s
         normal    -t 20 --delay 0s --timeout 10s
         aggressive -t 50 --delay 0s --timeout 5s
sqlmap   stealth   --level 1 --risk 1 --threads 1 --delay 1
         normal    --level 2 --risk 2 --threads 5 --delay 0
         aggressive --level 3 --risk 3 --threads 10 --delay 0
```
**stealth 强制**：技术指纹命中 WAF 时，即使请求 normal/aggressive，也套 stealth。

## 步骤 5 记录
把最终参数写 `parsed/params_<tool>.txt`（含 tech / 资源 / 档位 / 应用了哪些优化）。

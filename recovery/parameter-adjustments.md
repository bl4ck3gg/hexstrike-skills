---
name: parameter-adjustments
when_to_use: ADJUST_PARAMETERS 时
---
# 参数自动调整
## nmap
TIMEOUT → timing=-T2, reduce_ports=true
RATE_LIMITED → timing=-T1, delay=1000ms
RESOURCE_EXHAUSTED → max_parallelism=10
## gobuster
TIMEOUT → threads=10, timeout=30s
RATE_LIMITED → threads=5, delay=1s
## nuclei
TIMEOUT → concurrency=10, timeout=30
RATE_LIMITED → rate-limit=10, concurrency=5
## feroxbuster
TIMEOUT → threads=10, timeout=30
RATE_LIMITED → threads=5, rate-limit=10
## ffuf
TIMEOUT → threads=10, timeout=30
RATE_LIMITED → threads=5, rate=10
## 通用
TIMEOUT → timeout×2, threads÷2
RATE_LIMITED → 切 stealth timing
RESOURCE_EXHAUSTED → threads=3, memory_limit=1G

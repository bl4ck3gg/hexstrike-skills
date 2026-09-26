---
name: rate-limit-detector
description: 限流置信度打分与 timing 档位
when_to_use: 目标返回 429 或出现限流文本
---
# 限流检测

## 检测
```bash
curl -sSk -o $RUN/raw/rl.body -D $RUN/raw/rl.hdr -w '%{http_code}\n' '<url>'
code=$(curl -sSk -o /dev/null -w '%{http_code}' '<url>')
grep -ioE 'rate limit|too many requests|throttle|slow down|retry after|quota exceeded|api limit|request limit' $RUN/raw/rl.body | sort -u
grep -iE '^x-ratelimit|^retry-after|^x-rate-limit' $RUN/raw/rl.hdr
```

## 置信度
```
confidence = 0
 + 0.8  if HTTP 429
 + 0.2  每个命中的文本指标
 + 0.3  每个命中的 header
confidence = min(1.0, confidence)
推荐档位: >=0.8 stealth | >=0.5 conservative | >=0.2 normal | else aggressive
```

## timing 表与改写
```
aggressive   delay 0.1 threads 50 timeout 5
normal       delay 0.5 threads 20 timeout 10
conservative delay 1.0 threads 10 timeout 15
stealth      delay 2.0 threads 5  timeout 30
```
```bash
# 改写命令里的并发参数（先删再追加）
args=$(echo "$args" | sed -E 's/-t +[0-9]+//g; s/--threads +[0-9]+//g; s/--delay +[0-9.]+//g')
args="$args -t 5 --delay 2"
```

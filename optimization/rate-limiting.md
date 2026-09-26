---
name: rate-limiting
when_to_use: 目标 429/throttle
---
# 限流检测
## 指标
文本: rate limit / too many requests / 429 / throttle / slow down / retry after / quota exceeded / api limit / request limit
状态码: 429
Header: x-ratelimit* / retry-after / x-rate-limit*

## 置信度
429 +0.8 | 文本命中 +0.2 each | Header +0.3 each

## Timing Profiles
| 档位 | delay | threads | timeout |
|------|-------|---------|---------|
| aggressive | 0.1 | 50 | 5 |
| normal | 0.5 | 20 | 10 |
| conservative | 1.0 | 10 | 15 |
| stealth | 2.0 | 5 | 30 |

## 推荐
≥0.8 stealth | ≥0.5 conservative | ≥0.2 normal | else aggressive

## 调整
移除 -t N / --threads N / --delay N,追加新值

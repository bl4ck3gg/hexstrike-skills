---
name: ctf-crypto
when_to_use: CTF Crypto
---
# CTF Crypto 策略
1. frequency_analysis
2. known_plaintext
3. weak_keys
4. implementation_flaws
5. side_channel
6. mathematical_attacks

## 工作流
| 步 | 动作 | 工具 | 并行 | 耗时 |
|----|------|------|------|------|
| 1 | 密码识别 | cipher-identifier, hash-identifier | ✗ | 300s |
| 2 | 密钥空间 | manual | ✗ | 600s |
| 3 | 自动攻击 | hashcat, john, factordb | ✓ | 1800s |
| 4 | 数学分析 | sage, python | ✗ | 1200s |
| 5 | 频率分析 | frequency-analysis, substitution-solver | ✓ | 900s |
| 6 | 已知明文 | custom | ✗ | 1200s |
| 7 | 实现分析 | manual | ✗ | 900s |
| 8 | 验证 | manual | ✗ | 300s |

## 回退
known_plaintext_attack / frequency_analysis_variants / mathematical_properties / implementation_weaknesses / side_channel_analysis

## 验证
decryption_verification / key_validation / mathematical_check / flag_extraction

---
name: ctf-web
when_to_use: CTF Web
---
# CTF Web 策略
1. source_code_analysis
2. directory_traversal
3. sql_injection
4. xss_exploitation
5. authentication_bypass
6. session_manipulation
7. file_upload_bypass

## 工作流
| 步 | 动作 | 工具 | 并行 | 耗时 |
|----|------|------|------|------|
| 1 | 自动侦察 | httpx, whatweb, katana | ✓ | 300s |
| 2 | 源码分析 | manual | ✗ | 600s |
| 3 | 目录枚举 | gobuster, dirsearch, feroxbuster | ✓ | 900s |
| 4 | 参数发现 | arjun, paramspider | ✓ | 600s |
| 5 | 漏洞扫描 | sqlmap, dalfox, nikto | ✓ | 1200s |
| 6 | 手动测试 | manual | ✗ | 1800s |
| 7 | 利用 | custom | ✗ | 900s |
| 8 | flag | manual | ✗ | 300s |

## 回退
manual_source_review / alternative_wordlists / parameter_pollution / race_conditions / business_logic

## 验证
response_validation / payload_verification / flag_format_check / reproducibility_test

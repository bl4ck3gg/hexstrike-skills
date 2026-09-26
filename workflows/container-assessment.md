---
name: container-security-assessment
when_to_use: 评估容器
---
| # | 工具 | 参数 |
|---|------|------|
| 1 | trivy | scan_type=image, severity="HIGH,CRITICAL" |
| 2 | clair | output_format=json |
| 3 | docker-bench-security | - |

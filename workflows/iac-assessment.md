---
name: iac-security-assessment
when_to_use: 评估 IaC
---
| # | 工具 | 参数 |
|---|------|------|
| 1 | checkov | output_format=json |
| 2 | terrascan | scan_type=all, output_format=json |
| 3 | trivy | scan_type=config, severity="HIGH,CRITICAL" |

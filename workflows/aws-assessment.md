---
name: aws-security-assessment
when_to_use: 评估 AWS 账号
---
| # | 工具 | 参数 |
|---|------|------|
| 1 | prowler | provider=aws, output_format=json |
| 2 | scout-suite | provider=aws |
| 3 | cloudmapper | action=collect |
| 4 | pacu | modules="iam__enum_users_roles_policies_groups" |

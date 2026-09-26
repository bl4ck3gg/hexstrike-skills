---
name: checkov
category: IaC安全
description: IaC 扫描
when_to_use: 需要执行 checkov 时
---
# checkov
**类别**: IaC安全
**用途**: IaC 扫描

**底层命令行**:
```bash
checkov -d <dir> [--framework terraform] --output json
```

失败时参考 ../recovery/tool-alternatives.md

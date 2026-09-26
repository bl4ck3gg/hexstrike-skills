---
name: nuclei
category: 漏洞扫描
description: 模板化漏洞扫描
when_to_use: 需要执行 nuclei 时
---
# nuclei
**类别**: 漏洞扫描
**用途**: 模板化漏洞扫描

**底层命令行**:
```bash
nuclei -u <target> [-severity critical,high] [-tags cve,rce]
```

失败时参考 ../recovery/tool-alternatives.md

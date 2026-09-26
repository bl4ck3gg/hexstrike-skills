---
name: conventions
description: findings.tsv 约定、结果落盘规范、输出解析
when_to_use: 记录发现、做报告、跨步骤取数
---
# 记录约定

## findings.tsv（唯一漏洞源，制表符分隔）
```
sev  kind  title  target  tool  evidence
```
- `sev ∈ {critical,high,medium,low,info}`
- 记录：`add_finding "$sev" "$kind" "$title" "$target" "$tool" "$evidence"`
- 去重：`dedupe_findings`（按 sev/kind/title/target 四列）
- 证据里的制表符/换行要替换掉，否则破坏列结构：
  `evidence=$(echo "$raw" | tr '\t\n' '  ' | cut -c1-500)`

## 各能力统一落盘位置
| 能力 | 原始输出 | 解析结果 |
|---|---|---|
| 端口扫描 | `raw/nmap.log` + `raw/nmap.xml` | `parsed/ports.json` |
| 技术指纹 | `raw/headers.txt` | `parsed/tech.json` |
| HTTP 测试 | `raw/repeater.*` `raw/intruder.body` | 直接进 findings |
| API 测试 | `raw/api_*.json` | `parsed/api_*.json` |
| 情报 | `raw/nvd_*.json` | `parsed/cve_*.json` |
| 浏览器 | `artifacts/dom.html` `artifacts/*.png` | 直接进 findings |

## 多行命令的处理
命令块可直接粘贴执行；需要多行 stdin 时用 heredoc 一步到位：
```bash
python3 - <<'PY'
<文档里的代码块>
PY
```
不需要先落成脚本文件；只有需要反复执行的长逻辑才建议存到 `$RUN/` 下。

## 输出解析
ANSI/提示符噪声清洗：
```bash
... 2>/dev/null | sed -r 's/\x1B\[[0-9;]*[mK]//g' | grep -v '^$'
```
从混合输出里提取 JSON：
```bash
python3 -c "import json,sys,re;d=sys.stdin.read();m=re.search(r'\{.*\}',d,re.S);print(json.dumps(json.loads(m.group(0)),indent=2))" < out.txt
```
nmap XML → 端口表：
```bash
python3 - /path/nmap.xml <<'PY'
import json,re,sys
x=open(sys.argv[1]).read()
print(json.dumps([{"port":p,"state":s,"service":sv} for p,s,sv in
  re.findall(r'<port protocol="\w+" portid="(\d+)">.*?<state state="(\w+)".*?<service name="([^"]*)"', x, re.S)], indent=2))
PY
```

## 严重度判定
| 级别 | 典型 |
|---|---|
| critical | alg=none JWT 被接受、密码明文表单、RCE 确认 |
| high | 反射 XSS、SQL 错误、敏感信息泄露、公开 exploit、GraphQL 无深度限制 |
| medium | 缺安全头、无 CSRF、无鉴权端点、弱 cookie 标志 |
| low | 内联 JS、外链脚本无 SRI |
| info | 端点发现、过程信息 |

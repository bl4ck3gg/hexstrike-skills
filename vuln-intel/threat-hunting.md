---
name: threat-hunting
description: 威胁狩猎（蓝队）：环境检测查询、IOC 关联、调查步骤与处置
when_to_use: 在已授权环境内排查可疑活动（应急响应/护网/威胁情报落地）
---
# 威胁狩猎

输入：环境（Windows Domain / Cloud Infrastructure / Linux / 通用）、
IOC（IP/域名/哈希/进程名/CVE，逗号分隔）、
focus ∈ {general, apt, ransomware, insider_threat, supply_chain}。

原则：**只读取证优先**，任何封禁/隔离前先把证据固定到 `$RUN/artifacts/`；
检测命令都在**被授权主机/账号**上跑，不做无授权的横向探测。

## 1. 环境检测查询

### Windows Domain（PowerShell）
```powershell
# 在被授权主机上建证据目录，再采集
New-Item -ItemType Directory -Force -Path .\artifacts | Out-Null

# 可疑进程创建（4688）与编码命令行
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4688} -MaxEvents 500 |
  Where-Object {$_.Message -match 'powershell .*-enc|rundll32|regsvr32|mshta|wmic|bitsadmin'} |
  Select-Object TimeCreated,Message | Export-Csv -NoTypeInformation .\artifacts\win_4688.csv

# 自启动与计划任务
Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run',
                 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' |
  Select-Object *Run* | Format-List
Get-ScheduledTask | Where-Object {$_.State -ne 'Disabled'} |
  Select-Object TaskName,TaskPath,@{n='Action';e={$_.Actions.Execute + ' ' + $_.Actions.Arguments}}
```
```powershell
# 外部连接与本机监听（排除内网/环回）
Get-NetTCPConnection -State Established |
  Where-Object {$_.RemoteAddress -notmatch '^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|127\.)'} |
  Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,OwningProcess
Get-CimInstance Win32_StartupCommand | Select-Object Name,Command,Location,User
```

### Linux（取证镜像/主机）
```bash
# 登录与提权
last -aiF | head -30; lastb -aiF 2>/dev/null | head -20
grep -iE 'Failed password|Accepted' /var/log/auth.log /var/log/secure 2>/dev/null | tail -50

# 近期进程/持久化
ps -eo pid,ppid,user,lstart,args --sort=-lstart | head -30
crontab -l 2>/dev/null; ls -la /etc/cron.* /var/spool/cron /etc/systemd/system 2>/dev/null
grep -r . /etc/ld.so.preload 2>/dev/null
find /tmp /dev/shm /var/tmp -type f -mtime -7 -ls 2>/dev/null | head -50

# 外连
ss -tunap | grep -v '127.0.0.1\|::1'
```

### Cloud Infrastructure（AWS，CloudTrail/IAM/S3）
```bash
REGION=${REGION:-us-east-1}
# 近期控制台登录与高风险 API
aws cloudtrail lookup-events --region "$REGION" --max-results 100 \
  --lookup-attributes AttributeKey=EventName,AttributeValue=ConsoleLogin \
  | jq -r '.Events[] | [.EventTime,.Username,.CloudTrailEvent] | @tsv' | tee $RUN/raw/cloudtrail_login.tsv
aws cloudtrail lookup-events --region "$REGION" --max-results 100 \
  | jq -r '.Events[] | select(.CloudTrailEvent|test("CreateAccessKey|AttachUserPolicy|PutBucketAcl|AuthorizeSecurityGroupIngress"))
            | [.EventTime,.Username,.EventName] | @tsv' | tee -a $RUN/raw/cloudtrail_highrisk.tsv

# 公开暴露面
aws ec2 describe-security-groups --region "$REGION" \
  --filters Name=ip-permission.cidr,Values=0.0.0.0/0 \
  --query 'SecurityGroups[].[GroupId,GroupName]' --output text
aws s3api list-buckets --query 'Buckets[].Name' --output text | while read -r b; do
  aws s3api get-bucket-acl --bucket "$b" 2>/dev/null \
    | jq -r --arg b "$b" 'select(.Grants[]?.Grantee.URI|test("AllUsers"))|"PUBLIC \($b)"'
done
```

## 2. 场景化焦点（hunt_focus）

| focus | 典型行为 | 检测点 |
|---|---|---|
| `apt` | 鱼叉钓鱼、Living-off-the-Land、窃取凭据横向、数据暂存外传 | Office→powershell 父子进程、WMI/SMB 横向、大流量出站 |
| `ransomware` | RDP/VPN 初始访问、提权持久化、删除卷影、加密与勒索信 | `vssadmin delete shadows`、大批文件重命名、异常加密 IO |
| `insider_threat` | 异常数据访问、非工作时间、批量下载、访问敏感系统 | 权限外对象访问、S3/共享盘批量 GET、离职前行为突变 |
| `supply_chain` | 构建产物被篡改、依赖投毒、CI 凭据滥用 | CI 日志中的新发布者、依赖 hash 变化、令牌外联 |
| `general` | 未授权访问、可疑进程、网络异常、数据访问违规 | 上面全部基础查询 |

## 3. IOC 关联（复用 `vuln-intel/threat-feeds.md`）

```bash
# CVE 类 IOC → KEV/EPSS/NVD；hash → 公开情报源；域名 → URLhaus；其余本地检索
while IFS= read -r ioc; do
  if printf '%s' "$ioc" | grep -qE '^CVE-[0-9]{4}-[0-9]+$'; then
    curl -sS "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=$ioc" -o $RUN/raw/nvd_$ioc.json
    grep -i "$ioc" $RUN/parsed/kev_recent.tsv && echo "!! KEV: $ioc"
    curl -sS "https://api.first.org/data/v1/epss?cve=$ioc" \
      | jq -r --arg c "$ioc" '.data[]? | "\($c) EPSS=\(.epss) pct=\(.percentile)"'
  elif printf '%s' "$ioc" | grep -qE '^[0-9a-fA-F]{32}$|^[0-9a-fA-F]{40}$|^[0-9a-fA-F]{64}$'; then
    curl -sS -X POST https://mb-api.abuse.ch/api/v1/ --data-urlencode "query=get_info" \
      --data-urlencode "hash=$ioc" | jq -r '.query_status, (.data[]?.file_name // empty)'
  else
    curl -sS -X POST https://urlhaus-api.abuse.ch/v1/host/ --data-urlencode "host=$ioc" \
      | jq -r '[.query_status, (.urls[]?.url_status // empty)] | @tsv'
  fi
  grep -ri -- "$ioc" $RUN/raw/ 2>/dev/null | head -5
done <<'IOC'
<CVE-YYYY-NNNNN>
<malware.exe 的 sha256>
<suspicious.example.com>
<IOC>
```
命中记 findings（`add_finding high threat_ioc ...`），KEV/EPSS 判高优先级。

## 4. 调查步骤（固定顺序）
```
1. 验证初始 IOC，扩展关联 IOC（域名/同 IP/同 hash 家族）
2. 跑第 1 节的检测查询，结果落 raw/，命中落 parsed/
3. 跨数据源关联（EDR/日志/流量/云审计），建时间线
4. 确定受影响主机与账号，标注数据敏感性
5. 评估范围与影响（是否已外传、权限是否提升）
6. 确认威胁后按第 5 节处置（先固定证据再动作）
7. 输出结论并更新检测规则（IOC→规则）
```

## 5. 处置与建议
```
遏制: 隔离主机/禁用会话/吊销凭据（先采集内存与磁盘镜像）
清除: 删除持久化项/恶意文件，封禁 IOC（防火墙/DNS/EDR）
恢复: 从可信备份恢复，改密，复测
加固: 强制 MFA、最小权限、限制 RDP/VPN 来源、开启审计日志
```
每条处置记录：`time \t action \t target \t operator \t evidence`，写入
`$RUN/parsed/hunt_actions.tsv`（时间线可回放）。

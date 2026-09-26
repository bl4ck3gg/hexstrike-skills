---
name: attack-chains
description: 攻击链规划配方（阶段 + 复合概率）
when_to_use: 已知目标软件，规划纵深利用
---
# 攻击链规划

概率为示意值，用于排序而不是定论。

## 模式与阶段
```
privilege_escalation: local, kernel, suid, sudo
remote_execution:     remote, network, rce, code execution
persistence:          service, registry, scheduled, startup
lateral_movement:     smb, wmi, ssh, rdp
data_exfiltration:    file, database, memory, network
阶段: 1 Initial Access p=0.75 | 2 Privilege Escalation p=0.60 | 3 Persistence p=0.80
overall = 0.75*0.60*0.80 = 0.36 (复合乘积)
```
软件关系：`windows[iis,office,exchange,sharepoint] linux[apache,nginx,mysql,postgresql]
web[php,nodejs,python,java] database[mysql,postgresql,oracle,mssql]`

## 用真实 CVE 填充阶段（必须用真实数据，不得编造 CVE）
```bash
SW='Apache HTTP Server'
curl -sS -G 'https://services.nvd.nist.gov/rest/json/cves/2.0' \
  --data-urlencode "keywordSearch=$SW" --data-urlencode resultsPerPage=20 \
  -o $RUN/raw/nvd_soft.json
jq -r '.vulnerabilities[] | .cve as $c
  | (($c.metrics.cvssMetricV31 // $c.metrics.cvssMetricV30 // [{}])[0].cvssData) as $m
  | select(($m.baseScore // 0) >= 7)
  | [$c.id, (($m.baseScore)|tostring), ($c.descriptions[]|select(.lang=="en")|.value|.[0:120])] | @tsv' \
  $RUN/raw/nvd_soft.json | sort -k2 -nr | tee $RUN/parsed/chain_candidates.tsv
```
然后把候选填进阶段表，逐阶段做 exploit-search / exploit-generate：
```bash
while IFS=$'\t' read -r id score desc; do
  grep -oE 'remote|network|rce|code execution' <<< "$desc" >/dev/null && echo "stage1(initial) $id $score"
  grep -oE 'local|kernel|suid|sudo' <<< "$desc" >/dev/null && echo "stage2(privesc) $id $score"
  grep -oE 'service|registry|scheduled|startup' <<< "$desc" >/dev/null && echo "stage3(persist) $id $score"
done < $RUN/parsed/chain_candidates.tsv
```
概率计算：`awk 'BEGIN{p=.75*.60*.80; printf "overall=%.4f\n",p}'`。
**链是规划骨架，不是漏洞证据**；概率是示意值，不是实测。

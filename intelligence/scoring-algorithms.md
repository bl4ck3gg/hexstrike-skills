---
name: scoring-algorithms
description: 目标分析/工具选择/攻击链的判断与打分算法
when_to_use: 判断目标类型、给工具排序、估算成功率
---
# 决策算法

算法基于**实际 HTTP 探测结果**判断技术栈（见 `intelligence/tech-fingerprints.md`），
而不是仅凭目标字符串猜测。

## 1. 目标类型判定 `_determine_target_type`
按顺序短路：
```
1. http(s):// 开头: 路径含 "/api/" 或以 "/api" 结尾 -> API_ENDPOINT, 否则 WEB_APPLICATION
2. ^(\d{1,3}\.){3}\d{1,3}$          -> NETWORK_HOST
3. ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$   -> WEB_APPLICATION
4. .exe/.bin/.elf/.so/.dll 结尾      -> BINARY_FILE
5. 含 amazonaws.com/azure/googleapis.com -> CLOUD_SERVICE
6. 其他                              -> UNKNOWN
```
顺序陷阱：URL 判断在 IP/域名之前，云判断在最后。

## 2. 攻击面打分 `_calculate_attack_surface`
```
score = type_score + len(technologies)*0.5 + len(open_ports)*0.3
        + len(subdomains)*0.2 + (1.5 if cms_type else 0)
score = min(score, 10.0)
type_score: WEB 7.0 | API 6.0 | NETWORK_HOST 8.0 | CLOUD 5.0 | BINARY 4.0 | 其他 3.0
```

## 3. 风险等级：`>=8 critical | >=6 high | >=4 medium | >=2 low | else minimal`

## 4. 置信度
```
0.5 + 0.1(有 IP) + 0.2(technologies 非空且非 UNKNOWN) + 0.1(有 CMS) + 0.1(类型非 UNKNOWN)
上限 1.0
```

## 5. 工具有效性评分表（选工具的唯一依据）
```
WEB_APPLICATION: nmap .8 gobuster .9 nuclei .95 nikto .85 sqlmap .9 ffuf .9
 feroxbuster .85 katana .88 httpx .85 wpscan .95 burpsuite .9 dirsearch .87 gau .82
 waybackurls .8 arjun .9 paramspider .85 x8 .88 jaeles .92 dalfox .93
 anew .7 qsreplace .75 uro .7
NETWORK_HOST: nmap .95 nmap-advanced .97 masscan .92 rustscan .9 autorecon .95
 enum4linux .8 enum4linux-ng .88 smbmap .85 rpcclient .82 nbtscan .75 arp-scan .85
 responder .88 hydra .8 netexec .85 amass .7
API_ENDPOINT: nuclei .9 ffuf .85 arjun .95 paramspider .88 httpx .9 x8 .92 katana .85
 jaeles .88 postman .8
CLOUD_SERVICE: prowler .95 scout-suite .92 cloudmapper .88 pacu .85 trivy .9 clair .85
 kube-hunter .9 kube-bench .88 docker-bench-security .85 falco .87 checkov .9 terrascan .88
BINARY_FILE: ghidra .95 radare2 .9 gdb .85 gdb-peda .92 angr .88 pwntools .9 ropgadget .85
 ropper .88 one-gadget .82 libc-database .8 checksec .75 strings .7 objdump .75 binwalk .8 pwninit .85
```

## 6. 工具选择 `select_optimal_tools`
```
quick         -> 该类型评分降序前 3
comprehensive -> 评分 > 0.7 全部
stealth       -> 仅 [amass, subfinder, httpx, nuclei] 中存在的
其他          -> 全部
# 技术加成
含 WORDPRESS 且无 wpscan -> 追加 wpscan
含 PHP       且无 nikto  -> 追加 nikto
```

## 7. 攻击链 `create_attack_chain`
剧本见 `intelligence/attack-patterns.md`。每步：
```
success_probability = tool_effectiveness[type][tool] * confidence
execution_time      = 下表，秒；未列出默认 180
chain.success_probability = ∏ 各步（复合概率）
chain.estimated_time      = Σ
```
`nmap 120 gobuster 300 nuclei 180 nikto 240 sqlmap 600 ffuf 200 hydra 900 amass 300
ghidra 300 radare2 180 gdb 120 gdb-peda 150 angr 600 pwntools 240 ropper 120
one-gadget 60 checksec 30 pwninit 60 libc-database 90 prowler 600 scout-suite 480
cloudmapper 300 pacu 420 trivy 180 clair 240 kube-hunter 300 kube-bench 120
docker-bench-security 180 falco 120 checkov 240 terrascan 200`

**纯 shell 计算**（把候选工具作为参数）：
```bash
python3 - "$CONF" nmap gobuster nuclei <<'PY'
import sys
eff={"nmap":.8,"gobuster":.9,"nuclei":.95,"nikto":.85,"sqlmap":.9,"ffuf":.9}
t={"nmap":120,"gobuster":300,"nuclei":180,"nikto":240,"sqlmap":600,"ffuf":200}
conf=float(sys.argv[1]); chain=1.0; est=0
for tool in sys.argv[2:]:
    p=eff.get(tool,.5)*conf; chain*=p; est+=t.get(tool,180)
    print(f"{tool:12s} p={p:.3f} t={t.get(tool,180)}s")
print(f"chain P={chain:.6f} est={est}s")
PY
```

## 8. 执行流程（smart-scan 入口）
```
1. 探测存活/端口/技术栈 -> parsed/ports.json、parsed/tech.json
2. §1-4 算画像 -> parsed/target_profile.json
3. §5-6 选工具 -> parsed/selected_tools.txt
4. §7 建链    -> parsed/attack_chain.txt
5. 执行 workflows/<pattern>.md，结果落 findings
6. reporting/deliverables.md 出报告
```

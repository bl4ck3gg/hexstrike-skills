---
name: environment
description: 工具探测、依赖安装、运行目录约定
when_to_use: 开始任务前
---
# 环境检查

## 1. 引导块（每个任务开始时执行一次）
```bash
export TARGET='<target>'
export SKILLS='<skill包根>'          # 本包根目录（含 scripts/）
export HX_ROOT=/tmp/hexstrike
export HX_RUN_ID=$(echo "$TARGET" | tr '/: ' '___')-$(date +%Y%m%d-%H%M%S)
export RUN=$HX_ROOT/$HX_RUN_ID
export FINDINGS=$RUN/parsed/findings.tsv
mkdir -p $RUN/{raw,parsed,report,artifacts}
printf '# %s %s\n' "$TARGET" "$(date -u +%FT%TZ)" > $RUN/meta.txt

# 引入 add_finding / dedupe_findings / classify / rule / in_scope
source "$SKILLS/scripts/hx.sh"
hx_selftest            # 校验 RUN/FINDINGS 与函数就位
```

> **为什么必须 source**：termcp 每次执行基本是独立 shell，
> 函数不会跨调用存活。不 source 则 `add_finding` 不存在，findings 会丢。

## 2. 工具探测
```bash
for t in nmap masscan rustscan gobuster ffuf feroxbuster dirsearch nikto nuclei jaeles \
         sqlmap dalfox xsser wpscan whatweb zaproxy httpx katana gau waybackurls hakrawler \
         arjun paramspider x8 anew qsreplace uro subfinder amass assetfinder fierce dnsenum \
         smbmap netexec enum4linux-ng rpcclient responder hydra john hashcat searchsploit \
         gdb radare2 objdump strings xxd binwalk foremost exiftool steghide volatility \
         ropper ROPgadget one_gadget checksec pwninit ghidra jadx apktool upx \
         prowler scout cloudmapper pacu trivy clairctl kube-hunter kube-bench \
         docker-bench-security falco checkov terrascan msfconsole msfvenom \
         curl wget jq python3 pip3 go git docker kubectl aws tshark zsteg \
         chromium chromium-browser google-chrome; do
  p=$(command -v $t 2>/dev/null) && printf '%-22s %s\n' "$t" "$p" || printf '%-22s MISSING\n' "$t"
done | tee $RUN/parsed/toolcheck.txt
```
缺失项 → 查 `recovery/tool-alternatives.md` 换等价工具；Kali/Debian 上
`sudo apt-get install -y <tool>`。

## 3. python 依赖
```bash
python3 -c "import requests" 2>/dev/null || pip3 install --break-system-packages requests
python3 -c "import jwt"      2>/dev/null || pip3 install --break-system-packages pyjwt
which chromium chromium-browser google-chrome 2>/dev/null || echo "无浏览器: 用 curl 降级（browser/inspection.md）"
```
**不需要 playwright 也能完成大部分检查**（见 `browser/inspection.md` 的能力阶梯）。

## 4. 目录约定
```
$RUN/
  meta.txt      # 目标 + 开始时间
  raw/          # 每条命令的完整 stdout+stderr（丢输出可恢复）
  parsed/       # 规范化结果 + findings.tsv（唯一漏洞源）
  report/       # markdown / html 交付物
  artifacts/    # 截图、pcap、生成的 exploit、下载文件
```
跨任务复用：`cp parsed/<x>.json $HX_ROOT/cache/`（见 `basics/state.md`）。

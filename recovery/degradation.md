---
name: graceful-degradation
description: 关键操作降级链与部分失败补位
when_to_use: 关键工具全部失败，仍需给出最低限度结论
---
# 优雅降级

## 降级链
```
network_discovery      1[nmap,rustscan,masscan] 2[rustscan,nmap] 3[ping,telnet]
web_discovery          1[gobuster,feroxbuster,dirsearch] 2[feroxbuster,ffuf] 3[curl,wget]
vulnerability_scanning 1[nuclei,jaeles,nikto] 2[nikto,w3af] 3[curl]
subdomain_enumeration  1[subfinder,amass,assetfinder] 2[amass,findomain] 3[dig,nslookup]
parameter_discovery    1[arjun,paramspider,x8] 2[ffuf,wfuzz] 3[manual_testing]
```
选链：取第一条不含已失败工具的；全不满足用兜底
`network→ping / web→curl / vuln→curl / subdomain→dig / 其他→manual_testing`。

## 部分失败补位（纯 shell）
```bash
# open_ports 缺失：11 个常见端口 2s 探测
for p in 21 22 23 25 53 80 110 143 443 993 995; do
  timeout 2 bash -c "</dev/tcp/<host>/$p" 2>/dev/null && echo "$p open"
done
# directories 缺失：HEAD 探测
for d in /admin /login /api /wp-admin /phpmyadmin /robots.txt; do
  code=$(curl -sSk -o /dev/null -w '%{http_code}' "<url>$d")
  case $code in 200|301|302|403) echo "$d $code";; esac
done
# vulnerabilities 缺失：5 个安全头
for h in X-Frame-Options X-Content-Type-Options X-XSS-Protection Strict-Transport-Security Content-Security-Policy; do
  grep -qi "^$h:" $RUN/raw/headers.txt || echo "MISSING $h (medium)"
done
```
输出结构加 `degradation_info{operation,failed_components,partial_success,fallback_applied}`。

## 手工建议
```
network: telnet/nc 手测、看 banner、在线端口扫描器
web:     浏览常见目录、robots.txt/sitemap.xml、浏览器开发者工具
vuln:    手测常见漏洞、浏览器查安全头、手工输入校验
subdomain: 在线子域工具、crt.sh 证书透明、手工 dig
```

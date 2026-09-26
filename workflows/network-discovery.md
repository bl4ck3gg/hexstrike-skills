---
name: network-discovery
when_to_use: 目标为 IP/网段
---
# 网络发现剧本
| # | 工具 | 参数 |
|---|------|------|
| 1 | arp-scan | local_network=true |
| 2 | rustscan | ulimit=5000, scripts=true |
| 3 | nmap-advanced | scan_type="-sS", os_detection=true, version_detection=true |
| 4 | masscan | rate=1000, ports="1-65535", banners=true |
| 5 | enum4linux-ng | shares/users/groups=true |
| 6 | nbtscan | verbose=true |
| 7 | smbmap | recursive=true |
| 8 | rpcclient | commands="enumdomusers;enumdomgroups;querydominfo" |

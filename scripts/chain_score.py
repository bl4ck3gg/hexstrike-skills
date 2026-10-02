#!/usr/bin/env python3
"""攻击链复合概率与耗时估算

用法:
    chain_score.py <confidence> <tool> [tool ...]
    chain_score.py <confidence> --type api_endpoint nmap ffuf httpx
    chain_score.py 0.8 nmap gobuster nuclei

公式（见 intelligence/scoring-algorithms.md §7）:
    success_probability = tool_effectiveness[type][tool] * confidence
    chain.success_probability = 各步乘积
    chain.estimated_time      = 各步之和
"""
import sys

# 与 intelligence/scoring-algorithms.md §5 一致（按目标类型分表）
EFFECTIVENESS = {
    "web_application": {
        "nmap": 0.8, "gobuster": 0.9, "nuclei": 0.95, "nikto": 0.85,
        "sqlmap": 0.9, "ffuf": 0.9, "feroxbuster": 0.85, "katana": 0.88,
        "httpx": 0.85, "wpscan": 0.95, "burpsuite": 0.9, "dirsearch": 0.87,
        "gau": 0.82, "waybackurls": 0.8, "arjun": 0.9, "paramspider": 0.85,
        "x8": 0.88, "jaeles": 0.92, "dalfox": 0.93, "anew": 0.7,
        "qsreplace": 0.75, "uro": 0.7,
    },
    "api_endpoint": {
        "nuclei": 0.9, "ffuf": 0.85, "arjun": 0.95, "paramspider": 0.88,
        "httpx": 0.9, "x8": 0.92, "katana": 0.85, "jaeles": 0.88,
        "postman": 0.8,
    },
    "network_host": {
        "nmap": 0.95, "nmap-advanced": 0.97, "masscan": 0.92, "rustscan": 0.9,
        "autorecon": 0.95, "enum4linux": 0.8, "enum4linux-ng": 0.88,
        "smbmap": 0.85, "rpcclient": 0.82, "nbtscan": 0.75,
        "arp-scan": 0.85, "responder": 0.88, "hydra": 0.8, "netexec": 0.85,
        "amass": 0.7,
    },
    "cloud_service": {
        "prowler": 0.95, "scout-suite": 0.92, "cloudmapper": 0.88,
        "pacu": 0.85, "trivy": 0.9, "clair": 0.85, "kube-hunter": 0.9,
        "kube-bench": 0.88, "docker-bench-security": 0.85, "falco": 0.87,
        "checkov": 0.9, "terrascan": 0.88,
    },
    "binary_file": {
        "ghidra": 0.95, "radare2": 0.9, "gdb": 0.85, "gdb-peda": 0.92,
        "angr": 0.88, "pwntools": 0.9, "ropgadget": 0.85, "ropper": 0.88,
        "one-gadget": 0.82, "libc-database": 0.8, "checksec": 0.75,
        "strings": 0.7, "objdump": 0.75, "binwalk": 0.8, "pwninit": 0.85,
    },
}

ALIASES = {
    "web": "web_application", "api": "api_endpoint",
    "network": "network_host", "cloud": "cloud_service",
    "binary": "binary_file", "host": "network_host",
}

# 执行耗时（秒）；未列出默认 180
TIMES = {
    "nmap": 120, "gobuster": 300, "nuclei": 180, "nikto": 240, "sqlmap": 600,
    "ffuf": 200, "hydra": 900, "amass": 300, "ghidra": 300, "radare2": 180,
    "gdb": 120, "gdb-peda": 150, "angr": 600, "pwntools": 240, "ropper": 120,
    "one-gadget": 60, "checksec": 30, "pwninit": 60, "libc-database": 90,
    "prowler": 600, "scout-suite": 480, "cloudmapper": 300, "pacu": 420,
    "trivy": 180, "clair": 240, "kube-hunter": 300, "kube-bench": 120,
    "docker-bench-security": 180, "falco": 120, "checkov": 240, "terrascan": 200,
}

DEFAULT_EFF = 0.5
DEFAULT_TIME = 180


def main(argv: list) -> int:
    if len(argv) < 3 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if len(argv) > 1 else 2

    args = argv[1:]
    ttype = "web_application"
    if "--type" in args:
        ttype = args[args.index("--type") + 1]
        args = [a for i, a in enumerate(args)
                if a not in ("--type",) and i != args.index("--type") + 1]
        ttype = ALIASES.get(ttype, ttype)
    if ttype not in EFFECTIVENESS:
        print(f"未知目标类型: {ttype}\n可选: {', '.join(EFFECTIVENESS)}", file=sys.stderr)
        return 2

    try:
        conf = float(args[0])
    except ValueError:
        print(f"confidence 必须是数字，收到: {args[0]}", file=sys.stderr)
        return 2
    if not 0 < conf <= 1:
        print("confidence 应在 (0, 1]", file=sys.stderr)
        return 2

    table = EFFECTIVENESS[ttype]
    print(f"# target_type={ttype}  confidence={conf}")
    chain, est = 1.0, 0
    for tool in args[1:]:
        p = table.get(tool, DEFAULT_EFF) * conf
        t = TIMES.get(tool, DEFAULT_TIME)
        if tool not in table:
            print(f"#   警告: {tool} 在该类型下无评分，用默认 {DEFAULT_EFF}", file=sys.stderr)
        chain *= p
        est += t
        print(f"{tool:22s} p={p:.3f}  t={t}s")
    print(f"{'chain':22s} P={chain:.6f}  est={est}s ({est/60:.1f}min)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

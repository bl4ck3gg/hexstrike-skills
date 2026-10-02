#!/usr/bin/env python3
"""nmap XML -> JSON 端口表

用法:
    nmap_xml.py <nmap.xml>            # 输出 JSON 数组
    nmap_xml.py <nmap.xml> --tsv      # 输出 TSV (port/state/service)

只做正则抽取，不依赖 libnmap。
"""
import json
import re
import sys

PORT_RE = re.compile(
    r'<port protocol="\w+" portid="(\d+)">'
    r'.*?<state state="(\w+)"'
    r'.*?<service name="([^"]*)"',
    re.S,
)


def parse(path: str) -> list:
    with open(path, encoding="utf-8", errors="replace") as fh:
        xml = fh.read()
    return [
        {"port": int(p), "state": s, "service": sv}
        for p, s, sv in PORT_RE.findall(xml)
    ]


def main(argv: list) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if len(argv) > 1 else 2
    rows = parse(argv[1])
    if "--tsv" in argv[2:]:
        for r in rows:
            print(f"{r['port']}\t{r['state']}\t{r['service']}")
    else:
        print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

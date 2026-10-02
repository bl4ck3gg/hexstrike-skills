#!/usr/bin/env python3
"""从混合输出里提取 JSON（stdout 或文件）

用法:
    json_extract.py < out.txt           # 从 stdin
    json_extract.py out.txt             # 从文件
    json_extract.py out.txt --compact   # 不缩进

用途：工具输出前面带 ANSI/提示符噪声时，抓第一个完整 JSON 对象并格式化。
"""
import json
import re
import sys

ANSI_RE = re.compile(r"\x1B\[[0-9;]*[mK]")


def extract(text: str):
    text = ANSI_RE.sub("", text)
    # 优先整个文本就是一个 JSON
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    # 退化：抓第一个 {...} 或 [...] 块（贪婪，让 json.loads 自己报错更准）
    for pattern in (r"\{.*\}", r"\[.*\]"):
        m = re.search(pattern, text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                continue
    return None


def main(argv: list) -> int:
    args = [a for a in argv[1:] if not a.startswith("-")]
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0

    if args:
        with open(args[0], encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
    else:
        raw = sys.stdin.read()

    data = extract(raw)
    if data is None:
        print("未找到可解析的 JSON", file=sys.stderr)
        return 1
    indent = None if "--compact" in argv else 2
    print(json.dumps(data, indent=indent, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

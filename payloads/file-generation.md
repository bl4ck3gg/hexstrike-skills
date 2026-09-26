---
name: payload-file-generation
description: 二进制测试载荷文件生成（buffer / cyclic / random）与校验
when_to_use: 需要超长输入、溢出偏移模式或随机数据文件
---
# 载荷文件生成

产物统一落 `$RUN/artifacts/`，命名 `payload_<type>_<size>.bin`；
服务端 `/api/payloads/generate` 上限 **100MB**，超限拒绝。

## buffer（重复模式）
```bash
SIZE=1024; PATTERN=A
python3 -c "import sys;p=sys.argv[1];n=int(sys.argv[2]);sys.stdout.write(p*(n//len(p)))" "$PATTERN" "$SIZE" \
  > $RUN/artifacts/payload_buffer_$SIZE.bin
wc -c $RUN/artifacts/payload_buffer_$SIZE.bin
```

## cyclic（溢出偏移定位）
```bash
# 真 cyclic（pwntools，推荐；4/8 字节窗口内唯一，可用于精确 offset）
python3 -c "from pwn import cyclic;open('$RUN/artifacts/payload_cyclic_1024.bin','wb').write(cyclic(1024))"
# 崩溃时 EIP/RIP 值反查偏移
python3 -c "from pwn import cyclic_find;print(cyclic_find(0x61616168))"   # 32 位
python3 -c "from pwn import cyclic_find;print(cyclic_find(0x6161616161616168))"  # 64 位
```
注意：HexStrike 服务端 `/api/payloads/generate` 的 `cyclic` 只是 **A-Z 循环**，
窗口不唯一，**不能用于 offset 定位**，仅适合占位/长度测试；要精确定位用上面的 pwntools 版本。

## random
```bash
head -c 1024 /dev/urandom > $RUN/artifacts/payload_random_1024.bin
# 可打印随机（用于文本型输入）
python3 -c "import random,string;print(''.join(random.choices(string.ascii_letters+string.digits,k=1024)))" \
  > $RUN/artifacts/payload_random_1024.txt
```

## 使用
```bash
# 本地二进制
gdb -q ./vuln -ex 'run < '"$RUN"'/artifacts/payload_cyclic_1024.bin'
# 网络
HOST='<target>'; PORT='<port>'
nc -w3 "$HOST" "$PORT" < $RUN/artifacts/payload_buffer_1024.bin
# HTTP
curl -sSk --data-binary @$RUN/artifacts/payload_buffer_1024.bin '<url>'
```
大文件不要 `cat` 到终端（会被截断/转义）；用 `wc -c`、`xxd | head` 校验。

## 记账
- 偏移定位成功：`add_finding high binary_offset "EIP offset=<n>" <target> pwntools "cyclic=<n>"`
- 只生成了载荷、未验证：记 info，不写成漏洞。
- CTF Pwn 流程见 `ctf/pwn.md`，模板见 `payloads/exploit-templates.md`。

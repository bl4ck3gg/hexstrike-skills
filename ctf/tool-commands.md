---
name: ctf-tool-commands
description: CTF 150+ 工具命令模板
when_to_use: 需要 CTF 专用工具命令
---
# CTF 工具命令表

## Web
httpx: `httpx -probe -tech-detect -status-code -title -content-length`
katana: `katana -depth 3 -js-crawl -form-extraction -headless`
sqlmap: `sqlmap --batch --level 3 --risk 2 --threads 5`
dalfox: `dalfox url --mining-dom --mining-dict --deep-domxss`
gobuster: `gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt,js`
dirsearch: `dirsearch -u {} -e php,html,js,txt,xml,json -t 50`
feroxbuster: `feroxbuster -u {} -w ... -x php,html,js,txt`
arjun: `arjun -u {} --get --post`
paramspider: `paramspider -d {}`
wpscan: `wpscan --url {} --enumerate ap,at,cb,dbe`
nikto: `nikto -h {} -C all`
whatweb: `whatweb -v -a 3`

## Crypto
hashcat: `hashcat -m 0 -a 0 --potfile-disable --quiet`
john: `john --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5`
hash-identifier: `hash-identifier`
hashid: `hashid -m`
cipher-identifier: `python3 /opt/cipher-identifier/cipher_identifier.py`
factordb: `python3 /opt/factordb/factordb.py`
rsatool: `python3 /opt/rsatool/rsatool.py`
yafu: `yafu`
sage: `sage -python`
openssl: `openssl`
gpg: `gpg --decrypt`
steganography: `stegcracker`
frequency-analysis: `python3 /opt/frequency-analysis/freq_analysis.py`
substitution-solver: `python3 /opt/substitution-solver/solve.py`
vigenere-solver: `python3 /opt/vigenere-solver/vigenere.py`
base64: `base64 -d`
base32: `base32 -d`
hex: `xxd -r -p`
rot13: `tr 'A-Za-z' 'N-ZA-Mn-za-m'`

## Pwn
checksec: `checksec --file`
pwntools: `python3 -c 'from pwn import *'`
ropper: `ropper --file {} --search`
ropgadget: `ROPgadget --binary`
one-gadget: `one_gadget`
gdb-peda: `gdb -ex 'source /opt/peda/peda.py'`
gdb-gef: `gdb -ex 'source /opt/gef/gef.py'`
gdb-pwngdb: `gdb -ex 'source /opt/Pwngdb/pwngdb.py'`
angr: `python3 -c 'import angr'`
radare2: `r2 -A`
ghidra: `analyzeHeadless /tmp ghidra_project -import`
ltrace: `ltrace`
strace: `strace -f`
objdump: `objdump -d -M intel`
readelf: `readelf -a`
nm: `nm -D`
ldd: `ldd`
file: `file`
strings: `strings -n 8`
hexdump: `hexdump -C`
pwninit: `pwninit`
libc-database: `python3 /opt/libc-database/find.py`

## Forensics
binwalk: `binwalk -e --dd='.*'`
foremost: `foremost -i {} -o /tmp/foremost_output`
photorec: `photorec /log /cmd`
testdisk: `testdisk /log`
exiftool: `exiftool -all`
steghide: `steghide extract -sf {} -p ''`
stegsolve: `java -jar /opt/stegsolve/stegsolve.jar`
zsteg: `zsteg -a`
outguess: `outguess -r`
jsteg: `jsteg reveal`
volatility: `volatility -f {} imageinfo`
volatility3: `python3 /opt/volatility3/vol.py -f`
rekall: `rekall -f`
wireshark: `tshark -r`
tcpdump: `tcpdump -r`
autopsy: `autopsy`
sleuthkit: `fls -r`
scalpel: `scalpel -c /etc/scalpel/scalpel.conf`
bulk-extractor: `bulk_extractor -o /tmp/bulk_output`

## Rev
ida: `ida64`
ida-free: `ida64 -A`
retdec: `retdec-decompiler`
upx: `upx -d`
peid: `peid`
detect-it-easy: `die`
x64dbg: `x64dbg`
ollydbg: `ollydbg`
apktool: `apktool d`
jadx: `jadx`
dex2jar: `dex2jar`
jd-gui: `jd-gui`
dnspy: `dnspy`
ilspy: `ilspy`

## OSINT
sherlock: `sherlock`
social-analyzer: `social-analyzer`
theHarvester: `theHarvester -d {} -b all`
recon-ng: `recon-ng`
spiderfoot: `spiderfoot`
shodan: `shodan search`
censys: `censys search`
whois: `whois`
dig: `dig`
dnsrecon: `dnsrecon -d`
fierce: `fierce -dns`
sublist3r: `sublist3r -d`
amass: `amass enum -d`
subfinder: `subfinder -d`

## Misc
qr-decoder: `zbarimg`
audio-analysis: `audacity`
spectrum-analyzer: `python3 /opt/spectrum-analyzer/analyze.py`
brainfuck: `python3 /opt/brainfuck/bf.py`
whitespace: `python3 /opt/whitespace/ws.py`
piet: `python3 /opt/piet/piet.py`
malbolge: `python3 /opt/malbolge/malbolge.py`
zip: `unzip -P`
7zip: `7z x -p`
rar: `unrar x -p`
tar: `tar -xf`
gzip: `gunzip`
bzip2: `bunzip2`
xz: `unxz`

## 现代 Web
jwt-tool: `python3 /opt/jwt_tool/jwt_tool.py`
jwt-cracker: `jwt-cracker`
postman: `newman run`
burpsuite: `java -jar /opt/burpsuite/burpsuite.jar`
owasp-zap: `zap.sh -cmd`
websocket-king: `python3 /opt/websocket-king/ws_test.py`

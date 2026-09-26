---
name: technology-signatures
description: 技术指纹识别
when_to_use: 需针对特定技术选工具
---
# 技术指纹

## Header
Apache: Apache/apache | Nginx: nginx/Nginx | IIS: Microsoft-IIS | PHP: PHP/X-Powered-By: PHP | Node.js: Express | Python: Django/Flask/Werkzeug | Java: Tomcat/JBoss/WebLogic | .NET: ASP.NET/X-AspNet-Version

## Content
WordPress: wp-content/wp-includes | Drupal: /sites/default | Joomla: /administrator | React: __REACT_DEVTOOLS | Angular: ng-version | Vue: __VUE__

## Port
Apache: 80,443,8080,8443 | Nginx: 80,443,8080 | IIS: 80,443,8080 | Node.js: 3000,8000,8080,9000

## 联动
- WordPress → gobuster -x php,html,txt,xml + wpscan
- PHP → gobuster -x php,php3,php4,php5,phtml; sqlmap --dbms=mysql
- .NET → gobuster -x aspx,asp; sqlmap --dbms=mssql
- WAF 检测到 → 强制 stealth(threads≤5, delay≥2s)

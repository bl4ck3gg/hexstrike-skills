---
name: tech-detection
when_to_use: 从 header/content/port 识别技术
---
# 技术检测
## web_servers
apache: Apache/apache/httpd | nginx: nginx/Nginx | iis: Microsoft-IIS/IIS | tomcat: Tomcat/Apache-Coyote | jetty: Jetty | lighttpd: lighttpd
## frameworks
django: Django/csrftoken | flask: Flask/Werkzeug | express: Express | laravel: Laravel/laravel_session | symfony: Symfony | rails: Ruby on Rails/_session_id | spring: Spring/JSESSIONID | struts: Struts
## cms
wordpress: wp-content/wp-includes//wp-admin/ | drupal: Drupal//sites/default/ | joomla: Joomla//administrator/ | magento: Magento/Mage.Cookies | prestashop: PrestaShop | opencart: OpenCart
## databases
mysql: MySQL/phpMyAdmin | postgresql: PostgreSQL | mssql: Microsoft SQL Server/MSSQL | oracle: Oracle | mongodb: MongoDB | redis: Redis
## languages
php: PHP/.php | python: Python/.py | java: Java/.jsp/.do | dotnet: ASP.NET/.aspx | nodejs: Node.js/.js | ruby: Ruby/.rb
## security
waf: cloudflare/X-CF-Ray/incapsula/sucuri | load_balancer: F5/BigIP/HAProxy/AWS-ALB | cdn: CloudFront/Fastly/KeyCDN/Cloudflare
## port_services
21=ftp 22=ssh 23=telnet 25=smtp 53=dns 80=http 110=pop3 143=imap 443=https 993=imaps 995=pop3s 1433=mssql 3306=mysql 5432=postgresql 6379=redis 27017=mongodb 8080=http-alt 8443=https-alt 9200=elasticsearch 11211=memcached

## 参数联动
apache → gobuster -x php,html,txt,xml,conf; nuclei +apache
nginx → gobuster -x php,html,txt,json,conf; nuclei +nginx
wordpress → gobuster -x php,html,txt,xml; wpscan --enumerate ap,at,cb,dbe
php → gobuster -x php,php3,php4,php5,phtml,html; sqlmap --dbms=mysql
dotnet → gobuster -x aspx,asp,html,txt; sqlmap --dbms=mssql

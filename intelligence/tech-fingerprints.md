---
name: tech-fingerprints
description: 技术指纹表与参数联动
when_to_use: 识别技术栈并据此调参
---
# 技术指纹（识别规则）

## 检测模式（大小写不敏感；匹配 header 名/值与 body）
```
web_servers: apache[Apache,apache,httpd] nginx[nginx,Nginx] iis[Microsoft-IIS,IIS]
             tomcat[Tomcat,Apache-Coyote] jetty[Jetty] lighttpd[lighttpd]
frameworks:  django[Django,django,csrftoken] flask[Flask,Werkzeug]
             express[Express,X-Powered-By: Express] laravel[Laravel,laravel_session]
             symfony[Symfony,symfony] rails[Ruby on Rails,rails,_session_id]
             spring[Spring,JSESSIONID] struts[Struts,struts]
cms:         wordpress[wp-content,wp-includes,WordPress,/wp-admin/]
             drupal[Drupal,drupal,/sites/default/,X-Drupal-Cache]
             joomla[Joomla,joomla,/administrator/,com_content]
             magento[Magento,magento,Mage.Cookies]
             prestashop[PrestaShop,prestashop] opencart[OpenCart,opencart]
databases:   mysql[MySQL,mysql,phpMyAdmin] postgresql[PostgreSQL,postgres]
             mssql[Microsoft SQL Server,MSSQL] oracle[Oracle,oracle]
             mongodb[MongoDB,mongo] redis[Redis,redis]
languages:   php[PHP,php,.php,X-Powered-By: PHP] python[Python,python,.py]
             java[Java,java,.jsp,.do] dotnet[ASP.NET,.aspx,.asp,X-AspNet-Version]
             nodejs[Node.js,node,.js] ruby[Ruby,ruby,.rb] go[Go,golang] rust[Rust,rust]
security:    waf[cloudflare,CloudFlare,X-CF-Ray,incapsula,Incapsula,sucuri,Sucuri]
             load_balancer[F5,BigIP,HAProxy,nginx,AWS-ALB]
             cdn[CloudFront,Fastly,KeyCDN,MaxCDN,Cloudflare]
```

## 端口 → 服务
```
21 ftp | 22 ssh | 23 telnet | 25 smtp | 53 dns | 80 http | 110 pop3 | 143 imap
443 https | 993 imaps | 995 pop3s | 1433 mssql | 3306 mysql | 5432 postgresql
6379 redis | 27017 mongodb | 8080 http-alt | 8443 https-alt
9200 elasticsearch | 11211 memcached
```

## 采集命令（直接执行）
```bash
URL='<url>'
curl -sSk -D $RUN/raw/headers.txt -o $RUN/raw/body.html "$URL"
cat $RUN/raw/headers.txt
# 指纹匹配（示例：把命中的都打出来）
grep -oiE 'apache|nginx|Microsoft-IIS|Tomcat|Django|Flask|Express|Laravel|Symfony|Rails|Spring|Struts' $RUN/raw/headers.txt $RUN/raw/body.html | sort -u
grep -oiE 'wp-content|wp-includes|Drupal|Joomla|Magento|PrestaShop|OpenCart' $RUN/raw/body.html | sort -u
grep -oiE 'cloudflare|x-cf-ray|incapsula|sucuri' $RUN/raw/headers.txt | sort -u
# 有 httpx 时更快
httpx -u "$URL" -tech-detect -sc -title -server -silent
```
写 `parsed/tech.json`：`{"web_servers":[],"frameworks":[],"cms":[],"databases":[],
"languages":[],"security":[],"services":[]}`。

## 参数联动 `_apply_technology_optimizations`
```
apache    -> gobuster -x php,html,txt,xml,conf ; nuclei -tags apache
nginx     -> gobuster -x php,html,txt,json,conf ; nuclei -tags nginx
wordpress -> gobuster -x php,html,txt,xml + /wp-content/,/wp-admin/,/wp-includes/
             nuclei -tags wordpress ; wpscan --enumerate ap,at,cb,dbe
php       -> gobuster -x php,php3,php4,php5,phtml,html ; sqlmap --dbms=mysql
dotnet    -> gobuster -x aspx,asp,html,txt            ; sqlmap --dbms=mssql
WAF(cloudflare/incapsula/sucuri)
          -> 强制 stealth: gobuster -t 5 --delay 2s ; sqlmap --delay 2 --randomize
```

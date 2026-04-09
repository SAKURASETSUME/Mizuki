---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - URLRewrite 伪静态配置"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

**URLRewrite 能够隐藏服务器的真实地址**

```bash
rewrite是实现URL重写的关键指令，根据regex（正则表达式）部分内容，重定向到replacement，结尾是flag标记。
rewrite   <regex>   <replacement>  [flag];
关键字      正则       替代内容       flag标记
关键字：其中关键字error_log不能改变
正则：perl兼容正则表达式语句进行规则匹配
替代内容：将正则匹配的内容替换成replacement
flag标记：rewrite持的flag标记


rewrite参数的标签段位置：
server,location,if

flag标记说明：
1ast #本条规则匹配完成后，继续向下匹配新的location URI规则
break #本条规则匹配完成即终止，不再匹配后面的任何规则
redirect #返回302临时重定向，浏览器地址会显示跳转后的URL地址
permanent #返回301永久重定向，浏览器地址栏会显示跳转后的uRL地址
```

```bash
server {
        listen       80;
        server_name  www.nakatsusizuru.top nakatsusizuru.top;
        #charset koi8-r;
        #access_log  logs/host.access.log  main;
        location / {
        #伪静态配置 比如url是www.jd.com/index.jsp?pageNum=2111 那么这个rewrite的配置就是用了正则匹配的方式 把后面的URI换成2111.html 在你访问www.jd.com/2111.html的时候 实际的后端地址是www.jd.com/index.jsp?pageNum=2111
        
         rewrite ^/([0-9]+).html$      /index.jsp?pageNum=$1 break;
            proxy_pass http://192.168.24.52:8080;
        }

#用正则匹配 一个location配置能够配置多个静态资源文件夹 防止配置文件过长
        location ~*/(js|img|css) {
            root   html;
            index  index.html index.htm;
        }
        
        #error_page  404              /404.html;

  

        # redirect server error pages to the static page /50x.html

        #

        error_page   500 502 503 504  /50x.html;

        location = /50x.html {

            root   html;

        }

  

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80

        #

        #location ~ \.php$ {

        #    proxy_pass   http://127.0.0.1;

        #}

  

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000

        #

        #location ~ \.php$ {

        #    root           html;

        #    fastcgi_pass   127.0.0.1:9000;

        #    fastcgi_index  index.php;

        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;

        #    include        fastcgi_params;

        #}

  

        # deny access to .htaccess files, if Apache's document root

        # concurs with nginx's one

        #

        #location ~ /\.ht {

        #    deny  all;

        #}

    }
```
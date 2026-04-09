---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - 动静分离 - 基本配置"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

```bash
#最简单的动静分离配置
server {
        listen       80;
        server_name  www.nakatsusizuru.top nakatsusizuru.top;
        #charset koi8-r;
        #access_log  logs/host.access.log  main;
        location / {
            proxy_pass http://192.168.24.52:8080; #这一条就是把nginx反向代理到后端的tomcat服务器上了 当访问这台nginx服务器的80端口 或者上面配置过的域名的时候 就会代理到后端服务器上的8080端口 也就是tomcat的默认端口
            #root   /www/www;
            #index  index.html index.htm;
        }

#把css资源传到nginx服务器的root用户 /usr/local/nginx/html/css中 也就是默认页面的css目录中 再写一个location 就可以把静态资源代理到nginx服务器中 访问这个server中的80端口就可以展示静态资源 不需要去访问后端服务器了 图片 js同理
        location /css {
            root   html;
            index  index.html index.htm;
        }
  
        location /js {
            root   html;
            index  index.html index.htm;
        }
        
                location /img {
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

## 使用正则配置动静分离

```bash
server {
        listen       80;
        server_name  www.nakatsusizuru.top nakatsusizuru.top;
        #charset koi8-r;
        #access_log  logs/host.access.log  main;
        location / {
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
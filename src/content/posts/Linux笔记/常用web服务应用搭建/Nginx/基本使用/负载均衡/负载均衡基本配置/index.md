---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - 负载均衡 - 负载均衡基本配置"
category: "Linux笔记"
date: 2026-04-02
published: 2026-04-02
author: "Rin"
---

```bash
    #定义一组服务器

    upstream servertest {

        server 192.168.29.50:888;

        server 192.168.29.50:7777;

  

    }

  

    server {

        listen       80;

        server_name  www.nakatsusizuru.top nakatsusizuru.top;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

#代理这个服务器组的别名 当访问上述配置过的域名时 会根据某种算法来访问192.168.29.50:888和192.168.29.50:7777
            proxy_pass http://servertest;

            #root   /www/www;

            #index  index.html index.htm;

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

**这就是轮询的负载均衡方式 这种方式有个缺点就是无法保持会话 那么就会导致需要保存 需要登录及其它需要长时间保持会话才能实现的功能无法使用**
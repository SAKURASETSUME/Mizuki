---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - 负载均衡 - 基本概念 反向代理简单配置"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 服务器的集群

**集群就是 有一台服务器对应的功能 防止这个服务器出问题 备份了很多台和这台服务器一模一样的服务器备份 所有的服务器都有相同的功能 能够提供的服务完全一样 这群服务器就叫服务器集群**

## 负载均衡

**在一个服务器集群中有多台能提供完全相同的服务器 负载均衡就是能够实现把这个服务器集群中的服务器充分使用 让这个集群中的服务器同时工作(防止一台服务器负荷过高) 或者其中一台或多台服务器出问题时 可以快速地使用集群中的别的服务器提供完全相同的服务 这就是负载均衡**

## 反向代理到外网和内网主机的配置

```bash
#关键字：proxy_pass 这个和root关键字只能同时存在一个
server {

        listen       80;

        server_name  www.nakatsusizuru.top nakatsusizuru.top;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            proxy_pass http://www.baidu.com; #如果访问当前站点的根目录 就会访问到这个地址 比如这里就是访问192.168.29.52或者上面配过的域名 跳转到的是百度 这里只能访问http协议 不能访问https协议 因为要配置证书 如果要代理到内网另一台服务器上 可以这么写:http://192.168.29.50 

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
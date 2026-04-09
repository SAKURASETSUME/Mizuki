---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - 负载均衡 - 网关的概念 伪静态同时负载均衡"
category: "Linux笔记"
date: 2026-04-02
published: 2026-04-02
author: "Rin"
---

## 网关

**nginx的反向代理模型中 由于后端的静态资源是由nginx来代理的 那么有访问权限的人去访问后端一般是只能加载后端页面 而没有js css 图片等资源展示的 并且外网用户访问页面不是直接访问内网的后端服务器 而是访问nginx 再通过nginx访问后端服务器来进行交互 这时网页展示的静态资源是由nginx提供的 后端功能是由后端服务器提供的 这时候就称为nginx是后端的网关**

## 防火墙配置指定ip访问

```bash
#指定端口和ip访问
firewa11-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.44.101" port protocol="tcp" port="8080" accept"

#移除规则
firewa11-cmd --permanent --remove-rich-rule="rule family="ipv4" source address="192.168.44.101" port="8080" protocol="tcp" accept"

#查看配置过的所有规则
firewall-cmd --list-all
```

**这样配置完之后 处于外网的网络是访问不到后端服务器的 只有IP地址为192.168.44.101的机器才能访问到 这样可以模拟内网环境 方便测试**

## 伪静态的同时负载均衡

```bash
    #定义一组服务器

    #配置负载均衡器

    upstream servertest {

        server 192.168.29.52:888 weight=8;

        server 192.168.29.52:85 weight=2;

        server 192.168.29.52:8008 weight=3;

  

    }
    
 server {

            listen       80;

            server_name  www.nakatsusizuru.top nakatsusizuru.top;

  

            #charset koi8-r;

  

            #access_log  logs/host.access.log  main;

  

            location / {

                rewrite ~/([0-9]+).html$ /index.jsp?pageNum=$1 redirect;

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


**这时 这台nginx服务器上又有代理又有负载均衡 就被称作网关服务器**
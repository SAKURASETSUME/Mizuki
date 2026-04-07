---
title: "redirect server error pages to the static page /50x.html"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/基本配置/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```bash
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

  
#检测访问来源是不是24.52 如果是 就允许访问静态资源 如果来源是非法的 那么就返回403错误码
            location ~*/(js|img|css) {

                valid_referers nakatsusizuru.top;

                if ($invalid_referer) {

                return 403; #如果不想反回状态码 直接返回错误页面 那么把403改成页面路径就可以了 但是如果想要返回错误图片 不能用return写 要用rewrite来写

                }

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

#配置错误页面 当出现403错误的时候 返回默认html文件里的403.html页面
              error_page   403  /403.html;

            location = /403.html {

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


```bash
#如果想要返回一个错误图片 可以用rewrite来写
location ~*/(js|img|css) {

                valid_referers 192.168.24.52;

                if ($invalid_referer) {

                rewrite ^/  错误图片路径 break;

                }

                root   html;

                index  index.html index.htm;

            }
```
## 防盗链配置
```bash
valid_referers none | blocked | server_names | strings ....;

none，检测Referer头域不存在的情况。
blocked，检测 Referer 头域的值被防火墙或者代理服务器删除或伪装的情况。这种情况该头域的值不以"http://"或"https://"开头。
•server_names，设置一个或多个 URL，检测 Referer 头域的值是否是这些 URL 中的某一个。
```
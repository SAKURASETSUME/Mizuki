---
title: "基础配置"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/常用web服务应用搭建/Nginx/基本使用/基础配置/
categories:
  - Linux笔记
  - 常用web服务应用搭建
  - Nginx
  - 基本使用
  - 基础配置
tags:
  - Study
---

**/usr/local/nginx/conf/nginx.conf**

## 最小配置文件

**去除了默认配置所有注释 剩下的能保证nginx运行的最小配置**

```bash
worker_processes  1; #默认为1 表示工作的进程数 一般设置为服务器CPU的个数

events { #事件驱动模块
    worker_connections  1024; #一个进程的最大连接数
}

http {
    include       mime.types; #包含文件 把另外的配置文件引入到当前的配置文件中 mime.types是由服务器端向客户端(浏览器)返回文件类型的一个配置
    default_type  application/octet-stream; #默认类型  如果mime里面没写某个后缀对应的文件类型 就以这个默认的类型来解析

    sendfile        on; #数据0拷贝


    keepalive_timeout  65; #超时

#虚拟主机 vhost
    server {
        listen       80; #当前主机的监听端口号
        server_name  localhost; #主机的主机名 也可以拿来配置域名

# http://AAA.com/aaa/index.html -> URI 即AAA.com后面的路径
        location / { #匹配URI
        #找哪个目录下的html
            root   html; #html是相对路径 是nginx文件里的html
            index  index.html index.htm; #默认页
        }


#跳转到http://AAA.com/50x.html
        error_page   500 502 503 504  /50x.html; #如果发生服务器端错误的时候 展示的页面

#如果发生服务器端错误了 需要展示50x.html页面 从root下的html文件里面找
        location = /50x.html {
            root   html;

        }

    }

}
```

## ServerName的多种匹配方式

- 我们可以在同一servername中匹配多个域名

```bash
 server {

        listen       80;

        server_name  www.nakatsusizuru.top nakatsusizuru.top;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            root   /www/www;

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

  

   server {

        listen       80;

        server_name  nakatsusizuru.top;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            root   /www/www;

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

  

server {

        listen       80;

        server_name  video.nakatsusizuru.top;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            root   /www/video;

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
    
    #在这个配置文件中 优先生效的是写在前面的配置 如果你要多个域名指向同一个主机监听的同一个端口 完全可以只写一个server 只需要在servername这个配置下多配置几个域名就行了
```

- 完整匹配
- 通配符匹配

```bash
 server {

        listen       80;

        server_name  www.nakatsusizuru.top nakatsusizuru.top;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            root   /www/www;

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

server {

        listen       80;

        server_name  *.nakatsusizuru.top;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            root   /www/video;

            index  index.html index.htm;

        }

  

        #error_page  404              /404.html;

  

        # redirect server error pages to the static page /50x.html

        #

        error_page   500 502 503 504  /50x.html;

        location = /50x.html {

            root   html;

        }
        #用通配符来匹配 除了www. 和不带二级域名的域名 全部访问video目录
```

- 通配符结束匹配

```bash
server {

        listen       80;

        server_name  www.nakatsusizuru.top;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            root   /www/video;

            index  index.html index.htm;

        }

  

        #error_page  404              /404.html;

  

        # redirect server error pages to the static page /50x.html

        #

        error_page   500 502 503 504  /50x.html;

        location = /50x.html {

            root   html;

        }
        
server {

        listen       80;

        server_name  www.nakatsusizuru.*;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            root   /www/video;

            index  index.html index.htm;

        }

  

        #error_page  404              /404.html;

  

        # redirect server error pages to the static page /50x.html

        #

        error_page   500 502 503 504  /50x.html;

        location = /50x.html {

            root   html;

        }
        
        #除了顶级域名是.top的 其它域名为www.nakatsusizuru.的任何顶级域名都匹配到video目录
```

- 正则匹配

```bash
server {

        listen       80;

        server_name  ~^[0-9]+\.nakatsusizuru\.top$;

  

        #charset koi8-r;

  

        #access_log  logs/host.access.log  main;

  

        location / {

            root   /www/video;

            index  index.html index.htm;

        }

  

        #error_page  404              /404.html;

  

        # redirect server error pages to the static page /50x.html

        #

        error_page   500 502 503 504  /50x.html;

        location = /50x.html {

            root   html;

        }
        
        #以数字为二级域名的匹配到video目录下
```
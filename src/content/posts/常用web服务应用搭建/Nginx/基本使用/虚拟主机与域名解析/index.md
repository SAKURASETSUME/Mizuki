---
title: "redirect server error pages to the static page /50x.html"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/虚拟主机与域名解析/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 配置域名解析

**买个域名 目前最大的厂商是阿里云 比较靠谱**

**在线配置的时候 把记录值指向你域名要解析的ip就行**

**配置的时候支持正则匹配 如果要批量添加的时候可以用通配符`*` 来匹配 这个就是泛解析**

## 配置个站点

```bash
#先配置目录
cd /
mkdir www
mkdir www #主站
mkdir video #视频站点

cd video
vim index.html #创建主页面
#写入
this is video web site

cd ..
cd www
vim index.html
#写入
this is www web site.

#修改配置文件
cd /usr/local/nginx/conf

#修改
#这是第一个站点 监听的80端口 访问的是根目录下 www文件夹中的www文件夹里的index.html
server {

        listen       80;#如果下面的域名是localhost 这里的监听端口就要修改成别的端口来区分站点
#域名 主机名 如果修改了这一项 监听的端口就改回80 直接用域名访问就可以了
        server_name  www.nakatsusizuru.com;

  

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

  
  
  
#这是第二个站点 监听的是81端口 访问的是根目录下的www目录中的video目录的index.html
server {

        listen       80; #如果下面的域名是localhost 这里的监听端口就要修改成别的端口来区分站点
#域名 主机名 如果修改了这一项 监听的端口就改回80 直接用域名访问就可以了
        server_name  video.nakatsusizuru.com;

  

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
   
   #这是第三个站点 配置的是nakatsusizuru.com的域名 防止用户不写三级域名来访问 如果不配置这一条 那么用户访问nakatsusizuru.com的时候访问的就是nginx的默认页面了
server {

        listen       80; #如果下面的域名是localhost 这里的监听端口就要修改成别的端口来区分站点
#域名 主机名 如果修改了这一项 监听的端口就改回80 直接用域名访问就可以了
        server_name  nakatsusizuru.com;

  

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
   
#修改后重启nginx 防火墙开放81端口生效配置
systemctl restart nginx
firewall-cmd --permanent --add-port=81/tcp
firewall-cmd --reload

#访问域名 这里我使用的是自己的公网域名
www.nakatsusizuru.top #显示页面为this is www web site.
nakatsusizuru.top #显示页面为this is www web site.
nakatsusizuru.top:81 #显示页面为this is video web site.
```
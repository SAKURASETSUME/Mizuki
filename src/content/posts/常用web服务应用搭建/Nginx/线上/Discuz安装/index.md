---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/discuz安装/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

```bash
#将discuz压缩包传到nginx的html目录下
unzip Discuz_X3.5_SC_UTF8_20250901.zip

#把源码目录改个名
mv upload/ bbs

#

#打开站点 在线安装 注意一下 如果你装了证书 那么https默认访问的是443端口 这个在线安装你要访问80端口才生效 要去配置文件把80端口关于文件解析的配置都放到443的server下(从默认目录下面开始都是) 之后把访问80端口的请求跳转到访问443端口 这个协议跳转要写到80端口
#http协议跳转https协议
return 301 https://$server_name$request_uri;

#reload一下nginx

#访问
nakatsusizuru.top/bbs
#会发现目录权限有问题 可以自己改一下(以下仅为测试用 实际生产环境不要上777)
cd html
chmod -R 777 bbs/
```

```bash
#nginx配置
 87 server {
 88 listen 443 ssl;
 89 server_name localhost;#这个域名自己配置也可以
 90 
 91 ssl_certificate www.nakatsusizuru.top.pem;
 92 ssl_certificate_key www.nakatsusizuru.top.key;
 93 
 94     index index.html index.htm index.php;
 95     #error_page 404 /404.html;
 96     #error_page 502 /502.html;
 97     location /nginx_status {
 98       stub_status on;
 99       access_log off;
100       allow 127.0.0.1;
101       deny all;
102     }
103     location ~ [^/]\.php(/|$) {
104       #fastcgi_pass remote_php_ip:9000;
105       fastcgi_pass unix:/dev/shm/php-cgi.sock;
106       fastcgi_index index.php;
107       include fastcgi.conf;
108       # 如果需要限制并发连接，可以取消注释以下代码
109       #limit_conn addr 10;
110       #limit_conn_status 503;
111       #limit_conn_log_level error;
112     }
113     location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|flv|mp4|ico)$ {
114       expires 30d;
115       access_log off;
116     }
117     location ~ .*\.(js|css)?$ {
118       expires 7d;
119       access_log off;
120     }
121     location ~ ^/(\.user.ini|\.ht|\.git|\.svn|\.project|LICENSE|README.md) {
122       deny all;
123     }
124     location /.well-known {
125       allow all;
126     }
127 }
128 
129 server {
130     listen 80;
131     server_name _;
132     access_log /data/wwwlogs/access_nginx.log combined;
133     return 301 https://$server_name$request_uri;
134     root html;
135   }
136 ######################### vhost #############################
137   include vhost/*.conf;
138 }
```
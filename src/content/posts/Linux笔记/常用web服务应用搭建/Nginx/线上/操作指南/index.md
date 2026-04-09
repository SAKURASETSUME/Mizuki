---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 线上 - 操作指南"
category: "Linux笔记"
date: 2026-04-06
published: 2026-04-06
author: "Rin"
---

**L(linux)N(nginx)M(mysql)P(php)版本 集成了基本的运行环境**

**集成环境一键安装推荐：oneinstck.com**

**阿里云控制台的安全组就可以配置防火墙(配置规则)**

**配置Nginx默认页**

```bash
cd /usr/local/nginx/conf

vim nginx.conf

#找到80端口的监听server 之后把默认目录改了

#重启nginx
systemctl restart nginx
```

**申请证书**

```txt
在阿里云就能申请
在SSL证书里面申请就行
```

**把证书配置到Nginx**

```txt
把证书对应自己服务器web服务版本下载下来 之后传到服务器nginx的conf目录下
```

```bash
#nginx证书配置 配到nginx.conf里
server {
listen 443 ssl;
server_name localhost;#这个域名自己配置也可以

ssl_certificate /data/cert/server.crt;#绝对路径 按照你自己的路径去写 上面传到了nginx的conf目录下 用相对路径直接写名字也可以
ssl_certificate_key /data/cert/server.key; 

}

#重启nginx
systemctl restart nginx

#访问的时候用https就能知道配没配好了
```
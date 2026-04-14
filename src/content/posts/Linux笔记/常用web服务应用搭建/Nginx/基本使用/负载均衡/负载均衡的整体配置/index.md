---
title: "Linux笔记 - 常用web服务应用搭建 - Nginx - 基本使用 - 负载均衡 - 负载均衡的整体配置"
category: "Linux笔记"
date: 2026-04-14
published: 2026-04-14
author: "Rin"
---

```bash
#定义服务器集群
upstream httpserver{
server 192.168.29.50:80;
server 192.168.29.51:80;
}

upstream phpserver{
server 192.168.29.52:80;
server 192.168.29.53:80;
}

upstream staticserver{
server 192.168.29.54:80;
server 192.168.29.55:80;
}

#定位网站目录
location / {
proxy_pass http://httpserver;
}

location ~ \.html${
proxy_pass http://httpserver; #代理推送 这里填服务器集群
}

location ~ \.php${
proxy_pass http://phpserver;
}

location ~ \.(jpg|png|css|js)${
proxy_pass http://staticserver;
}
```
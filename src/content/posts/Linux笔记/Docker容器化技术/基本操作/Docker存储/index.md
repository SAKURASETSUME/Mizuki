---
title: "Linux笔记 - Docker容器化技术 - 基本操作 - Docker存储"
category: "Linux笔记"
date: 2026-04-14
published: 2026-04-14
author: "Rin"
---

## 目录挂载
```bash
#把Docker Host的/app/nghtml挂载到nginx容器里的/usr/share/nginx/html
docker run -d -p 80:80 --name nginx -v /app/nghtml:/usr/share/nginx/html mynginx:v1.0

#在Docker Host的对应目录下直接写index.html就可以了 并且不担心Docker炸了之后 数据会丢失
```

## 卷映射
```bash
#把/etc/nginx里的文件都映射到ngconf卷中 这个卷统一存储在/var/lib/docker/volumes/<volume-name>中 想要修改的话在这里改就行
docker run -d -p 80:80 --name nginx -v /app/nghtml:/usr/share/nginx/html -v ngconf:/etc/nginx mynginx:v1.0

#列出所有的卷
docker volume ls
#创建一个卷
docker volume create aaa
#查看卷的详情
docker volume inspect ngconf
```
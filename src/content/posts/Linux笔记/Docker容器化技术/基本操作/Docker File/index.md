---
title: "Linux笔记 - Docker容器化技术 - 基本操作 - Docker File"
category: "Linux笔记"
date: 2026-04-14
published: 2026-04-14
author: "Rin"
---

## 制作镜像
```bash
#从本机随便找个jar包传上去
#编写Docker File文件
vim Dockerfile

#写入
FROM openjdk:17 #指定镜像基础环境 这里也可以直接下一个OS


LAVEL author=RIN #一些标签

COPY app.jar /app.jar #文件在镜像内的位置

EXPOSE 8080 #指定暴露的端口

ENTRYPOINT ["java","-jar","/app.jar"] #容器固定启动命令


#构建镜像
docker build -f Dockerfile -t myjavaapp:v1.0 .
#直接启动
docker -d -p 8888:8080 myjavaapp:v1.0
```

## 镜像分层存储机制
DockerFile是分层存储的 每一行命令都独占一层
这样存储有一个好处：镜像基础环境和你的修改互不相干并且节省空间 假如你有两个nginx 一个是官方的 一个是你自己的v1.0 那么这两个nginx占的空间大小并不是nginx\*2 而是nginx+你v1.0新增的内容大小

```bash
#可以看一下
#启动两个nginx 
docker run -p 80:80 -d --name nginx -v /app/nghtml/:/usr/share/nginx/html nginx
docker run -p 8080:80 -d --name nginx2 nginx

#把被改过的nginx保存一下
docker commit -m "update index" nginx mynginx:v1.0

#查看镜像详情
docker image inspect mynginx:v1.0
docker image inspect nginx
#可以看到 mynginx的Layer是多了一层的
#再去看占用空间
docker ps -s #可以看到 实际占用的只有新增空间 括号里的是镜像空间 本来就是存在系统硬盘里的

```
---
title: "Linux笔记 - Docker容器化技术 - 基本操作 - Docker Compose"
category: "Linux笔记"
date: 2026-04-14
published: 2026-04-14
author: "Rin"
---

## 什么是Docker Compose?
Docker Compose是容器的**批量管理**工具
## 使用
```bash
#首先准备一个yaml文件 之后把所有你要启动的容器配置文件都写到这里
#批量上线
docker compose up -d
#批量下线
docker compose down
#或者指定启动的容器
docker compose start x1 x2 x3
#上线和start的区别：上线是第一次创建应用并启动 start就是启动已经上线过的容器

#停止
docker stop x1 x2
#扩容 让某个应用的实例启动3份
docker compose scale x2=3
```

## 测试
```bash
#安装wordpress
#基础的写法
#先创建一个自定义网络
docker network create blog
#安装mysql
docker run -d -p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=123456 \
-e MYSQL_DATABASE=wordpress \
-v mysql-data:/var/liv/mysql \
-v /app/myconf:/etc/mysql/conf.d \
--restart always --name mysql \
--network blog \
mysql:8.0

#安装wordpress
docker run -d -p 8080:80 \
-e WORDPRESS_DB_HOST=mysql \
-e WORDPRESS_DB_USER=root \
-e WORDPRESS_DB_PASSWORD=123456 \
-e WORDPRESS_DB_NAME=wordpress \
-v wordpress:/var/www/html \
--restart always --name wordpress-app \
--network blog \
wordpress:latest

#使用Docker Compose
#编写compose.yaml
name: myblog

services:

    mysql:

    container_name: mysql

        image: mysql:8.0

        ports:

            - "3306:3306"

        environment:

            - MYSQL_ROOT_PASSWORD=123456

            - MYSQL_DATABASE=worepress

        volumes:

            - mysql-data:/var/lib/mysql

            - /app/myconf:/etc/mysql/conf.d

        restart:always

        networks:

            - blog

  

    wordpress:

    container_name: wordpress-app

        image: wordpress-app

        ports:

            - "8080:80"

        environment:

            - WORDPRESS_DB_HOST=mysql

            - WORDPRESS_DB_USER=root

            - WORDPRESS_DB_PASSWORD=123456

            - WORDPRESS_DB_NAME=wordpress

        volumes:

            - wordpress:/var/www/html

        restart:always

        networks:

            - blog

        depens_on:

            - mysql

  

volumes:

    mysql-data:

    wordpress:

  

networks:

    blog:
    
 #启动
 docker compose -f compose.yaml up -d
 #一键删除所有环境
 docker compose down --rmi all -v
```

**yaml语法参考:[Compose file reference | Docker Docs](https://docs.docker.com/reference/compose-file/)**
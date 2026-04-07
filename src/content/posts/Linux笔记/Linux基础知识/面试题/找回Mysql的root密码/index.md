---
title: "找回Mysql的root密码"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/面试题/找回Mysql的root密码/
categories:
  - Linux笔记
  - Linux基础知识
  - 面试题
  - 找回Mysql的root密码
tags:
  - Study
---

```txt
如忘记了mysql5.7数据库的ROOT用户的密码 如何找回？
```

```bash
#修改文件
vim /etc/my.cnf

#在mysqld模块插入
skip-grant-tables

#重启mysql服务
mysql -u root -p
#空密码进入 修改密码
show databases;
#能看到有一个mysql数据库
use mysql;
show tables;
#其中有一个user表
#可以看看表里面的信息
desc user;
#可以看到里面有一个权限字段
authentication_string
#修改密码
update user set authentication_string=password("密码") where user='root';
#刷新权限
flush privileges;

#删了刚才写的权限跳过 重启mysql 测试密码
```

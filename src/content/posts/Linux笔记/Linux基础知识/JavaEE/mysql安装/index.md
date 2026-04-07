---
title: "Linux笔记 - Linux基础知识 - JavaEE - mysql安装"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 步骤

- 新建文件夹/opt/mysql cd进去

- 运行 wget http://dev/mysql.com/get/mysql-5.7.26-1.el7.x86_64.rpm-bundle.tar 下载mysql安装包
**ps:CentOS7.6自带的类mysql数据库mariadb会跟mysql冲突 要先删了**

- 运行tar -xvf mysql-5.7.26-1.el7.x86_64.rpm-bundle.tar

- 运行 rpm-qa | grep mari 查询mariadb相关安装包

- 运行 rpm -e --nodeps mariadb-libs 卸载

- 开始安装 依次运行

```bash
rpm -ivh mysql-community-common-5.7.26-1.el7.x86_64.rpm
rpm -ivh mysql-community-libs-5.7.26-1.el7.x86_64.rpm
rpm -ivh mysql-community-client-5.7.26-1.el7.x86_64.rpm
rpm -ivh mysql-community-server-5.7.26-1.el7.x86_64.rpm
```

- 运行 systemctl start mysqld.service 启动mysql

- 设置root用户密码
Mysql自动给root用户设置随机密码 运行 grep "password" /var/log/mysqld.log 可以查看当前密码

- 运行mysql -u root -p 用root用户登录 密码用上面指令查到的

- 设置root密码 对于个人开发环境 如果要设简单的密码 可以运行

```bash
set global validate_password_policy=0; 提示密码策略(默认为1)
```

- set password for 'root'@'localhost' = password('密码');

- 运行flush privileges;  使密码生效
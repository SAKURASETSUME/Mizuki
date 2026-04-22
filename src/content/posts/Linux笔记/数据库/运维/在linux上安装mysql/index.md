---
title: "Linux笔记 - 数据库 - 运维 - 在linux上安装mysql"
category: "Linux笔记"
date: 2026-04-22
published: 2026-04-22
author: "Rin"
---

```bash
#下载linux的安装包
wget https://dev.mysql.com/get/Downloads/MySQL-8.4/mysql-8.4.9-1.el7.x86_64.rpm-bundle.tar

#查看linux自带的mariadb 如果有就卸了
rpm -qa | grep mariadb
rpm -e mariadb-libs-5.5.68-1.el7.x86_64 --nodeps
#创建目录并解压
mkdir mysql
tar -xvf mysql-8.0.46-1.el7.x86_64.rpm-bundle.tar -C mysql

#安装mysql的安装包
cd mysql

#使用rpm来解压rpm包 如果解压过程中少依赖了 用yum自己装一下 rpm包一定要按顺序来装
#顺序为 common -> client-plugins -> libs -> libs-compat -> devel -> client -> icu -> server
rpm -ivh

#启动mysql服务
systemctl start mysqld
systemctl enable mysqld
#查询自动生成的root用户密码
grep 'temporary password' /var/log/mysqld.log
#登录
mysql -uroot -p
#更改密码
alter user 'root'@'localhost' identified by 'root';
#如果报错 可以改密码复杂度
set validate_password.policy=0;
#8.4可以用这个
SET GLOBAL validate_password.policy=LOW;

set validate_password.length=4;
#8.4用这个
set global validate_password.length=4;
#创建一个用于远程访问的用户
create user 'root'@'%' identified with mysql_native_password by 'root';
#8.4用这个
CREATE USER 'root'@'%' IDENTIFIED BY 'Zerotwo02!';

#赋权
grant all on *.* to 'root'@'%'
#使用连接软件连接mysql
```
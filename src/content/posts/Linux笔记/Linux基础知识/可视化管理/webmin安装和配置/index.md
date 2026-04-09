---
title: "Linux笔记 - Linux基础知识 - 可视化管理 - webmin安装和配置"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 基本介绍

**Webmin是功能强大的基于Web的Unix/linux系统管理工具 管理员通过浏览器访问Webmin的各种管理功能并完成相应的管理操作 除了各版本的linux以外还可用于：AIX、HPUX、Solaris、Unixware、Irix和FreeBSD等系统**

## 安装webmin并配置

- 下载webmin

```bash
#手动下载 用工具传也行
#指令下载
wget http://download.webmin.com/download/yum/webmin-1.700-1.noarch.rpm

#安装
rpm -ivh webmin-1.700-1.noarch.rpm

#重置密码 
#root是webmin的用户名 不是OS的
/usr/libexec/webmin/changepass.pl /etc/webmin root Zerotwo02

#修改webmin的端口号
vim /etc/webmin/miniserv.conf
port=7777
listen=7777

#重启webmin
/etc/webmin/restart #重启
/etc/webmin/start #启动
/etc/webmin/stop #停止

#防火墙开放7777端口
firewall-cmd --zone=public --add-port=7777/tcp --permanent #配置防火墙开放7777端口
firewall-cmd --reload
direwall-cmd --zone=public --list-ports #查看开放的端口

#访问
```
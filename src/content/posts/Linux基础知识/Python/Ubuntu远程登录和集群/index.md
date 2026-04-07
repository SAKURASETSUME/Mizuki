---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/ubuntu远程登录和集群/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## SSH

**SSH是建立在应用层和传输层基础上的安全协议 目前比较可靠的 专门为远程登录会话和其它网络服务提供安全性的协议 几乎所有UNIX/Linux平台都可运行SSH**

**使用SSH 需要安装相应的服务器和客户端 如果A机器想被B机器远程控制 那么A机器需要安装SSH服务器 B机器需要安装SSH客户端**

**和CentOS不一样 Ubuntu没有预装SSHD服务 (可以使用netstat -anp 命令查看 apt install net-tools)**

## 安装SSH并启用

```bash
#安装ssh服务端+客户端
sudo apt-get install openssh-server

#启用sshd服务
service sshd restart

#看一眼22端口是不是正在监听
netstat -anp | more
```

## 从一台Linux系统远程登录另一台Linux系统

**在创建服务器集群时 会使用到该技术**

```bash
#基本语法
ssh 用户名@IP

#例如
ssh kazusa@192.168.2.50
#使用ssh访问 如果访问出现错误 可以查看是否有该文件
~/.ssh/known_ssh 尝试删除该文件解决

#登出
exit 或者 logout
```
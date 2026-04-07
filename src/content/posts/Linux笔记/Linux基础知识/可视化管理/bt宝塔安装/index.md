---
title: "bt宝塔安装"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/可视化管理/bt宝塔安装/
categories:
  - Linux笔记
  - Linux基础知识
  - 可视化管理
  - bt宝塔安装
tags:
  - Study
---

## 基本介绍

bt宝塔Linux面板是提升运维效率的服务器管理软件 支持一键LAMP/LNMP/集群/监控/网站/FTP/数据库/JAVA等多项服务器管理功能

## 安装

```bash
mkdir /opt/bt
cd /opt/bt

yum install -y wget && wget -O install.sh http://download.bt.cn/install/install_6.0.sh && sh install.sh

 外网ipv4面板地址: https://111.167.200.103:42201/040937e6
 内网面板地址:     https://192.168.29.50:42201/040937e6
  username: epkqneky
 password: 88f18470

#如果忘记账号密码了
bt default
```

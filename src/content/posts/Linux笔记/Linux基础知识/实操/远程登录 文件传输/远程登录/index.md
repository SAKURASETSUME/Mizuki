---
title: "远程登录"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/实操/远程登录 文件传输/远程登录/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 登陆工具

- Xshell （free-for-home-school即可）

## 使用ipv4进行连接 网卡名一般是ens开头的

**如果没有ipv4的话 使用如下命令**

```shell
#查看网卡名
ls /etc/sysconfig/network-scripts/ifcfg-*

#使用vi编辑网卡
vi /etc/sysconfig/network-scripts/ifcfg-ens33

#修改配置 BOOTPROTO=dhcp
	#	 ONBOOT=yes

```
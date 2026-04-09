---
title: "Linux笔记 - Linux基础知识 - 实操 - 网络配置 - linux网络环境配置实例"
category: "Linux笔记"
date: 2026-03-11
published: 2026-03-11
author: "Rin"
---

## 第一种方法（自动获取）

说明：登陆后 通过界面的设置来自动获取ip 特点：linux启动后会自动获取IP 缺点是每次自动获取的ip可能不一样 这个缺点就注定了不可能把这个设置当做服务器使用

## 第二种方法 指定ip

说明：直接通过修改配置文件来指定IP 并可以连接到外网
编辑 vi /etc/sysconfig/network-scripts/ifcfg-ens33
要求：将ip地址配置为静态的 比如:192.168.29.50

**ifcfg-ens33文件说明**

```bash
TYPE=Ethernet #网络类型（通常是Ethernet）
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=dhcp
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens33
UUID=2de79d7b-06a1-47e4-b446-503243c63881 #随机ID
DEVICE=ens33  #接口名（设备 网卡）
ONBOOT=yes #系统启动时的网络接口是否有效
HWADDR=00:0c:2x:6x:0x:xx #MAC地址
``` 

## IP的配置方法\[none|static|bootp|dhcp](引导时不使用协议|静态分配IP|BOOTP协议|DHCP协议)

```bash
BOOTPROTO=static
#IP地址
IPADDR=192.168.29.50
#网关
GATEWAY=192.168.29.2
#域名解析器
DNS1=192.168.29.2
```

**注意：配置完之后看一眼VMware的网络编辑器 看看子网IP的C段和自己写的静态IP的C段一不一样 还有网关也看一眼 看看和自己配的一不一样**

- **配置完之后 重启网络服务或者重启系统生效**

```bash
reboot
#或者
service network restart
```
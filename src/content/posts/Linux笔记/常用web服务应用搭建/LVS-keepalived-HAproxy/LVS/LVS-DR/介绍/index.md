---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - LVS - LVS-DR - 介绍"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

**DR -> direct routing 直连路由**

## 工作原理

- 客户端将请求发往前端的负载均衡器，请求报文源地址是CIP，目标地址为VIP。
- 负载均衡器收到报文后，发现请求的是在规则面存在的地址，那么它将客户端请求报文的源MAC地址改为自己DIP的MAC地址，目标MAC改为了RIP的MAC地址，并将此包发送给RS。
- RS发现请求报文中的目的MAC是自己，就会将次报文接收下来，处理完请求报文后，将响应报文通过lo接口送给eth0网卡直接发送给客户端。

## 特点
- 集群节点和director必须在一个物理网络内
- RIP可以使用公网地址或私有地址
- director仅处理入站请求，director服务器的压力比较小
- 集群节点网关不指向director，故出站不经过director
- 不支持端口映射
- 大多数操作系统可以作为realserver，要支持隔离arp广播

## ARP相关的问题
- 通常，DR模式需要在Real-server上配置VIP，配置的方式为：
/sbin/ifconfig lo:0 inet VIP netmask 255.255.255.255

- 原因在于，当LVS把client的包转发给Real-serVer时，因为包的目的IP地址是
VIP，那么如果Real-server收到这个包后，发现包的目的IP不是自己的系统IP，那
么就会认为这个包不是发给自己的，就会丢弃这个包，所以需要将这个IP地址绑
到网卡上；当发送应答包给client时，Real-serVer就会把包的源和目的地址调换，
直接回复给client.

- 关于ARP广播：
上面绑定VIP的掩码是"255.255.255.255"，说明广播地址是其本身，那么他就不
会将ARP发送到实际的自己该属于的广播域了，这样防止与LVS上VIP冲突，而导
致IP冲突。
另外在Linux的Real-server上，需要设置ARP的sysctl选项：
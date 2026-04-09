---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - keepalived - 协议"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## keepalived是什么？
keepalived是集群管理中保证集群高可用的一个服务软件，用来防止单点故障。

## 工作原理
keepalived是以VRRP协议为实现基础的，VRRP全称Virtual　RouterRedundancyProtocol，即虚拟路由冗余协议。

将N台提供相同功能的服务器组成一个服务器组，这个组里面有一个master和多个backup，master上面有一个对外提供服务的vip（该服务器所在局域网内其他机器的默认路由为该vip），master会发组播，当backup收不到vrrp包时就认为master岩掉了，这时就需要根据VRRP的优先级来选举一个backup当master

## 组播
IPV4总共三种通信方式：单播，组播，广播。
组播是指以224.0.0.0地址作为通信地址的一种方式
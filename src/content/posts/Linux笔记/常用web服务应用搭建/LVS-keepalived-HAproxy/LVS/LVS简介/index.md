---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - LVS - LVS简介"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

LVS是LinuxVirtual Server,Linux虚拟服务器

LVS工作在一台server上提供Directory(负载均衡器）的功能 本身并不提供服务 只是把特定的请求转发给对应的realserver(真正提供服务的主机) 从而实现集群环境中的负载均衡

## LVS的框架

- LB-SERVER负载均衡器
- relay-server真实服务器

## LVS的工作模式

- **NAT转发模式**

- **DR直接路由模式**

- TUN-IP模式

- FULL-NAT

## LVS四种工作模式的对比


|               | VS/NAT | VS/TUN    | VS/DR         |
| ------------- | ------ | --------- | ------------- |
| 服务器OS         | 任意     | 支持隧道      | 多数(支持Non-arp) |
| 服务器网络         | 私有网络   | 支持局域网/广域网 | 局域网           |
| 服务器数目(100M网络) | 10-20  | 100       | >100          |
| 服务器网关         | 负载均衡器  | 自己的路由     | 自己的路由         |
| 效率            | 一般     | 高         | 最高            |
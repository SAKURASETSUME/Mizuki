---
title: "Linux笔记 - 常用web服务应用搭建 - LVS-keepalived-HAproxy - LVS - LVS-NAT - 介绍"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

### NAT转发模式

Network Address Translation 网络地址转换

**工作原理：**
客户端将请求发往前端的负载均衡器 请求报文源地址是CIP(客户端IP)后面统称为CIP) 目标地址为VIP(负载均衡器前端地址 后面统称为VIP) 
负载均衡器收到报文后 发现请求的是在规则里面存在的地址 那么它将客户端请求报文的目标IP地址改为了后端服务器的RIP地址并将报文根据算法发送出去
报文送到RealServer后 由于报文的目标地址是自己 所以会响应该请求 并将响应报文返还给LVS
然后Ivs将此报文的源地址修改为本机并发送给客户端
注意在NAT模式中 RealSenver的网关必须指向LVS 否则报文无法送达客户端
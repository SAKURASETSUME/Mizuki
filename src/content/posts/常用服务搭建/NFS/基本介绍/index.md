---
title: "未命名文章"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/基本介绍/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 概述

NFS是一种基于TCP/IP 传输的网络文件系统协议。通过使用NFS协议，客户机可以像访问本地目录一样访问远程服务器中的共享资源
NAS存储: NFS服务的实现依赖于RPC (Remote Process Call，远端过程调用)机制， 以完成远程到本地的映射过程。在Centos 7系统中，需要安装nfs-utils、rpcbind 软件包来提供NFS共享服务，前者用于NFS共享发布和访问，后者用于RPC支持。手动加载NFS共享服务时，应该先启动rpcbind，再启动nfs。
nfs端口:2049
RPC端口:111w

## 特点

- 采用TCP/IP传输网络文件
- 安全性低
- 简单易操作
- 适合局域网环境
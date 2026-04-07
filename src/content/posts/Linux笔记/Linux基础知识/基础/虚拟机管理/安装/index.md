---
title: "安装"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/基础/虚拟机管理/安装/
categories:
  - Linux笔记
  - Linux基础知识
  - 基础
  - 虚拟机管理
  - 安装
tags:
  - Study
---

## 磁盘手动分区

**一般分为三个区**
*  引导分区(boot分区) -> 1G 文件系统改为ext4 设备类型是标准分区
* 交换分区(swap) -> 分配的运存大小 用处是防止运存满 临时充当内存 设备类型是标准分区 文件系统是swap
* 根分区(/) -> 剩下的所有空间 文件系统改为ext4 设备类型是标准分区

## KDUMP

**用处：是系统崩溃的日志 建议勾选**
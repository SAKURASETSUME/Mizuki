---
title: "动态监控系统"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/实操/进程管理/动态监控系统/
categories:
  - Linux笔记
  - Linux基础知识
  - 实操
  - 进程管理
  - 动态监控系统
tags:
  - Study
---

## 介绍

top与ps命令很相似 它们都用来显示正在执行的进程 top与ps的最大不同之处是 在top执行一段时间可以更新正在运行的进程

```bash
#基本语法
top [选项]
#选项
-d 秒数 指定top命令每隔几秒更新 默认是3s
-i 使top不显示任何闲置或僵死进程
-p 通过指定监控进程ID来仅仅监控某个进程的状态
```

### 顶部信息

```txt
top - 11:47:03
up  4:52 (系统运行时间)
3 users
load average: 0.00, 0.01, 0.05  (负载均衡 计算方法是三个数字加一起除以3 如果超过0.7就要性能优化)
Tasks: 266 total  1 running, 264 sleeping,   1 stopped,   0 zombie
%Cpu(s):  0.0 us(用户占用),  0.0 sy(系统占用),  0.0 ni,100.0 id(空闲cpu),  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  1863032 total,    88716 free,   937540 used,   836776 buff/cache
KiB Swap:  2096124 total,  2091508 free,     4616 used.   740800 avail Mem 
```

## 交互操作

```bash
P 按照CPU排序
M 按内存使用率排序
N 以PID排序
q 退出top
```

### 案例1 监视特定用户

```bash
#输入top后
u : 输入u 回车后输入用户名
```

### 案例2 终止指定的进程

```bash
#输入top后
k 回车 然后输入要结束的PID
#信号量输入9
```

### 案例3 设置每10s定时刷新信息

```bash
top -d 10
```

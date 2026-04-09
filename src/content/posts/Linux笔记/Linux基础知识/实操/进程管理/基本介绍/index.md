---
title: "Linux笔记 - Linux基础知识 - 实操 - 进程管理 - 基本介绍"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

在LINUX中 每个执行的程序都称为一个进程 每一个进程都分配一个ID号（pid 进程号）
每个进程都可能以两种方式存在的：**前台**与**后台** 所谓前台进程就是用户目前的屏幕上可以进行操作 后台进程则是实际在操作 但由于屏幕上无法看到的进程 通常使用后台方式执行
一般系统的服务都是以后台进程的方式存在 而且都会常驻系统中 直到关机才结束

## 显示系统执行的进程

```bash
#基本语法
ps

#常用选项
ps -a:显示当前终端的所有进程信息
ps -u:以用户的格式显示进程信息
ps -x: 显示后台进程运行的参数

#常用组合
ps -aux | grep xxx
```

### 字段介绍

- USER：进程的执行者
- PID：进程号
- %CPU：CPU占用率
- %MEM：占用物理内存的百分比
- VSZ：占用虚拟内存的大小
- RSS：占用物理内存的大小
- TTY：终端名称 一般是缩写
- STAT：当前运行状态

  S：休眠
  R：运行
  s：表示该进程是会话的先导进程
  N：表示进程拥有比普通优先级更低的优先级
  D：短期等待
  Z：僵死进程 （需要定时进行清除）
  T：被跟踪或者被停止

- START：进程执行的开始时间
- TIME：进程占用CPU的时间
- COMMAND：进程名/执行该进程的指令 如果过长会被截断显示

## 父子进程

**子进程就是由父进程创建的进程 如果杀掉父进程 那么子进程也会被杀掉**

```bash
#基本语法
ps -ef

-e 显示所有进程
-f 全格式

#第一个数字是进程本身的pid
#第二个数字就是父进程的pid

#查到了父进程的id 直接用
ps -aux | more
```

## 终止进程

```bash
#基本语法
kill [选项] 进程号
killall 进程名称 (支持通配符)
#常用选项
-9 表示强迫进程立即停止
```

### 案例1 踢掉某个非法登录用户

```bash
#先查看登陆的信息
ps -aux | grep sshd

#根据非法用户的PID 直接kill
kill PID
```

### 案例2 终止远程登录服务sshd 在适当时候再次重启sshd

```bash
kill PID

#重启
/bin/ststemctl start sshd.service
#或者
service sshd restart
```

### 案例3 终止多个gedit

```bash
killall gedit
```

### 案例4 强制杀掉一个终端

```bash
#查询pid
ps -aux | grep bash

kill -9 PID
```

## 查看进程树

```bash
#基本语法
pstree [选项]
#常用选项
-p 显示进程PID
-u 显示进程的所属用户
```

### 案例1 树状形式显示进程的pid

```bash
pstree -p
```

### 案例2 树状形式显示用户名

```bash
pstree -u
```
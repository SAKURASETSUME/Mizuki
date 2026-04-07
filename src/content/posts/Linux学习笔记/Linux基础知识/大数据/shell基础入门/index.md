---
title: "shell基础入门"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/大数据/shell基础入门/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 作用

- Linux运维工程师在进行服务器集群管理时需要编写Shell程序来进行服务器管理
- 对于JavaEE和Python程序员来说 工作的需要 会编写一些Shell脚本进行程序或者是服务器的维护 比如编写一个定时备份数据库的脚本
- 对于大数据程序员来说 需要编写Shell程序来管理集群

## 什么是Shell

**Shell是一个命令行解释器 它为用户提供了一个向Linux内核发送请求以便运行程序的界面系统级程序 用户可以用Shell来启动 挂起 停止甚至是编写一些程序**

## Shell脚本的执行方式

- 脚本格式要求

```txt
脚本以#!/bin/bash开头
脚本需要有可执行权限
```

### 编写一个脚本 输出hello world

```shell
#!/bin/bash
echo "hello world!"
```

### 两种执行方式

- 用绝对路径/相对路径运行 比如./root/shcode/hello.sh
- sh+脚本绝对路径/相对路径 比如sh /root/shcode/hello.sh 这种不需要赋x权限就能运行了
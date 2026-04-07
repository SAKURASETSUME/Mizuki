---
title: "数据恢复restore"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/高级/备份与恢复/数据恢复restore/
categories:
  - Linux笔记
  - Linux基础知识
  - 高级
  - 备份与恢复
  - 数据恢复restore
tags:
  - Study
---

## 基本语法

```bash
restore [模式选项] [选项]

#模式选项 不能混用 每次只能用一种
-C 对比模式 将备份的文件与存在的文件进行对比
-i 交互模式 进行还原操作时 restore命令将依序询问用户
-r 还原模式
-t 查看模式

#选项
-f <备份设备> 从指定的文件中读取备份数据 进行还原操作
```

## 案例1 比较模式

```bash
restore -C -f /opt/boot.bak.bz2

#看Label 不同会报错 相同会显示none
```

## 案例2 查看备份文件有哪些数据

```bash
restore -t -f /opt/boot.bak.bz2
```

## 案例3 还原模式

```bash
#如果有增量备份 需要把增量备份文件也恢复
mkdir /opt/boottmp
cd /opt/boottmp

restore -r -f /opt/boot.bak.bz2
restore -r -f /opt/boot.bak1.bz2
```
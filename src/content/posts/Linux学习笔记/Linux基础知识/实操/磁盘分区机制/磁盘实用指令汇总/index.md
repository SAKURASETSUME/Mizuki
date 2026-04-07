---
title: "磁盘实用指令汇总"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/实操/磁盘分区机制/磁盘实用指令汇总/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 统计/opt文件夹下文件的个数

```bash
#先列出所有opt下的文件和文件夹 之后用grep过滤 正则表达式的意思是只要以-开头的 最后wc的作用是列出个数
ll /opt | grep "^-" | wc -l
```

## 统计/opt下目录的个数

```bash
ll /opt | grep "^d" | wc -l
```

## 统计/opt下文件的个数 包括子文件夹里的

```bash
ls -lR /opt | grep "^-" | wc -l
```

## 统计/opt下目录的个数 包括子文件夹里的

```bash
ll -R /opt | grep "^d" | wc -l
```

## 以树状显示目录结构

```bash
#需要自己安装一下tree命令 
yum install tree

tree /opt
```
---
title: "查找指令"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/实操/实用指令/查找指令/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

- ## find指令

**find指令将从指定目录向下递归地遍历其各个子目录 将满足条件的文件或者目录显示在终端**

```bash
find [搜索范围] [选项]

#选项说明
-name 查询方式 按照指定文件名查找
-user 用户名 查找属于指定用户名的所有文件
-size 文件大小 按照指定文件大小查找文件 +n大于 -n小于 n等于 单位有 k M G

#例如 查找整个linux系统下大于200M的文件
find / -size +200M
```

- ## locate指令

**locate指令可以快速定位文件路径 locate指令利用事先建立的系统中所有文件名称及路径的locate数据库实现快速定位给定的文件 locate指令无需遍历整个文件系统 查询速度较快 为了保证查询结果的准确度 管理员必须定期更新locate时刻**

```bash
#基本语法
locate 文件
#由于locate指令基于数据库进行查询 所以第一次运行前 必须使用updatedb指令创建locate数据库
```

- ## which指令

**可以查看某个指令在哪个目录下**

```bash
#基本语法
which 指令
```

- ## grep指令

**grep过滤查找 管道符 “|” 表示将前一个命令的处理结果输出传递给后面的命令处理**

```bash
#基本语法
grep [选项] 查找内容 源文件
#常用选项
-n 显示匹配行及行号
-i 忽略大小写

#例如 在hello.txt中查找yes是否存在 以及行号
cat /home/hello.txt | grep -n "yes"
#或者
grep -n "yes" /home/hello.txt
```
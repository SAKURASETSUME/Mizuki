---
title: "Linux笔记 - Linux基础知识 - 实操 - 实用指令 - 压缩和解压"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

- ## gzip/gunzip 指令

```bash
#基本语法
gzip 文件 （只能压缩成*.gz）
gunzip 文件
```

- ## zip/unzip

**项目打包常用**

```bash
#基本语法
zip [选项] xxx.zip 目标文件
unzip [选项] xxx.zip
#常用选项

#zip
-r 递归压缩

#unzip
-d 目录 指定解压后的文件存放目录

#例如
zip -r myhome.zip /home/ [将home及其子文件和子文件夹都压缩]
```

- ## tar指令

**tar指令是打包指令 最后打包后的文件是 .tar.gz的文件**

```bash
#基本语法
tar [选项] XXX.tar.gz 打包的内容
#选项说明
-c 产生.tar打包文件
-v 显示详情信息
-f 指定压缩后的文件名
-z 打包同时压缩
-x 解包.tar文件

#案例
#压缩多个文件 将/home/pig.txt和/home/cat.txt压缩成pc.tar.gz
tar -zcvf pc.tar.gz /home/pig.txt /home/cat.txt

#将/home文件夹压缩成myhome.tar.gz
tar -zcvf myhome.tar.gz /home/

#将pc.tar.gz解压到当前目录
tar -zxvf pc.tar.gz

#将myhome.tar.gz解压到/opt/tmp目录下
tar -zxvf myhome.tar.gz -C /opt/tmp
```
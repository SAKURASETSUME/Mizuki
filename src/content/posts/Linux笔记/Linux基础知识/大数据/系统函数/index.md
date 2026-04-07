---
title: "系统函数"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/大数据/系统函数/
categories:
  - Linux笔记
  - Linux基础知识
  - 大数据
  - 系统函数
tags:
  - Study
---

## 函数函数

**shell编程和其它编程语言一样 有系统函数 也可以自定义函数**

## 系统函数

```bash
#基本语法
#basename功能：返回完整路径最后/的部分 常用于获取文件名
basename [pathname] [suffix]
basename [string] [suffix] (功能描述：basename命令会删除所有前缀包括最后一个/字符 然后将字符串显示出来)

#选项
suffix为后缀 如果suffix被指定了 basename会将pathname或string中的suffix去掉

#dirname
#基本语法
dirname 绝对路径 #去除文件名 返回目录部分
```

## 实例

```txt
返回/root/shcode/aaa.txt的aaa.txt部分
返回/root/shcode/test.txt的/root/shcode
```

```bash
basename /root/shcode/aaa.txt
dirname /root/shcode/aaa.txt
```
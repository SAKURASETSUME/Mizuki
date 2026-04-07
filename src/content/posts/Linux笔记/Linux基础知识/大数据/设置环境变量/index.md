---
title: "Linux笔记 - Linux基础知识 - 大数据 - 设置环境变量"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 基本语法

```bash
export 变量名=变量值 （将shell变量输出为环境变量）
source 配置文件 （让修改后的配置信息立即生效）
echo $变量名 （查询环境变量的值）
```

## 快速入门

- 在/etc/profile文件中定义TOMECAT_HOME环境变量
- 查看环境变量TOMCAT_HOME的值
- 在另一个shell程序中使用TOMCAT_HOME

```bash
vim /etc/profile

#写入
export TOMCAT_HOME=abbb #保存

source /etc/profile

echo $TOMCAT_HOME
```

## shell脚本的多行注释

```bash
#必须要独立一行 不能和内容在同一行
:<<!
内容
!
```
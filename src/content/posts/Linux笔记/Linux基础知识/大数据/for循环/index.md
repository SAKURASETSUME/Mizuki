---
title: "Linux笔记 - Linux基础知识 - 大数据 - for循环"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 基本语法1

```bash
for 变量 in 值1 值2 值3...
do
程序
done
```

## 案例：打印命令行输入的参数

```bash
#!/bin/case
#$*把输入的参数当做一个整体 所以只会输出一句话
for i in "$*"
do
        echo "num is $i"
done

#$@获取参数 这时是分别对待的
for j in "$@"
do
        echo "num is $j"
done
```

## 基本语法2

```bash
for ((初始值;循环控制条件;变量变化))
do
程序
done
```

## 案例 一加到一百

```bash
#!/bin/bash
#从1加到100
SUM=0
for (( i=1; i<=100 ; i++ ))
do
        SUM=$[$SUM+$i]
done

echo "总和SUM=$SUM"
```

## 案例 从输入加到输入

```bash
#!/bin/bash

#从输入的数字加到输入的数字
SUM=0
for (( i=$1; i<=$2 ; i++ ))
do
        SUM=$[$SUM+$i]
done

echo "总和SUM=$SUM"
```
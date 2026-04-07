---
title: "自定义函数"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/大数据/自定义函数/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 基本语法

```bash
[ function ] funname[()]
{
		Action;
		[return int;]
}

#调用直接写函数名 : funname [值]
```

## 实例

```txt
计算输入两个参数的和 getSum
```

```bash
#!/bin/bash
function getSum ()
{       
        SUM=$[$1+$2]
        echo "和=$SUM"
}

#输入两个值
read -p "请输入n1" n1 
read -p "请输入n2" n2

#调用自定义函数
getSum $n1 $n2

```
---
title: "ok = ok"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/条件判断/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 基本语法

```bash
[ condition ] #空格不要省
#非空返回true 可用$?验证 0为true >1为false
```

## 常用判断条件

```bash
= 字符串比较

#两个整数的比较
-lt 小于
-le 小于等于
-eq 等于
-gt 大于
-ge 大于等于
-ne 不等于

#按照文件权限进行判断
-r 读权限
-w 写权限
-x 执行权限

#按照文件类型进行判断
-f 文件存在并且是一个常规的文件
-e 文件存在
-d 文件存在并是一个目录
```
## 案例

```txt
[ addad ] true
[ ] false
[ condition ] && echo OK || echo notok 条件满足 执行后面的语句
```

```txt
"ok" = "ok"
23 >= 22
/root/shcode/aaa.txt是否存在
```

```bash
#!/bin/bash
echo $[ addad ]
echo $[]
echo $[ cabb ] || echo ok || echo notok

# ok = ok
if [ "ok" = "ok" ]
then
        echo "equal"
fi

# 23 >= 22
if [ 23 -ge 22 ]
then
        echo "大于"
fi

# /root/shcode/aaa.txt是否存在
if [ -f /root/shcode/aaa.txt ]
then
        echo "存在"
fi
```

## 单分支多分支

```bash
#基本语法
if [ 条件判断式 ]
then
代码
fi

#或者
if [ 条件判断式 ]
then
代码
elif [条件判断式]
then
fi
```

### 案例

```txt
编写一个shell程序 如果输入的参数 大于等于60 则输出及格 反之不及格
```

```bash
#!/bin/bash

if [ $1 -ge 60 ]
then
        echo "及格了"
elif [ $1 -lt 60 ]
then
        echo "不及格"
fi
```
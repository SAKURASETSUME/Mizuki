---
title: "Linux笔记 - Linux基础知识 - 大数据 - shell变量"
category: "Linux笔记"
date: 2026-03-12
published: 2026-03-12
author: "Rin"
---

## shell变量介绍

- Linux Shell中的变量分为 系统变量和用户自定义的变量
- 系统变量:$HOME $PWD $SHELL $USER等等 比如echo $HOME
- 显示当前shell中所有变量: set

## shell变量的定义

```shell
#基本语法
#定义变量
变量名=值 #中间不要打空格

#撤销变量
unset 变量名

#声明静态变量
readonly 变量 #不能被unset
```

### 快速入门

#### 案例 定义变量、撤销变量

```bash
#!/bin/bash
A=100

#输出变量需要加上$
echo A=$A

unset A
#这里输出的应该为A=
echo A=$A

#定义静态变量
readonlyB=122

echo B=$B

unset B
#这里应该再输出一个B=122 静态变量不可被撤销
echo B=$B
```

### 定义变量的规则

- 变量名称可以由字母 数字 下划线组成 但是不能以数字开头
- 等号两边不能有空格
- 变量名称一般习惯为大写

### 将命令的返回值赋给变量

- A=\`date\` 反引号 运行里面的命令 并把结果返回给变量A
- A=$(date) 等价于反引号
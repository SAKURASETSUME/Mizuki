---
title: "权限的基本介绍"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/实操/组管理和权限管理/权限的基本介绍/
categories:
  - Linux笔记
  - Linux基础知识
  - 实操
  - 组管理和权限管理
  - 权限的基本介绍
tags:
  - Study
---

ls -l中显示的内容如下:
-rwxrw-r-- 1 root root 1213 Feb 2 09:39 abc

0-9位说明

- 第0位确定文件类型（d , - , l , c , b）
l是链接 相当于快捷方式
d是目录 相当于文件夹
c是字符设备文件 比如鼠标键盘
b是块设备 比如硬盘

- 第1-3位确定所有者（该文件的所有者） 拥有该文件的权限 ---User

- 第4-6位确定所属组（同用户组的）拥有该文件的权限 ---Group

- 第7-9位确定其他用户拥有该文件的权限 ---Other

- 可用数字表示为： r=4 w=2 x=1 rwx=7

- 1：文件：硬链接数 或 目录：子目录数+文件数
- root 用户
- root 组
- 1213 文件大小（字节） 如果是文件夹 显示4096字节
- Feb 2 09:39 最后修改日期
- abc 文件名

## rwx权限

### 作用在文件上

- r代表可读：可以读取 查看
- w代表可写：可以修改 删除（需要对该文件所在的目录有写权限才能删）
- x代表可执行：可以执行

### 作用在目录上

- r代表可读：可以读取 ls查看
- w代表可写： 可以修改 对目录内创建+删除+重命名目录
- x代表可执行：可以进入该目录

## 修改权限

```bash
#方式一 通过+ - = 变更权限
#u:所有者 g:所有组 o:其他人 a:所有人(u+g+o)
chmod u=rwx,g=rx,o=x 文件/目录名
chmod o+w 文件/目录名
chmod a-x 文件/目录名

#方式二 通过数字变更权限
#r=4 w=2 x=1 rwx=7
chmod u=rwx,g=rw,o=x
#等效于
chmod 761
```

## 修改所有者和所在组

```bash
#修改所有者
chown newowner 文件/目录

#改变所有者和所在组
chown newowner:newgroup 文件/目录

-R #如果是目录 则使其下所有子文件和目录递归生效
chown -R kazusa:UserGroup /home/123

#修改文件/目录所在组
chgrp newgroup 文件/目录
```
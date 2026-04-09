---
title: "Linux笔记 - Linux基础知识 - 实操 - 软件包管理 - rpm管理"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## rpm包

**rpm是用于互联网下载包的打包及安装工具 它包含在某些Linux分发版中 它具有.RPM扩展名的文件 RPM是RedHat Package Manager的缩写 类似于Windows的setup.exe 这一文件格式名称虽然打上了RedHat的标志 但理念是通用的**

**Linux的分发版本都有采用 可以算是公认的行业标准了**

## rpm包的简单查询指令

```bash
#查询已安装的rpm列表
rpm -qa | grep xx

#比如查看是否安装了火狐
rpm -qa | grep firefox
```

## rpm包名基本格式

```txt
firefox-68.10.0-1.el7.centos.x86_64
```

- 名称：firefox
- 版本号：68.10.0-1
- 使用操作系统：el7.centos.x86_64
  表示centos7.x的64位系统
- 如果是i686、i386表示32位系统 noarch表示通用

## rpm包的其它查询指令

```bash
#查询所安装的所有rpm软件包
rpm -qa

#查询软件包是否安装
rpm -q 软件包名

#查询软件包信息
rpm -qi 软件包名

#查询软件包中的文件
rpm -al 软件包名

#查询文件所属的软件包
rpm -qf 文件全路径名
```

## 卸载rpm包

```bash
#基本语法
rpm -e RPM包的名称
```

**如果其他软件包依赖于要删除的软件包 卸载时就会报错 这时候加一个参数就可以删除了 但不推荐这么做**

```bash
#强制删除
rpm -e --nodeps foo
```

## 安装rpm包

```bash
#基本语法
rpm -ivh RPM包全路径名称
#参数说明
i 安装
v=verbose 提示
h=hash 进度条

#比如
rpm -ivh /opt/firefox-68.10.0-1.el7.centos.x86_64.rpm
```
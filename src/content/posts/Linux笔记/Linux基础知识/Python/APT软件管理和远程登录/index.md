---
title: "默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/Python/APT软件管理和远程登录/
categories:
  - Linux笔记
  - Linux基础知识
  - Python
  - APT软件管理和远程登录
tags:
  - Study
---

## APT介绍

apt是一款安装包管理工具 在Ubuntu下 我们可以使用apt命令进行软件包的安装 删除 清理等 类似于Windows的软件管理工具

## 镜像网站

**会定时将美国的APT服务器里的apt软件 下载到镜像站服务器中 供国内用户使用**

## apt操作的相关命令

```bash
#更新源
sudo apt-get update

#安装包
sudo apt-get install package

#删除包
sudo apt-get remove package

#获取包的相关信息
sudo apt-cache show package

#下载包的源代码
sudo apt-get source package
```

## 更新Ubuntu软件下载地址

```bash
#备份一下镜像文件 防止修改出问题
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup


#把sources.list清空
echo ' ' > /etc/apt/sources.list

#切换到root用户
su root

vi /etc/apt/sources.list

#写入镜像源
#直接复制镜像站的地址就行 比如清华大学的

# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse

# 以下安全更新软件源包含了官方源与镜像站配置，如有需要可自行修改注释切换
deb http://security.ubuntu.com/ubuntu/ noble-security main restricted universe multiverse
# deb-src http://security.ubuntu.com/ubuntu/ noble-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-proposed main restricted universe multiverse
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-proposed main restricted universe multiverse

#写完之后更新源地址
sudo apt-get update
```

## 测试

```txt
用apt装个vim
```

```bash
sudo apt-get install vim

sudo apt-cache show vim
```

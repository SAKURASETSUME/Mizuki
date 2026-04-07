---
title: "清除旧缓存"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/yum管理/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 介绍

yum是一个shell前段软件包管理器 基于RPM包管理 能够从指定的服务器自动下载RPM包并且安装 可以自动处理依赖性关系 并且一次安装所有的软件依赖包

```bash
#基本指令
#查询yum服务器是否有需要安装的软件
yum list | grep xxx

#安装指定的yum包
yun install xxx

#应用实例
yum list | grep firefox
#查询到firefox的包
yum install firefox.x86_64 
```

## 配置国内源

```bash
#下载阿里的镜像源
#备份系统默认配置
mkdir repos.bak
mv *.repo repos.bak

#下载阿里镜像
sudo wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

# 清除旧缓存
yum clean all

# 生成新缓存（将源信息缓存到本地，加速后续安装）
yum makecache

#验证
yum repolist enabled
```
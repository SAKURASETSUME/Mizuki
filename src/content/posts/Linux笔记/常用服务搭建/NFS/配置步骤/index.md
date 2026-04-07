---
title: "配置步骤"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/常用服务搭建/NFS/配置步骤/
categories:
  - Linux笔记
  - 常用服务搭建
  - NFS
  - 配置步骤
tags:
  - Study
---

## 修改主机名以及配置主机映射

**controller节点**
```bash
hostnamectl set-hostname nfs1
bash
vi /etc/hosts

127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.29.50  centos7
192.168.29.51  nfs
```

**compute节点**
```bash
hostnamectl set-hostname nfs2
bash
vi /etc/hosts

127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.29.50  centos7
192.168.29.51  nfs
```

## 安装nfs服务

**两个节点都要安装**

```bash
yum install -y nfs-utils
```

## 安装共享目录

**controller节点**
```bash
mkdir /nfs
```

**compute节点**
```bash
mkdir /test
```

## 配置文件

**controller节点**
```bash
vi /etc/exports

/nfs *(rw,sync,no_root_squash) 
#rw: read-write，可读写。
#sync：文件同时写入硬盘和内存。
#no_root_squash：NFS客户端连接服务端时，如果使用的是root，那么对服务端共享的目录来说，也拥有root权限。显然开启这项是不安全的。                                        
```

## 开启第一节点的NFS服务

**controller节点**
```bash
systemctl start nfs

#验证
ps -ef | grep "nfs"
```

## 查看第一节点的可共享目录

**compute节点**
```bash
#提前关了防火墙 或者开放111 2049端口
showmount -e 192.168.29.50 
```

## 进行NFS共享目录的挂载

**compute节点**
```bash
mount -t nfs 192.168.29.50:/nfs /test
```

## 查看系统磁盘使用情况

**compute节点**
```bash
mount -t nfs 192.168.29.50:/nfs /test
```

## 验证

**controller节点**
```bash
#切换到共享目录中 随便创一个文件
touch aaa.txt
```

**compute节点**
```bash
#切换到test目录中 查看文件
ls
#应该能看到有aaa.txt在里面 那么就是部署成功
```

参考：[NFS服务搭建(验证)详细步骤（适合小白专用）_nfs搭建教程-CSDN博客](https://blog.csdn.net/wjk1020312/article/details/130415937)
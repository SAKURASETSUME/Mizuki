---
title: "先更新yum源（可选，但建议执行）"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/vmtools/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 作用

- 可以在windows下更好地管理虚拟机
- 可以设置windows和虚拟系统之间的共享文件夹

## 安装步骤

- 进入centos
- 点击vm菜单的install vmware tools
- centos会出现一个vm的安装包 xx.tar.gz
- 拷贝到/opt
- 使用解压命令`tar` 得到一个安装文件
		cd /opt
		tar -zxvf xx.tar.gz
		cd vmware-tools-distrib
		./vmware-install.pl
- 进入该vm解压的目录 /opt目录下
- 安装./vmware-install.pl
- 全部使用默认设置
- 注意：安装vmtools **需要有gcc**

## 注意

**Vmware17版本已经不提供直接安装vmtools的工具 需要自己下载vmtools的镜像 之后关闭虚拟机 在虚拟机的cd/DVD选项中把vmtools镜像挂载一下**

## 第二种安装步骤（CentOS7下）

```bash
# 先更新yum源（可选，但建议执行） 
yum update -y 
# 安装open-vm-tools核心包（CentOS 7 专属）
yum install -y open-vm-tools 
# 安装桌面版依赖（如果是图形化CentOS 7，需执行；纯命令行可跳过） 
yum install -y open-vm-tools-desktop
```

```bash
# 启动open-vm-tools服务 
systemctl start vmtoolsd 
# 设置开机自启 
systemctl enable vmtoolsd 
# 再次检查服务状态（验证是否成功） 
systemctl status vmtoolsd
```

## 设置共享文件夹

- 首先在windows下创建一个文件夹
- 在虚拟机选项中添加共享文件夹
- 打开虚拟系统的文件夹 找/mnt下的文件夹即可

ps:实际开发中 文件的上传、下载一般用远程方式完成
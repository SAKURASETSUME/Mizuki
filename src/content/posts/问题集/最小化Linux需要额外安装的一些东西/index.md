---
title: "问题集 - 最小化Linux需要额外安装的一些东西"
category: "问题集"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 配置EPEL源 加速YUM

```bash
# 安装 EPEL 源
yum install -y epel-release
# 加快 YUM 速度
yum install -y yum-plugin-fastestmirror
# 安装 bash-completion
yum install -y bash-completion
# 使 bash-completion 立即生效
source /etc/profile.d/bash_completion.sh
```



## 配置阿里云yum源

```bash
# 下载阿里云 CentOS 7 新版源
curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
# 清理缓存
yum clean all
# 生成新缓存
yum makecache
```

## 基本工具

```bash
# 安装网络工具
yum install -y net-tools
# 安装 vim 编辑器
yum install -y vim
# 安装 wget 命令
yum install -y wget
# 安装 zip 和 unzip 工具
yum install -y unzip zip
```

## CentOS7,8发行版常用工具

```bash
yum install  vim iotop bc gcc gcc-c++ glibc glibc-devel pcre \
pcre-devel openssl  openssl-devel zip unzip zlib-devel  net-tools \
lrzsz tree ntpdate telnet lsof tcpdump wget libevent libevent-devel \
bc  systemd-devel bash-completion traceroute -y
```

## Ubuntu1804发行版常用工具

```bash
apt  install iproute2  ntpdate  tcpdump telnet traceroute \
nfs-kernel-server nfs-common  lrzsz tree  openssl libssl-dev \
libpcre3 libpcre3-dev zlib1g-dev ntpdate  traceroute  gcc openssh-server \
lrzsz tree  openssl libssl-dev libpcre3 libpcre3-dev zlib1g-dev ntpdate tcpdump \
telnet traceroute iotop unzip zip -y
```

## 利用shell脚本进行自动化安装

```bash
#!/bin/bash
#
#********************************************************************
#Author:        zouyongbing
#QQ:                         273838882
#Date:             2021-12-03
#FileName：        min_install.sh
#URL:             https://www.cnblogs.com/zouyongbing/
#Description：        The test script
#Copyright (C):     2021 All rights reserved
#********************************************************************
. /etc/os-release
min_install_yum(){
yum install  vim iotop bc gcc gcc-c++ glibc glibc-devel pcre \
pcre-devel openssl  openssl-devel zip unzip zlib-devel  net-tools \
lrzsz tree ntpdate telnet lsof tcpdump wget libevent libevent-devel \
bc  systemd-devel bash-completion traceroute -y
 }
 min_install_dnf(){
dnf install  vim iotop bc gcc gcc-c++ glibc glibc-devel pcre \
pcre-devel openssl  openssl-devel zip unzip zlib-devel  net-tools \
lrzsz tree ntpdate telnet lsof tcpdump wget libevent libevent-devel \
bc systemd-devel bash-completion traceroute -y
}
min_install_apt(){
apt  install iproute2  ntpdate  tcpdump telnet traceroute \
nfs-kernel-server nfs-common  lrzsz tree  openssl libssl-dev \
libpcre3 libpcre3-dev zlib1g-dev ntpdate  traceroute  gcc openssh-server \
lrzsz tree  openssl libssl-dev libpcre3 libpcre3-dev zlib1g-dev ntpdate tcpdump \
telnet traceroute iotop unzip zip -y
}
judge_os(){
     if [ ${VERSION_ID} == "7" ];then
         echo "你的操作系统是centos7,下面进行安装常用软件包："
         min_install_yum
         echo "所有常用软件包已经安装完毕！请验证是否成功执行！！！"
     elif [ ${VERSION_ID} == "8" ];then
         echo "你的操作系统是centos8,下面进行安装常用软件包："
         min_install_dnf
         echo "所有常用软件包已经安装完毕！请验证是否成功执行！！！"
     elif [ ${VERSION_ID} == "18.04" ];then
         echo "你的操作系统是ubuntu1804,下面进行安装常用软件包："
         min_install_apt
         echo "所有常用软件包已经安装完毕！请验证是否成功执行！！！"
     else
         echo "不支持的操作系统，请手动安装"
     fi
 }
 judge_os

```
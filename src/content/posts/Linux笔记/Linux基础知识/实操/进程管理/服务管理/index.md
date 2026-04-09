---
title: "Linux笔记 - Linux基础知识 - 实操 - 进程管理 - 服务管理"
category: "Linux笔记"
date: 2026-04-02
published: 2026-04-02
author: "Rin"
---

## 介绍

**服务本质就是进程 是运行在后台的 通常会监听某个端口 等待其他程序的请求 比如(mysqld sshd 防火墙等) 因此我们又称为守护进程 是Linux中非常重要的知识点**

## service管理指令

```bash
service 服务名 [start | stop | restart | reload | status]
```

**在CentOS7后 很多服务不再使用service 而是systemctl**

**service指令管理的服务在/etc/init.d查看**

### 案例 用service指令对network服务进行操作

```bash
#查看
service network status

#关闭
service network stop

#启动
service network start

#重启
service network restart
```

### 查看服务名

- 方式1：使用setup 系统服务 就可以看到全部 (退出键按tab就可以选中了)
- 方式2：/etc/init.d/ 看到service指令管理的服务

## 运行级别

- 0：关机 默认级别不能设置为0 不然就无法启动系统
- 1：单用户(找回丢失密码) root权限 用于系统维护
- 2：多用户状态没有网络服务（没有NFS）
- 3：多用户状态有网络服务（有NFS） 登陆过后进入控制台命令行模式
- 4：系统未使用保留给用户
- 5：X11控制台 登陆后进入图形界面
- 6：系统重启 同样默认级别不能设置为6

### 开机的流程说明

- 开机
- BIOS
- /boot
- systemd进程1
- 运行级别
- 运行级别对应的服务

### CentOS7后设置运行级别

```bash
#查看当前运行级别
systemctl get-default

#设置默认运行级别
systemctl set-default graphical.target 
systemctl set-default multi-user.target 
```

## chkconfig指令

### 介绍

- 通过chkconfig指令 可以给服务的各个运行级别设置自启动/关闭
- chkconfig指令管理的服务在/etc/init.d查看

```bash
#基本语法
#查看服务
chkconfig --list [| grep xxx]
chkconfig 服务名 --list
chkconfig --level 5 服务名 on/off
```

### 案例演示：对network服务 进行操作

```bash
#关闭3级的自启动
chkconfig --level 3 network off

#开启自启动
chkconfig --level 3 network on
```

## systemctl管理指令

```bash
#基本语法
systemctl [start | stop | restart | status] 服务名
```

**systemctl指令管理的服务在 /usr/lib/systemd/system查看**

### systemctl设置服务的自启动状态

```bash
#查看服务开机启动状态
systemctl list-unit-files [| grep 服务名]

#设置服务开机启动
systemctl enable 服务名

#关闭服务开机启动
systemctl disable 服务名

#查询某个服务是否是自启动的
systemctl is-enabled 服务名

```

### 案例 查看当前防火墙的状况 关闭和重启防火墙

```bash
#查看防火墙的状态
systemctl status firewall

#关闭防火墙(重启后回归之前的设置)
systemctl stop firewall

#启动防火墙（重启后回归之前的设置）
systemctl start firewall

#指定端口和ip访问
firewa11-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.44.101" port protocol="tcp" port="8080" accept"

#移除规则
firewa11-cmd --permanent --remove-rich-rule="rule family="ipv4" source address="192.168.44.101" port="8080" protocol="tcp" accept"
```

## 打开或关闭指定端口

```bash
#打开端口
firewall-cmd --permanent --add-port=端口号/协议

#关闭端口
firewall-cmd --permanent --remove-port=端口号/协议

#重新载入后才生效
firewall-cmd --reload

#查询端口是否开放
firewall-cmd --query-port=端口/协议
```

### 案例 开放防火墙的5353端口并测试连通

```bash
#测试telnet能不能通5353
telnet 192.168.29.50 5353

#查询防火墙运行状态
systemctl status firewalld

#查询开机自启
systemctl is-enabled firewalld

#如果没启动 就手动启动一下并设置开机自启
systemctl start firewalld

#开机自启
systemctl enable firewalld

#查询5353端口是否开放
firewall-cmd --query-port=5353/udp

#手动开放
firewall-cmd --permanent --add-port=5353/udp

#重载
firewall-cmd --reload

#查询是否开放
firewall-cmd --query-port=5353/udp

#手动连通
telnet 192.168.29.50 5353

#手动关闭
firewall-cmd --permanent --remove-port=5353/udp

#重载
firewall --reload
```
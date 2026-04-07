---
title: "资产分配"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/常用服务搭建/堡垒机-JumpServer/资产分配/
categories:
  - Linux笔记
  - 常用服务搭建
  - 堡垒机-JumpServer
  - 资产分配
tags:
  - Study
---

## 添加设备

**按照提示添加就行了 可以先不添加账号**

## 分配资产

**在账号管理那边分配 注意：账号能登入哪一个资产 就分配哪一个 不然会登不进去 名称可以随便填 但是用户名要填主机名 或者登陆系统的账户**

```bash
#Windows查看主机名
net user
#Windows查看当前登录用户
whoami
#一定要给系统设置密码 不然rdp会登不进去
#Windows设置密码 在控制面板-用户或家庭安全-添加或删除用户-改密码 添加密码
```

## 打开主机服务

**Windows打开RDP**

```bash
#Win7菜单栏搜允许远程访问计算机
#Win10右键此电脑 属性 找远程桌面 开一下就行
```

**Linux打开ssh**

```bash
#查看服务是否启动
systemctl status sshd
```

**mysql打开远程登录**

```bash
GRANT ALL ON *.* TO root@'%'IDENTIFIED BY '密码' WITH GRANT OPTION;
```

## 登陆

**要先把资产分配出去才能远程连接**

**在权限管理中 选择资产授权 创建一下就行 账号选择指定账号 之后登陆那个账号之后就可以远程连接了**

**如果在堡垒机无法上传文件 看一眼是不是系统防火墙没关 ps：上传文件不能直接在远程登录上传 要在文件管理那边上传**
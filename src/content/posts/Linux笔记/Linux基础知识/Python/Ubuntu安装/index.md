---
title: "Ubuntu安装"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/Python/Ubuntu安装/
categories:
  - Linux笔记
  - Linux基础知识
  - Python
  - Ubuntu安装
tags:
  - Study
---

## 概述

**Ubuntu是一个桌面应用为主的开源GUN/Linux操作系统 Ubuntu是基于GNU/Linux 支持x86 amd64(x64) 和ppc架构 Python开发者一般会选用Ubuntu作为生产平台**

## 安装

- CPU尽量分配4个核以上
- 内存最低2G
- 网络选NAT
- 安装时间比较长 慢慢等吧
- 进入界面之后按照提示选进行
- 检查网络是否通畅 如果需要自己配置一下静态IP
- 打开终端 看看常用的指令能不能正常使用(Ubuntu和CentOS都是基于Linux内核开发的 常用的指令用法差不多)

## 中文支持

- 点击左侧图标栏打开Language Support菜单
- Install / Remove Languages 找简体中文的选项 打个勾就行
- 这时汉语（中国）在最后一位 第一位是English 所以会显示英文 把中文选项卡拖到第一位 重新登陆一下就行了

## root用户

- 安装Ubuntu之后 都是普通用户权限 并没有root权限 如果需要使用最高权限 通常会在命令前面加一个sudo 会很麻烦
- 用su指令切到root就行 
- 如果没有给root设置初始密码 就会抛出错误 : su : Authentication failture 解决问题就是设置一个密码就行

## 给root设置密码

- sudo passwd 命令 设定root密码
- 设定root密码之后 输入su命令 并输入刚才的密码 就能切换成root了 提示符$代表一般用户 \#代表root用户
- 输入exit就能切换成root了
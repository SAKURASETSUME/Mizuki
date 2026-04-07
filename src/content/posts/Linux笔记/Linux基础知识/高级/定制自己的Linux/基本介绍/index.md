---
title: "Linux笔记 - Linux基础知识 - 高级 - 定制自己的Linux - 基本介绍"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 思路

**通过裁剪现有的Linux系统 可以创建出只有自己需要功能的系统 同时可以加深对linux的理解**

## 基本原理

**Linux系统的启动流程**

- 首先Linux要通过自检 检查硬件设备有没有故障
- 如果有多块启动盘 需要在BIOS中选择启动盘
- 启动MBR中的bootloader引导程序
- 加载内核文件
- 执行所有进程的父进程 老祖宗systemd
- 欢迎界面

**在Linux启动流程中 加载内核文件时关键文件**

- kernel文件：vmlinuz-3.10.0-957.el7.x86_64
- initrd文件：initramfs-3.10.0-947.el7.x86_64.img

## 制作min linux思路分析

- 在现有的Linux系统上加一块硬盘 /dev/sdb 在硬盘上分两个分区 /boot和/ 并将其格式化 需要明确的是 现在加的这个硬盘在现有的Linux系统中是/dev/sdb 但是 当我们把全部东西设置好时 要把这个硬盘拔除 放在新的系统上 此时就是/dev/sda
- 在/dev/sdb硬盘上 将其打造成独立的Linux系统 里面的所有文件都是要拷贝进去的
- 作为能独立运行的Linux系统 内核文件和initramfs文件也要一起拷贝到/dev/sdb上
- 创建一个新的linux虚拟机 将其硬盘指向创建的硬盘 启动即可
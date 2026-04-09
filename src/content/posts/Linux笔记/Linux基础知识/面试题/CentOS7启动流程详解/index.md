---
title: "Linux笔记 - Linux基础知识 - 面试题 - CentOS7启动流程详解"
category: "Linux笔记"
date: 2026-03-17
published: 2026-03-17
author: "Rin"
---

```txt
说明CentOS7启动流程 并说明和CentOS6相同的地方和不同的地方
```

```txt
第一阶段：硬件引导启动： 开机 -> BIOS （初始化硬件：显卡 内存 硬盘 时间  查找启动介质：CDROM USB HDD）-> MBR（安装grub2的booting 读取分区表）

第二阶段：GRUB2启动引导阶段： Boot.img -> Core.img -> *.mod -> grub.cfg
从这一个阶段开始 CentOS7的主引导程序用的是grub2 
这一步的流程：显示加载两个镜像 再加载Mod模块文件 把grub2程序加载执行 接着解析配置文件/boot/grub2/grub.cfg 根据配置文件加载内核镜像到内存 之后构建虚拟根文件系统 最后转到内核
在这里 grub.cfg 配置文件已经比较复杂了 但并不用担心：到了 CentOs7 中一般是使用命令进行配置 而不直接去修改配置文件了 不过我们可以看到 grub.ctg 配置文件开头注释部分说明了由/etc/grub.d/目录下文件和/etc/default/grub文件组成
一般修改好配置后都需要使用命令grub2-mkconfig-o /boot/grub2/grub.cfg 将配置文件重新生成

第三阶段：内核引导阶段：
这一步与CentOS6 也差不多 加载驱动 切换到真正的根文件系统 唯一不同的是执行的初始化程序变成了/usr/lib/systemd/systemd

第四阶段：systemd初始化阶段（又叫系统初始化阶段）
Centos7中我们的初始化进程变为了 systemd 执行默认 target 配置文件/etc/systemd/system/default.target（这是一个软链接 与默认运行级别有关) 然后执行 sysinittarget 来初始化系统和 basic.target 来准备操作系统 接着启动 multi-user.target 下的本机与服务器服务 并检查/etc/rc.d/rc.local 文件是否有用户自定义脚本需要启动 最后执行 multi-user 下的 getty.target 及登录服务 检查 default.target 是否有其他的服务需要启动
注意：/etc/systemd/system/default.target 指向了 /lib/systemd/system/ 目录下 的 graphical.target 或multiuser.target  而 graphical.target 依赖 multiuser.target multiusertarget 依赖 basic.target  basic.target 依赖sysinit.target 所以倒过来执行

```
---
title: "Linux笔记 - Linux基础知识 - 高级 - 定制自己的Linux - 操作步骤"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

- 先在现有的linux添加一块大小为20G的硬盘 (添加为单个文件做成系统盘 不要分开)

```bash
#给磁盘进行分区 格式化等操作 挂载到系统上
#先查一下磁盘情况 看看硬盘加没加上
lsblk

#分区
fdisk /dev/sdb
n
#使用默认配置
p
#第一个分区 给500M左右 是将来的boot分区
#剩下的全部给第二个分区 是将来的/分区
lsblk #查看sdb的分区情况

#格式化
mkfs.ext4 /dev/sdb1
mkfs.ext4 /deb/sdb2

#创建目录并挂载
mkdir -p /mnt/boot /mnt/sysroot
mount /dev/sdb1 /mnt/boot
mount /dev/sdb2 /mnt/sysroot

#安装grub 内核文件拷贝到目标磁盘
grub2-install --root-directory=/mnt/dev/sdb
#查看二进制文件确认是否安装成功
hexdump -C -n 512 /dev/sdb

#把sda中 boot里面的内容拷贝到mnt的boot中
cp -rf /boot/* /mnt/boot/

#修改grub2/grub.cfg文件
#在grub.cfg里面指定启动盘和根目录盘
#先进入到boot里面
cd /mnt/boot/grub2
vim grub2.cfg

#新开一个终端 查一下sdb的uuid
lsblk -f

#把grub2.cfg中 对应sda的/boot和/分区的硬盘uuid 改成sdb的uuid(不止一个地方 慢慢找 有很多)
#改完之后 在root对硬盘的uuid那一行 最后的部分加一句话 别加错地方 加到 开头是linuxxx /vmlinuzxxx那一行  有两个地方要加
selinux=0 init=/bin/bash

#创建目标主机的根文件系统
mkdir -pv /mnt/sysroot/{etc/rc.d,usr,var,proc,sys,dev,lib,lib64,bin,sbin,boot,srv,mnt,media,home,root}

#拷贝需要的bash
cp /lib64/*.* /mnt/sysroot/lib64/
cp /bin/bash /mnt/sysroot/bin/

#创建一个新的虚拟机 把默认分配的硬盘移除 执行刚刚创建的磁盘
#应该能顺利启动 但是很多命令都用不了 因为上面值拷贝了bash进去
#后面就是根据个人需要拷贝对应的功能进去就行
#比如把ls拷贝进来

#进入原机
#把sdb2挂到sysroot 如果不再挂一次 那么你拷到的是/dev/sdb2这个文件 和硬盘就没关系了
mount /dev/sdb2 /mnt/sysroot/
#拷贝
cp /bin/ls /mnt/sysroot/bin/ #ls命令
cp /bin/systemctl  /mnt/sysroot/bin/ #systemctl
cp /sbin/reboot /mnt/sysroot/sbin/

#重启新的系统 这时候还没有配置环境 ls之类的不能直接用 如果要用的话可以这么用
/bin/ls
```
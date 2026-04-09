---
title: "Linux笔记 - Linux基础知识 - 实操 - 磁盘分区机制 - Linux分区"
category: "Linux笔记"
date: 2026-03-17
published: 2026-03-17
author: "Rin"
---

- Linux来说无论有几个分区 分给哪一目录使用 它归根结底就只有一个目录 一个独立且唯一的文件结构 Linux中每个分区都是用来组成整个文件系统的一部分
- Linux采用了一种叫“载入”的处理方法 它的整个文件系统包含了一整套的文件和目录 且将一个分区和一个目录联系起来 这时要载入的一个分区将使它的存储空间在一个目录下获得

## 查看所有设备的挂载情况

```bash
lsblk
#或者
lsblk -f
```

## 硬盘说明

- Linux硬盘分IDE硬盘和SCSI硬盘 目前基本上是SCSI硬盘
- 对于IDE硬盘 驱动器标识符为 "hdx~" 其中"hd" 表明分区所在设备的类型 这里是指IDE硬盘 "x"为盘号（a为基本盘 b为基本从属盘 c为辅助主盘 d为辅助从属盘）， "~"代表分区 前四个分区用数字1-4表示 它们是主分区或者扩展分区 从5开始就是逻辑分区 例 hda3表示第一个IDE硬盘的第三个主分区或扩展分区 hdb2表示为第二个IDE硬盘的主分区或扩展分区
- 对于SCSI硬盘则标识为"sdx~" SCSI硬盘是用"sd"来表示分区所在设备的类型的 其余则和IDE硬盘的表示方法一样

## 增加磁盘实例

### 如何增加一块硬盘

- 虚拟机添加硬盘 （虚拟机软件手动添加 添加后重启系统）

- **分区**

```bash
#分区命令
fdisk /dev/sdb

#开始对sdb分区
m 显示命令列表
p 显示磁盘分区 同fdsik -l
n 新增分区
d 删除分区
w 写入并退出

#说明
#开始分区后输入n 新增分区 然后选择p 分区类型为主分区 两次回车默认剩余全部空间 最后输入w写入分区并退出 若不保存退出输入
```

- **格式化**

```bash
mkfs -t ext4 /dev/sdb1 #其中ext4是分区类型
```

- **挂载**

```bash
mount /dev/sdb1 /newdisk

#卸载
umount /dev/sdb1
#或者
umonut /newdisk
```

- **设置自动挂载**

**因为用命令行挂载 重启后会失效 所以要设定自动挂载**

```bash
#修改/etc/fstab
#添加完成后 执行mount -a

```

## 磁盘扩充

```bash
#提前在VMware中扩充好磁盘空间
lsblk #确定磁盘扩充完毕
fdisk /dev/sda #进入分区
#依次输入n p t 分区号 8e w
partprobe /dev/sda #刷新分区表
pvremove /dev/sda5 #清除LVM标记
mkfs.xfs -f /dev/sda5 #格式化为xfs

#创建临时目录并挂载
mkdir -p /data
mount /dev/sda5 /data 

#配置永久挂载
blkid /dev/sda5 #查看UUID
vim /etc/fstab
#写入
UUID=UUID /data xfs defaults 0 0

mount -a #验证配置
df -h
```
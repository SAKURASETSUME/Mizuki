---
title: "Linux笔记 - Linux基础知识 - 高级 - 备份与恢复 - dump备份"
category: "Linux笔记"
date: 2026-03-16
published: 2026-03-16
author: "Rin"
---

## 备份分区
### 案例1

```txt
将/boot分区所有内容备份到/opt/boot.back.bz2文件中 备份层级为0
```

```bash
dump -0uj -f /opt/boot.bak0.bz2 /boot
```

### 案例2

```txt
在/boot下拷贝一个文件 备份层级为1 注意看这次生成的备份文件大小
```

```bash
dump -1uj -f /opt/boot.bak1.bz2 /boot
```

**用dump配合crontab命令可以实现无人值守备份**

```bash
dump -W #显示需要备份的文件及其最后一次备份的层级 时间 日期
cat /etc/dumpdates #查看备份时间文件
```

## 备份文件或目录

```bash
#备份/etc目录 建议备份之后上传到其它服务器保存 防止数据丢失
#备份目录不支持增量备份 如果再用dump -1j会报错
dump -0j -f /opt/etc.bak0.bz2 /etc
```
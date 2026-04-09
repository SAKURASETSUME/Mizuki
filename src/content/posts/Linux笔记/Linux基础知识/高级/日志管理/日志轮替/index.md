---
title: "Linux笔记 - Linux基础知识 - 高级 - 日志管理 - 日志轮替"
category: "Linux笔记"
date: 2026-03-13
published: 2026-03-13
author: "Rin"
---

## 概念

**日志轮替就是把旧的日志移动并改名 同时建立新的空日志文件 当旧日志文件超出保存的范围之后 就会进行删除**

## 日志轮替文件命名

- centos7采用logrotate进行日志轮替管理 要想改变日志轮替文件名字 通过/etc/logrotate.conf 配置文件中 dateext 参数修改
- 如果配置文件中有 dateext参数 那么日志会用日期来作为文件名的后缀 例如 secure-20201010 这样日志文件不会重名 也就不需要日志文件的改名 只需要指定保存日志文件个数 删除多余的日志文件即可
- 如果配置文件中没有 dateext 参数 日志文件就需要改名了 当第一次日志轮替时 当前的 secure 日志会自动改名为secure.1 然后新建secure日志 用来保存新的日志 当第二次进行日志轮替时 secure.1会改名成secure.2 当前的secure会改成secure.1 以此类推

## logratate配置文件

```bash
# rotate log files weekly 每周对配置文件进行一次论题
weekly

# keep 4 weeks worth of backlogs 最多保存4个日志文件
rotate 4

# create new (empty) log files after rotating old ones 在日志轮替后 创建新的空日志文件
create

# use date as a suffix of the rotated file 使用日期作为日志轮替文件的文件名
dateext

# uncomment this if you want your log files compressed 日志文件是否压缩
#compress

# RPM packages drop log rotation information into this directory 包含/etc/logratate.d/目录中的所有子配置文件
include /etc/logrotate.d

#下面是单独配置 优先级更高
# no packages own wtmp and btmp -- we'll rotate them here
/var/log/wtmp {
    monthly #每周对日志文件进行一次论题
    create 0664 root utmp #建立新的日志文件 权限是0664 所有者是root 所属组是utmp组
	minsize 1M #日志的最小轮替大小是1MB
    rotate 1 #仅保留一个日志备份
}

/var/log/btmp {
    missingok #如果日志不存在 则忽略该日志的警告信息
    monthly
    create 0600 root utmp
    rotate 1
}
```

**也可以把某个日志的配置文件写到/etc/logratate.d中 比如**

```bash
[root@CentOS7 ~]# cat /etc/logrotate.d/bootlog
/var/log/boot.log
{
    missingok
    daily
    copytruncate
    rotate 7
    notifempty
}
```

## 自定义日志轮替

| 参数                      | 参数说明                      |
| ----------------------- | ------------------------- |
| daily                   | 每天轮替                      |
| weekly                  | 每周轮替                      |
| monthly                 | 每月轮替                      |
| rotate 数字               | 保留的日志文件个数 0表示不备份          |
| comperss                | 日志轮替时 旧日志是否压缩             |
| create mode owner group | 建立新日志 同时指定新日志的权限与所有者和所属组  |
| mail address            | 当日志轮替时 输出内容通过邮件发送到指定的邮件地址 |
| missingok               | 如果日志不存在 则忽略该日志的警告信息       |
| notifempty              | 如果日志为空文件 则不进行日志轮替         |
| minsize 大小              | 日志轮替的最小值                  |
| size 大小                 | 日志大于指定大小时才进行轮替            |
| dateext                 | 使用日期作为日志轮替文件的后缀           |
| sharedscripts           | 在此关键字后的脚本只执行一次            |
| prerotate/endscript     | 在日志轮替之前执行脚本命令             |
| postrotate/endscript    | 在日志轮替之后执行脚本命令             |
## 把自己的日志加入日志轮替

- 第一种方法是直接在/etc/logrotate.conf 配置文件中写入该日志的轮替策略
- 第二种方法是在/etc/logrotate.d/目录中新建该日志文件的轮替文件 在该轮替文件中写入正确的轮替策略 因为该目录中的所有文件都会被include到主配置文件中
- 推荐使用第二种方法

```txt
给adad.log添加日志轮替策略
```

```bash
vim /etc/logrotate.d/adadlog

#写入
/var/log/adad.log
{
	missingok
	daily
	copytruncate
	rotate 7
	notifempty
}
```
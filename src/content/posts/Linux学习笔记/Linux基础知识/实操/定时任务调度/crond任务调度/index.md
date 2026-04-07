---
title: "crond任务调度"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/Linux基础知识/实操/定时任务调度/crond任务调度/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## crond 任务调度

**crontab 进行定时任务的设置**

  **任务调度：是指系统在某个时间执行的特定的命令或程序**

  任务调度的分类：
  - 系统工作：有些重要的工作必须周而复始地执行 如病毒扫描等
  - 个别用户工作：个别用户可能希望执行某些程序 比如对mysql数据库的备份

```bash
#基本语法
crontab [选项]
#常用选项
-e 编辑crontab定时任务
-l 查询crontab任务
-r 删除当前用户所有的crontab任务
```

### 基本使用案例

```txt
需求：每分钟执行一次 ls -l /etc > /opt/tmp/to.txt
```

```bash
crontab -e
*/1 * * * * ls -l /etc/ > /opt/tmp/to.txt
```

### 5个占位符的说明

- 第一个是一小时当中的第几分钟 0-59
- 第二个是一天当中的第几小时 0-23
- 第三个是一个月当中的第几天 1-31
- 第四个是一年当中的第几月 1-12
- 第五个是一周当中的星期几 0-7 （0和7都代表星期日）

## crond时间规则

### 特殊符号的说明

- *  代表任何时间 比如第一个\* 就代表每一小时的每分钟都执行一次的意思
- , 代表不连续的时间 比如"0 8,12,16 \* \* \* 命令" 就代表在每天的8:00 12:00 16:00执行一次
- - 代表连续的时间范围 比如""0 5 \* \* 1-6 命令" 代表每周一到每周六的5:00执行一次
- \*/n 代表每隔多久执行一次 比如"\*/10 \* \* \* \* 命令" 代表每隔十分钟执行一次

### 特殊时间执行任务案例

```bash
45 22 * * * 命令 #每天的22:45执行
0 17 * * 1 命令 #每周一的17:00执行
0 5 1,15 * * 命令 #每月1号和15号的5:00执行
40 4 * * 1-5 命令 #每周一到周五的4:40执行
*/10 4 * * * 命令 #每天凌晨4:00 隔十分钟执行一次 注：5:00开始就失效了
0 0 1,15 * 1 命令 #每个月的1号和15号 还有每周一 凌晨0:00执行
```

### 实例

#### 实例1

```txt
每隔1分钟 就将当前的日期信息 追加到/tmp/mydate文件中
```

```bash
crontab -e
*/1 * * * * date >> /opt/tmp/mydate
```

#### 实例2

```txt
每隔1分钟 将当前日期和日历都追加到/opt/tmp/mycal文件中
```

**尝试用shell脚本来写**

```bash
vim my.sh

#写入
date >> /opt/tmp/mycal
cal >> /opt/tmp/mycal

#设置权限
chmod 744 /scripts/my.sh

#设置定时任务
crontab -e

#写入
*/1 * * * * ./root/scripts/my.sh
```

#### 实例3

```txt
每天凌晨2:00 将mysql数据库testdb 被分到文件中
指令为：mysqldump -u root -p密码 数据库 >> /home/db.bak
```

```bash
crontab -e

#写入
0 2 * * * mysqldump -u root -p root test.db > /home/db.bak
```

### crond 相关指令

```bash
crontab -r :终止任务调度
crontab -l :列举当前的任务调度
service crond restart :重启任务调度
```
---
title: "at任务调度"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/实操/定时任务调度/at任务调度/
categories:
  - Linux笔记
  - Linux基础知识
  - 实操
  - 定时任务调度
  - at任务调度
tags:
  - Study
---

## 基本介绍

- at命令是一次性定时计划任务 at的守护进程atd会以后台模式运行 检查作业队列来运行
- 默认情况下 atd守护进程每60秒检查作业队列 有作业时 会检查作业运行时间 如果时间与当前时间匹配 则运行此作业
- at命令是一次性定时计划任务 执行完一个任务后不再执行此任务了
- 在使用at命令的时候 一定要保证atd进程的启动 可以使用相关指令来查看 （查看命令 ps -ef | grep atd）

## 命令格式

```bash
at [选项] [时间] # 输入两次Ctrl + D 结束at命令的输入

#常用选项
-m 当指定的任务被完成后 给用户发送邮件 即使没有标准输出
-I atq的别名 -> 查询
-d atrm的别名 -> 删除
-v 显示任务将被执行的时间
-c 打印任务的内容到标准输出
-V 显示版本信息
-q <队列> 使用指定的队列
-f <文件> 从指定文件读入任务而不是从标准输入读入
-t <时间参数> 以时间参数的形式提交要运行的任务
```

## at时间定义

- 接受在当天hh:mm (小时:分钟) 式的时间指定 假如该时间已经过去 那么就放在第二天执行 例如: 04:00
- 使用midnight(深夜) noon(中午) teatime(饮茶时间 一般是下午四点) 等比较模糊的词语来指定时间
- 采用12小时计时制 即在时间后加上AM PM来说明上午还是下午 例如12pm
- 采用指定命令执行的具体日期 指定格式为: month day(月 日) 或 mm/dd/yy （月/日/年） 或 dd.mm.yy (日.月.年) 指定的日期必须跟在指定时间的后面 例如: 04:00 2021-03-1
- 使用相对计时法 指定格式为： now + count time-units now就是当前时间 time-units是时间单位 这里能够是minutes hours days weeks count是时间的数量 几天 几小时 例如： now + 5 minutes
- 直接使用today tomorrow 爱指定完成命令的时间

## at调度实例

### 实例1

```txt
2天后的下午5点执行 /bin/ls /home
```

```bash
at 5pm + 2 days

#输入
/bin/ls /home
```

### 实例2

```txt
明天17点钟 输出时间到指定文件内 比如/root/date100.log
```

```bash
at 5pm tomorrow

#输入
date > /root/date100.log
```

### 实例3

```txt
2分钟后 输出时间到指定文件内 比如/root/date200.log
```

```bash
at now + 2 minutes

#输入
date >> /toor/date200.log
```

### 实例4

```txt
删除编号为5的任务
```

```bash
atrm 5
```
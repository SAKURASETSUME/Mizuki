---
title: "统计访问量和连接数"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/Linux笔记/Linux基础知识/面试题/统计访问量和连接数/
categories:
  - Linux笔记
  - Linux基础知识
  - 面试题
  - 统计访问量和连接数
tags:
  - Study
---

```txt
分析日志t.log（访问量），将各个ip地址截取，并统计出现次数，并按从大到小排序（腾讯）
http://192.168.200.10/index1.html
http://192.168.200.10/index2.html
http://192.168.200.20/index1.html
http://192.168.200.30/index1.html
http://192.168.200.40/index1.html
http://192.168.200.30/order.html
http://192.168.200.10/order.html
```

```bash
#截取ip地址 按照/截取 截取第三段
cat /opt/interview/l.log | cut -d '/' -f 3

#排序
cat /opt/interview/l.log | cut -d '/' -f 3 | sort 

#统计
cat /opt/interview/l.log | cut -d '/' -f 3 | sort | uniq -c

#给出现次数从大到小排序
cat /opt/interview/l.log | cut -d '/' -f 3 | sort | uniq -c | sort -nr
```

```txt
统计连接到服务器各个ip情况 并按连接数从大到小排序
```

![ip情况](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/e46594199b02484ab10ac93dca75acf6~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp)

```bash
#查看连接情况 找状态是ESTABLISHED的
netstat -an

#过滤出状态是ESTABLISHED
netstat -an | grep "ESTABLISHED"

#把ip单独拿出来 awk那里的意思是 根据空格分割 打印出第5位
netstat -an | grep "ESTABLISHED" |  awk -F " " '{print $5}'

#继续分割 把端口去掉
netstat -an | grep "ESTABLISHED" |  awk -F " " '{print $5}' | awk -F ":" '{print $1}'

#统计连接数 并从大到小排序
netstat -an | grep "ESTABLISHED" |  awk -F " " '{print $5}' | awk -F ":" '{print $1}' | sort | uniq -c | sort -nr
```

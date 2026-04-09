---
title: "Linux笔记 - Linux基础知识 - 面试题 - 访问量排名和tcpdump"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

```txt
写出指令：统计ip访问情况，要求分析nginx访问日志（access.log），找出访问页面数量在前2位的ip（美团）
```

```bash
# 先查看内容 查看之后用awk把ip单独拿出来 排序之后计算访问个数 之后用head保留前两位
cat /opt/interview/access.log | awk -F " " '{print $1}' | sort | uniq -c | sort -nr | awk -F " " '{print $2}' | head -2
```

```txt
192.168.130.21 aaa.html
192.168.130.20 aaa.html
192.168.130.20 aaa.html
192.168.130.20 aaa.html
192.168.130.23 aaa.html
192.168.130.20 aaa.html
192.168.130.25 aaa.html
192.168.130.20 aaa.html
192.168.130.20 aaa.html
192.168.130.25 aaa.html
192.168.130.20 aaa.html
```




```txt
使用tcpdump监听本机，将来自ip192.168.29.1，tcp端口为22的数据，保存输出到tcpdump.log，用做将来数据分析（美团）
```

```bash
#验证当前装没装tcpdump
tcpdump

#监听网络设备
tcpdump -i ens33 host 192.168.29.1 and port 22

#写入日志
tcpdump -i ens33 host 192.168.29.1 and port 22 >> /opt/interview/tcpdump.log
```




```txt
常用的Nginx模块 用来做什么
```

```txt
rewrite模块，实现重写功能
access模块：来源控制
ssl模块：安全加密
ngx_http_gzip_module：网络传输压缩模块
ngx_http_proxy_module模块实现代理
ngx_http_upstream_module模块实现定义后端服务器列表
ngx_cache_purge实现缓存清除功能
```
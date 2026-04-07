---
title: "Linux笔记 - Linux基础知识 - 实操 - 网络配置 - 主机名 host映射"
category: "Linux笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 设置主机名

```bash
hostname #查看主机名

#修改文件在
vim /etc/hostname

#修改后 重启生效
```

## 设置hosts映射

**host作用：把域名解析成对应的IP地址进行访问**

**Windows下路径： C:\Windows\System32\drivers\etc\hosts**

**Linux下路径： etc/hosts 文件 指定**

## 主机名解析过程分析

### 什么是Host？

- 一个文本文件 用来记录IP和Hostname（主机名）的映射关系

### DNS

- DNS 就是Domain Name System的缩写 翻译过来就是域名系统
- 是互联网上作为域名和IP地址相互映射的一个分布式数据库

## 实际过程

- 浏览器先检查浏览器缓存中有没有用户输入的域名解析IP地址 有就先调用这个IP完成解析；如果没有 检查DNS解析器缓存 如果有 直接返回IP完成解析 这两个缓存 可以理解为 本地解析器缓存
- 一般来说 当电脑第一次成功访问某一网站后 在一定时间内 浏览器或操作系统会缓存他的IP地址（DNS解析记录） 如 在cmd窗口中输入

```bash
ipcnofig /displaydns #DNs域名解析缓存
ipconfig /flushdns #手动清理dns缓存
```

- 如果本地解析器缓存没有找到对应映射 检查系统中hosts文件中有没有配置对应的域名IP映射 如果有 则完成解析并返回
- 如果本地DNS解析器缓存和hosts文件中均没有找到对应的IP 则到域名服务DNS进行解析域
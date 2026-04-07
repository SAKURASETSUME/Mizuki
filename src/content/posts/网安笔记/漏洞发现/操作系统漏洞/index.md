---
title: "操作系统漏洞"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/漏洞发现/操作系统漏洞/
categories:
  - 网安笔记
  - 漏洞发现
  - 操作系统漏洞
tags:
  - Study
---

## 一、思维导图

![](https://cdn.nlark.com/yuque/0/2021/jpeg/2476579/1630153024103-5f1dad8d-6d6b-4ea0-8acb-fd00f7e399d0.jpeg)

## 二、探针

### 1、Goby

可以到官网下载，这里使用忍者系统虚拟机里的。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153049777-0f78f4e9-f7e9-4832-9281-8c92c124d65b.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508104520.png)

结果：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153049961-e1703a25-77d8-4f78-9259-e34a5076b764.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508112114.png)

### 2、Namp

Nmap --script=vuln 默认nse插件 Nmap vulscan vulners 调用第三方库探针 加入拓展扫描模块 https://cnblogs.com/shwang/p/12623669.html

扫描：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153049987-80a87056-5a5d-4f8a-96ac-11789ffef3ba.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508112422.png)

结果：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153050071-d9f0249a-a93f-4223-a09f-91c486d78918.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508112402.png)

### 3、Nessus

下载地址

https://pan.baidu.com/s/17uA2OmJbV_cDG2C6QnHqqA 提取码：cxd4

安装教程在文件里有。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153050180-00c92912-14b2-4337-bf1d-43d3e387d6e8.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508114727.png)

## 三、漏洞类型

### 1、远程执行

### 2、权限提升

### 3、缓冲区溢出

## 四、漏洞利用

0day交易

https://mrxn.net/share/0day-today.html

#### 1、Searchploit使用方法

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153050738-6b8b749b-d1af-4423-ae07-0dbe4418ac37.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508123731.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153051099-e5828784-205a-4362-88d4-eb1daaad236d.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508124342.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153051685-8a5a0f21-381b-4516-9951-4202a0441cc6.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508124622.png)

然后打开msfcosole，在Nessus上看一下开放的端口和漏洞。

#### 2、Metasploit

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153051907-516c5200-11a9-4f74-8328-d70b78df0710.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508124841.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153051892-9c4245f9-e7dc-492b-b538-07f6104e3732.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508124951.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153051997-7ce2bc44-a31e-4c45-a509-84938d8543d2.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508125108.png)

然后看一下靶机：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153052188-1fc53b0f-8b4e-4d64-b901-f3fa7ca3063e.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210508125136.png)

## 五、涉及资源

```
涉及资源：
https://nmap.org
https://gobies.org
https://www.cnvd.org.cn
https://www.seebug.org
https://www.exploit-db.com
https://github.com/scipag/vulscan
https://github.com/vulnersCom/nmap-vulners
https://github.com/offensive-security/exploitdb
https://www.cnblogs.com/shwang/p/12623669.html
https://blog.csdn.net/qq_38055050/article/details/80214684
https://pan.baidu.com/s/17uA2OmJbV_cDG2C6QnHqqA 提取码：cxd4
```

##

---
title: "JAVA反序列化"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/web漏洞/反序列化/JAVA反序列化/
categories:
  - 网安笔记
  - web漏洞
  - 反序列化
  - JAVA反序列化
tags:
  - Study
---

### 一、思维导图

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629877623325-c4349945-b0b1-48a0-8b9d-68b3b9c74743.png)

Java中API实现：

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629878012763-c1184b4c-36fc-43ae-8011-10904cc1c533.png)

### 二、序列化理解

```
#序列化和反序列化

序列化(Serialization): 将对象的状态信息转换为可以存储或传输的形式的过程。在序列化期间，对象将其当前状态写入到临时或持久性存储区。

反序列化：从存储区中读取该数据，并将其还原为对象的过程，成为反序列化。
```

### 三、演示案例

- Java 反序列化及命令执行代码测试
- WebGoat_Javaweb 靶场反序列化测试

  

  

**补充知识点**

下方的特征可以作为序列化的标志参考:

一段数据以`rO0AB`开头，你基本可以确定这串就是JAVA序列化base64加密的数据。

或者如果以aced开头，那么他就是这一段java序列化的16进制。|

  

#### webgoat反序列

```
jiang@ubuntu:~$ docker pull webgoat/webgoat-8.0
jiang@ubuntu:~$ docker run -d -p 8080:8080 webgoat/webgoat-8.0:latest
```

[http://10.1.1.7:8080/WebGoat/login](http://10.1.1.7:8080/WebGoat/login)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629880320441-1716fda7-b536-4a65-9d4c-c0a20a6f094b.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629886664541-12f82ed3-a7ad-4eac-8281-62ec2d5437b5.png)

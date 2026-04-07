---
title: "APP漏洞发现"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/漏洞发现/APP漏洞发现/
categories:
  - 网安笔记
  - 漏洞发现
  - APP漏洞发现
tags:
  - Study
---

## 一、导图

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630205496910-f4d1225a-0ece-415a-a6c0-a41d930ec434.png)

## 二、思路

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209238674-8366cf86-e09b-4d90-be59-1bcf16928070.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512122402.png)

## 三、案例演示

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209238666-4badbf2c-6446-4c83-8c7f-5956fbb6c703.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512124747.png)

### 1、抓包工具WEB协议面使用说明

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209238674-b7474631-5890-443e-a9b1-8222b8adbb81.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512124841.png)

配置

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209238682-75b9d589-178b-41a8-9397-4af1e0e03be7.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512125016.png)

打开和妹妹吃西瓜聊天的app，登录后随便点一点，看一看

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209238679-53544f04-be39-465f-9508-1ee17fd57003.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512125353.png)

### 2、茶杯Charles抓包工具

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209245487-f4bfb2e9-c55b-4412-a3b2-f9e97d8cc6f2.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512130244.png)

主要是获取url

电脑访问，被拦截：  
[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209245548-6cab1ac7-b63e-44fb-a5ee-f4270b4020bb.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512131122.png)

那就用安卓模拟器，抓下包，对比两种包有啥不同，进行伪造就完事了。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209245730-2c099ab3-e811-4ec6-bd39-708447a74640.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512131153.png)

### 3、抓包精灵

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209245920-b92542f9-c85d-4678-9321-448953ab197f.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512131356.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209245875-c41b659a-cdc4-4ed3-a493-5aeb620bd469.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512131426.png)

### 4、Wireshark抓包

其他的抓包软件可能只会抓HTTP比较鸡肋，可以用Wireshark捕获网络接口。各种协议都有了。

### 5、安卓逆向便捷APK一键提取URL演示

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209246488-1d2d8fab-3aea-4e3f-9fe5-698f48d41d5f.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512132037.png)

反编译后：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209246497-f056a1f0-9aaa-4396-8de4-e88d802319b2.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512132109.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209246676-0cd9a95b-c863-4af9-808d-4bf424e7c2e0.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512132129.png)

### 6、利用Burp筛选及联动功能打出军体拳

联动Xray或awvs

打开powershell，使用webscan 监听6666端口

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209246858-0dafd7df-8e16-409a-8ee7-a1ced5f4d472.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515144125.png)

在burp里设置

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209246896-054007c9-a21e-4fa0-bd67-b42001371dcb.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515143931.png)

模拟器这里配置到burp

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630209247406-6094cb52-2374-497d-a5e4-03764c2cf12b.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515144025.png)

然后burp就转发到xray那里。

## 四、wireshark过滤器

过滤源ip、目的ip。

在wireshark的过滤规则框Filter中输入过滤条件。如查找目的地址为192.168.101.8的包，ip.dst==192.168.101.8；查找源地址为ip.src==1.1.1.1

端口过滤。

如过滤80端口，在Filter中输入，tcp.port==80，这条规则是把源端口和目的端口为80的都过滤出来。使用tcp.dstport==80只过滤目的端口为80的，tcp.srcport==80只过滤源端口为80的包

协议过滤

比较简单，直接在Filter框中直接输入协议名即可，如过滤HTTP的协议

http模式过滤。

如过滤get包，http.request.method=="GET",过滤post包，http.request.method=="POST"

连接符and的使用。

过滤两种条件时，使用and连接，如过滤ip为192.168.101.8并且为http协议的，ip.src==192.168.101.8 and http。

**工作中，一些使用方式**

调整时间格式

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630211412908-8cc0836c-9911-402e-bdf0-a5bbf9024f4b.png)

然后再排序下。根据时间字段

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630211413125-3324e0cb-ed8d-4d2d-bcab-2a5d366bd238.png)

**根据端口过滤**

**服务端端口是7018，和客户端建立socket连接，根据服务端的端口找到2者通信的所有socket数据（客户端进入房间后会异常断开，判断是客户端导致的还是服务端导致的）**

**tcp.port==7018，最后的RST报文是服务端发起的，说明是服务端主动断开的，缩小问题范围**

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630211413046-73127564-1159-450f-83e6-d2a4bcc29e0b.png)

仅从抓包信息看是服务器的一个流量控制机制启动了。服务器发回rst位，同时win置为0，是告诉客户端不要发包。按tcp流控机制来说，此时客户端应该停止发包，直至服务器发送信息告诉客户端可以继续发送。

TCP连接:SYN ACK RST UTG PSH FIN  
三次握手：发送端发送一个SYN=1，ACK=0标志的数据包给接收端，请求进行连接，这是第一次握手；  
接收端收到请求并且允许连接的话，就会发送一个SYN=1，ACK=1标志的数据包给发送端，告诉它，可以通讯了，并且让发送端发送一个确认数据包，这是第二次握手；  
最后，发送端发送一个SYN=0，ACK=1的数据包给接收端，告诉它连接已被确认，这就是第三次握手。之后，一个TCP连接建立，开始通讯。

*SYN：同步标志  
同步序列编号(Synchronize Sequence Numbers)栏有效。该标志仅在三次握手建立TCP连接时有效。它提示TCP连接的服务端检查序列编号，该序列编号为TCP连接初始端(一般是客户端)的初始序列编号。  
在这里，可以把 TCP序列编号看作是一个范围从0到4，294，967，295的32位计数器。通过TCP连接交换的数据中每一个字节都经过序列编号。  
在TCP报头中的序列编号栏包括了TCP分段中第一个字节的序列编号。

  
*ACK：确认标志  
确认编号(Acknowledgement Number)栏有效。大多数情况下该标志位是置位的。TCP报头内的确认编号栏内包含的确认编号(w+1，Figure-1)为下一个预期的序列编号，同时提示远端系统已经成功接收所有数据。

*RST：复位标志  
复位标志有效。用于复位相应的TCP连接。

*URG：紧急标志  
紧急(The urgent pointer) 标志有效。紧急标志置位，

*PSH：推标志  
该标志置位时，接收端不将该数据进行队列处理，而是尽可能快将数据转由应用处理。在处理 telnet 或 rlogin 等交互模式的连接时，该标志总是置位的。

*FIN：结束标志  
带有该标志置位的数据包用来结束一个TCP回话，但对应端口仍处于开放状态，准备接收后续数据。

TCP的几个状态对于我们分析所起的作用。在TCP层，有个FLAGS字段，这个字段有以下几个标识：SYN, FIN, ACK, PSH, RST, URG.其中，对于我们日常的分析有用的就是前面的五个字段。它们的含义是：SYN表示建立连接，FIN表示关闭连接，ACK表示响应，PSH表示有 DATA数据传输，RST表示连接重置。  
其中，ACK是可能与SYN，FIN等同时使用的，比如SYN和ACK可能同时为1，它表示的就是建立连接之后的响应，如果只是单个的一个SYN，它表示的只是建立连接。  
TCP的几次握手就是通过这样的ACK表现出来的。但SYN与FIN是不会同时为1的，因为前者表示的是建立连接，而后者表示的是断开连接。  
RST一般是在FIN之后才会出现为1的情况，表示的是连接重置。一般地，当出现FIN包或RST包时，我们便认为客户端与服务器端断开了连接；  
而当出现SYN和SYN＋ACK包时，我们认为客户端与服务器建立了一个连接。  
PSH为1的情况，一般只出现在DATA内容不为0的包中，也就是说PSH为1表示的是有真正的TCP数据包内容被传递。TCP的连接建立和连接关闭，都是通过请求－响应的模式完成的。
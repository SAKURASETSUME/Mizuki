---
title: "数据包扩展"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/基础知识部分/数据包扩展/
categories:
  - 网安笔记
  - 基础知识部分
  - 数据包扩展
tags:
  - Study
---

### 1、http/https数据包

  

- **HTTP协议是什么？**

```
HTTP协议是超文本传输协议的缩写，英文是Hyper Text Transfer Protocol。它是从WEB服务器传输超文本标记语言(HTML)到本地浏览器的传送协议。
设计HTTP最初的目的是为了提供一种发布和接收HTML页面的方法。
HTPP有多个版本，目前广泛使用的是HTTP/1.1版本。
```

- **HTTP原理**

```
HTTP是一个基于TCP/IP通信协议来传递数据的协议，传输的数据类型为HTML 文件,、图片文件, 查询结果等。

HTTP协议一般用于B/S架构（）。浏览器作为HTTP客户端通过URL向HTTP服务端即WEB服务器发送所有请求。
```

- **HTTP特点**

```
http协议支持客户端/服务端模式，也是一种请求/响应模式的协议。

简单快速：客户向服务器请求服务时，只需传送请求方法和路径。请求方法常用的有GET、HEAD、POST。

灵活：HTTP允许传输任意类型的数据对象。传输的类型由Content-Type加以标记。

无连接：限制每次连接只处理一个请求。服务器处理完请求，并收到客户的应答后，即断开连接，但是却不利于客户端与服务器保持会话连接，为了弥补这种不足，产生了两项记录http状态的技术，一个叫做Cookie,一个叫做Session。

无状态：无状态是指协议对于事务处理没有记忆，后续处理需要前面的信息，则必须重传。
```

- **URI和URL的区别**

```
HTTP使用统一资源标识符（Uniform Resource Identifiers, URI）来传输数据和建立连接。

URI：Uniform Resource Identifier 统一资源标识符
URL：Uniform Resource Location 统一资源定位符
URI 是用来标示 一个具体的资源的，我们可以通过 URI 知道一个资源是什么。

URL 则是用来定位具体的资源的，标示了一个具体的资源位置。互联网上的每个文件都有一个唯一的URL。
```

- **HTTP报文组成**

1. 请求行：包括请求方法、URL、协议/版本
2. 请求头(Request Header)
3. 请求正文

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622351999792-48a14997-ba55-48d6-bccf-5e7cff123fce.png)

- **响应报文构成**

```
状态行
响应头
响应正文
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622352005270-f279fd02-7fee-4076-ab1c-d4b5749e301a.png)

- **常见请求方法**

```
GET:请求指定的页面信息，并返回实体主体。
POST:向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST请求可能会导致新的资源的建立和/或已有资源的修改。
HEAD:类似于get请求，只不过返回的响应中没有具体的内容，用于获取报头
PUT:从客户端向服务器传送的数据取代指定的文档的内容。
DELETE:请求服务器删除指定的页面。
```

**get请求**

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622352005311-d1d635ef-9e78-413b-b034-4cf5e442f53b.png)

  

**post请求**

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622351999710-b2f8274c-36b5-4739-8878-e5a5fb573629.png)

POST请求

**post和get的区别：**

```
都包含请求头请求行，post多了请求body。
get多用来查询，请求参数放在url中，不会对服务器上的内容产生作用。post用来提交，如把账号密码放入body中。
GET是直接添加到URL后面的，直接就可以在URL中看到内容，而POST是放在报文内部的，用户无法直接看到。
GET提交的数据长度是有限制的，因为URL长度有限制，具体的长度限制视浏览器而定。而POST没有。
```

**响应状态码**

```
访问一个网页时，浏览器会向web服务器发出请求。此网页所在的服务器会返回一个包含HTTP状态码的信息头用以响应浏览器的请求。
状态码分类：
1XX- 信息型，服务器收到请求，需要请求者继续操作。
2XX- 成功型，请求成功收到，理解并处理。
3XX - 重定向，需要进一步的操作以完成请求。
4XX - 客户端错误，请求包含语法错误或无法完成请求。
5XX - 服务器错误，服务器在处理请求的过程中发生了错误。
```

  

**常见状态码**：

```
200 OK - 客户端请求成功
301 - 资源（网页等）被永久转移到其它URL
302 - 临时跳转
400 Bad Request - 客户端请求有语法错误，不能被服务器所理解
401 Unauthorized - 请求未经授权，这个状态代码必须和WWW-Authenticate报头域一起使用
404 - 请求资源不存在，可能是输入了错误的URL
500 - 服务器内部发生了不可预期的错误
503 Server Unavailable - 服务器当前不能处理客户端的请求，一段时间后可能恢复正常。
```

  

**为什么要用https？**

实际使用中，绝大说的网站现在都采用的是https协议，这也是未来互联网发展的趋势。下面是通过wireshark抓取的一个博客网站的登录请求过程。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622351999972-3b2906df-6d12-42c1-9925-0fc70103e928.png)

可以看到访问的账号密码都是明文传输， 这样客户端发出的请求很容易被不法分子截取利用，因此，HTTP协议不适合传输一些敏感信息，比如：各种账号、密码等信息，使用http协议传输隐私信息非常不安全。

**一般http中存在如下问题：**

```
请求信息明文传输，容易被窃听截取。
数据的完整性未校验，容易被篡改
没有验证对方身份，存在冒充危险
```

**什么是HTTPS?**

为了解决上述HTTP存在的问题，就用到了HTTPS。

HTTPS 协议（HyperText Transfer Protocol over Secure Socket Layer）：一般理解为HTTP+SSL/TLS，通过 SSL证书来验证服务器的身份，并为浏览器和服务器之间的通信进行加密。

**那么SSL又是什么？**

SSL（Secure Socket Layer，安全套接字层）：1994年为 Netscape 所研发，SSL 协议位于 TCP/IP 协议与各种应用层协议之间，为数据通讯提供安全支持。

TLS（Transport Layer Security，传输层安全）：其前身是 SSL，它最初的几个版本（SSL 1.0、SSL 2.0、SSL 3.0）由网景公司开发，1999年从 3.1 开始被 IETF 标准化并改名，发展至今已经有 TLS 1.0、TLS 1.1、TLS 1.2 三个版本。SSL3.0和TLS1.0由于存在安全漏洞，已经很少被使用到。TLS 1.3 改动会比较大，目前还在草案阶段，目前使用最广泛的是TLS 1.1、TLS 1.2。

**SSL发展史（互联网加密通信）**

```
1994年NetSpace公司设计SSL协议（Secure Sockets Layout）1.0版本，但未发布。
1995年NetSpace发布SSL/2.0版本，很快发现有严重漏洞
1996年发布SSL/3.0版本，得到大规模应用
1999年，发布了SSL升级版TLS/1.0版本，目前应用最广泛的版本
2006年和2008年，发布了TLS/1.1版本和TLS/1.2版本
```

**浏览器在使用HTTPS传输数据的流程是什么？**

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622352000732-7741fa61-72b9-4a59-8f34-73a7c93618b0.png)

HTTPS数据传输流程

```
首先客户端通过URL访问服务器建立SSL连接。
服务端收到客户端请求后，会将网站支持的证书信息（证书中包含公钥）传送一份给客户端。
客户端的服务器开始协商SSL连接的安全等级，也就是信息加密的等级。
客户端的浏览器根据双方同意的安全等级，建立会话密钥，然后利用网站的公钥将会话密钥加密，并传送给网站。
服务器利用自己的私钥解密出会话密钥。
服务器利用会话密钥加密与客户端之间的通信。
```

**HTTPS的缺点**

```
HTTPS协议多次握手，导致页面的加载时间延长近50%；
HTTPS连接缓存不如HTTP高效，会增加数据开销和功耗；
申请SSL证书需要钱，功能越强大的证书费用越高。
SSL涉及到的安全算法会消耗 CPU 资源，对服务器资源消耗较大。
```

  

**总结HTTPS和HTTP的区别**

- HTTPS是HTTP协议的安全版本，HTTP协议的数据传输是明文的，是不安全的，HTTPS使用了SSL/TLS协议进行了加密处理。
- http和https使用连接方式不同，默认端口也不一样，http是80，https是443。

  

  

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622351185970-116d66cc-4c92-4357-a90a-8da4b4a724e2.png)

```
Request	请求数据包
Reponse	相应数据包
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622351304043-6cdce93e-612c-419c-84e5-d4a7e38ae49e.png)

```
#Requeset	请求数据包
#Proxy		代理服务器
#Reponse	相应数据包
代理的出现在接受数据包和发送数据包的时候提供了修改数据包的机会 
```

```
通信过程

1.浏览器建立与web服务器之间的连接
2.浏览器将请求数据打包（生成请求数据包）并发送到web服务器
3.web服务器将处理结果打包（生成响应数据包）并发送给浏览器

4.web服务器关闭连接

总结：
建立连接——>发送请求数据包——>返回响应数据包——>关闭连接

 

数据格式
请求数据包包含什么
1.请求行：请求类型/请求资源路径、协议的版本和类型
2.请求头：一些键值对，一般由w3c定义，浏览器与web服务器之间都可以发送，表示特定的某种含义

3.【空行】请求头与请求体之间用一个空行隔开；

4.请求体：要发送的数据(一般post方式会使用)；例：userName=123&password=123&returnUrl=/
```

**http与https的区别**

```
http通信过程

建立连接—>发送请求数据包—>返回响应数据包——>关闭连接1.浏览器建立与web服务器之间的连接
1.浏览器建立与web服务器之间的连接
2.浏览器将请求数据打包（生成请求数据包）并发送到web服务器
3.web服务器将处理结果打包（生成响应数据包）并发送给浏览器
4.web服务器关闭连接

```

### 2、windows安装burp

参考文档

配置Java环境

[https://www.runoob.com/java/java-environment-setup.html](https://www.runoob.com/java/java-environment-setup.html)

安装burp

  

### 3、burp代理设置

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622361703221-db163ed6-2786-4863-b0f6-91a2ac170ebe.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622361749422-69ad9e29-194f-4c03-892a-feead9dec183.png)

**第三方查询信息平台**

[http://ip.chinaz.com/](http://ip.chinaz.com/)

修改站长之家的返回信息

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622363323304-b57790ef-2191-4a2e-a70a-0b34e7cdf117.png)

**通过修改数据包改动页面上的信息**

修改之前的数据包

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622363377112-3d2ba263-5b89-414c-a5da-2740293003c5.png)

在修改的数据包不止一个是站长之家的信息还有百度地图的信息是为了获取我们Ip地址

我们修改user-agent信息把他改为111111

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622363712056-ce9cb946-88e0-4d91-8920-63002db4cf76.png)

这个操作没得任何的意义只是证明是网站是通过数据包访问

```
修改kali的网络源
cat >/etc/apt/sources.list <<EOF
# See https://www.kali.org/docs/general-use/kali-linux-sources-list-repositories/
#deb http://http.kali.org/kali kali-rolling main contrib non-free

# Additional line for source packages
# deb-src http://http.kali.org/kali kali-rolling main contrib non-free
#deb https://mirrors.aliyun.com/kali kali-rolling main non-free contrib
#deb-src https://mirrors.aliyun.com/kali kali-rolling main non-free contrib

deb http://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free
deb-src https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free

EOF

安装火狐中文环境
apt install firefox-esr-l10n-zh-cn
```

### 4、burp抓取https数据包

第一步在burp中将证书导出到本地

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622443869019-581d9452-1290-4a0a-8b9a-f2bde7da5b67.png)

第二步

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622443894138-03beeab0-f0c6-4f87-aca3-e6e1e3b7e472.png)

第三步

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622444024139-3fbf1b88-37bc-4626-b521-3851e208a2e1.png)

第四步

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622445298967-7190ae07-37f0-468f-a1f9-8b8de52361fb.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622445258297-1b85797a-3193-4dd2-b830-347190f65366.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622445393532-123efeb1-1108-4af7-aa29-efe58b9da6df.png)

### 5、burp抓取APP数据包
---
title: "CDN绕过方法"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/基础知识部分/CDN绕过方法/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

CDN的全称是Content Delivery Network，即内容分发网络。CDN是构建在现有网络基础之上的智能虚拟网络，依靠部署在各地的边缘服务器，通过中心平台的负载均衡、内容分发、调度等功能模块，使用户就近获取所需内容，降低网络拥塞，提高用户访问响应速度和命中率。但在安全测试过程中，若目标存在CDN服务，将会影响到后续的安全测试过程。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623216008707-d063e412-ff3d-4256-8b9d-8ef9ef41d219.png)

### 1、如何判断目标存在CDN服务?

```
利用多节点技术进行请求返回判断
	http://ping.chinaz.com/
 	http://ping.aizhan.com/
  http://ce.cloud.360.cn/
```

如果ping的结果只有一个那么就没有CDN、要是不止一个则可以判断为有CDN

没有使用CDN

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623217475468-cd530cb6-3c7d-45c6-8346-ec66dcc9993f.png)

使用CDN

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623217655187-bcd611f8-5ddc-4c9e-af74-05ab076501bb.png)

### 2、CDN对于安全测试有那些影响?

```
	cdn会隐藏服务器真实的ip地址，无法对目标网站的操作系统进行渗透，但cdn站点又可以理解为是目标站点的镜像站点（大多数都是静态cdn加速），拥有相同的网站架构，且cdn服务器可与站点服务器进行交互，因此sql注入，xss等漏洞的挖掘并不受太大影响。
```

### 3、目前常见的CDN绕过技术有哪些?

```
子域名查询：
					因为有些主站是做了CDN服务而子站是没有做CDN服务
邮件服务查询
					因为邮箱大部分都是内部人在访问、而且访问的量也不是很大，一般是没有做CDN。
国外地址请求
					因为很多的企业没有在国外部署CDN，要是用国外的地址请求、就容易找到他的真实地址。
遗留文件、扫描全网
					如PHPinfo信息当中会遗留出ip地址
黑暗引擎搜索
					fofa、傻蛋、谛听、zoomeye、censys
特定文件dns历史记录，以量打量

#CDN真实IP地址获取后绑定指向地址
更改本地HOSTS解析指向文件

奇淫技巧
	fackcdn w8fuckcdn	zmap
```

[  
](https://tools.ipip.net/cdn.php)

### 四、案例演示获取真实ip

#### 1、以学而思网站为例

`www.xueersi.com`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623221502624-1ad2b891-695a-4bb8-8aed-6d76a4af55d6.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623221515487-67a0826d-e508-431a-b414-1de25c938330.png)

`xuersi.com`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623221535716-9ffd1037-e88f-4fd3-88f4-da54ae6b4e15.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623221578304-dbf57d08-16b5-487c-9d68-7fb7a8473ee6.png)

备注：通过对比发现xueersi.com没有使用cdn直接获取到了真实的IP地址、而其中的IP地址71、72是负载均衡的访问入口。

验证获取到ip是否可信可以采用第三方的ip地址查询工具经行验证。

[https://get-site-ip.com/](https://get-site-ip.com/)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623221828776-c24014d7-9a2b-485a-ac5d-80e771185112.png)

#### 2、www.sp910.com

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623222180759-dd3fc90b-e5da-469b-923d-78ad27dfd383.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623222189256-f2153fc7-0a26-4df7-8190-1908ce782ece.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623222237005-e0383a26-4166-43c1-be1c-372a7ce60535.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623222252362-e5ddc8d7-0a32-4880-9c41-63085e82523a.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623222289371-e1764710-f9f8-4eeb-94c6-2eb7113e3a84.png)

#### 3、cdn网站

[https://tools.ipip.net/cdn.php](https://tools.ipip.net/cdn.php)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623720533766-d5412aec-bdcb-47fe-acde-02807483daf0.png)

  

  

`总结:`网站的cdn的绕过方法第三方工具或通过邮件的方式不一定完全靠谱还是要结合一定的社会工程学才能找到真实的IP地址。
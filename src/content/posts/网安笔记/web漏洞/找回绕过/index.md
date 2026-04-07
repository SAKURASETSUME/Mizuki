---
title: "找回绕过"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/web漏洞/找回绕过/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629182322161-1a6609f6-67c5-489d-a3ea-dfee7cc121bc.png?x-oss-process=image%2Fresize%2Cw_862%2Cresize%2Cw_862)

```
#找回重置机制
客户端回显，Response 状态值，验证码爆破，找回流程绕过等

#接口调用乱用
短信轰炸，来电轰炸等
```

### 演示案例：

- 找回密码验证码逻辑-爆破测试-实例
- 墨者靶场密码重置-验证码套用-靶场
- 手机邮箱验证码逻辑-客户端回显-实例
- 绑定手机验证码逻辑-Rep 状态值篡改-实例
- 某 APP 短信轰炸接口乱用-实例接口调用发包

  

### 涉及资源

```
http://downcode.com/downcode/j_16621.shtml

https://pan.baidu.com/share/init?surl=P73QFmEhY6f350CvmnOJNg 提取码小

https://pan.baidu.com/share/init?surl=N963jFjTefNc6Gnso-RHmw 提取码xiao

https://www.mozhe.cn/bug/detail/K2sxTTVYaWNncUE1cTdyNXIyTklHdz09bW96aGUmozhe
```

### 墨者靶场

漏洞分析原因

```
第一个页面：第一个页面输入手机号，验证码
第二个页面：重置密码

刚好靶场是这么一个流程 手机号 新密码 图片验证码,短信验证码

这样就行了一个后台更改数据包发送的手机号也就获取到了验证码
```

1、打开靶场进入操作界面，发现有一个已经注册的手机号

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629424977600-499a22d6-8b51-4180-84ce-cc0b1442362c.png)

2、使用测试号码获取短信验证码

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629425051854-a11c231e-7cb3-44ee-95c9-7e239bc617cc.png)

3、将手机号改为需要登录的手机号，点击重置，成功获取key值

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629425075353-ecb534f3-51a8-496b-bfba-8569eb26a50e.png)

其短信验证码5分钟内有效，只验证验证码的有效性，而没有验证验证码和手机号的一致性。所以可以越权重置。

### 汉川招聘网

[http://0712zpw.com/user/user_getpass.php](http://0712zpw.com/user/user_getpass.php)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629425832823-0e52abfe-b00f-451b-9ede-2a2171275603.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629425841657-dbf223a8-29cd-4b17-b6ea-74fdc8fb0a4f.png)

汉川招聘源码采用的是74cms，下载下来分析，切记不要直接在公网上直接开整，不然的话网安法问候

[https://74cms.com/downloadse/show/id/52.html](https://74cms.com/downloadse/show/id/52.html)  

### 手机验证码

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629428967366-691f8ea8-eddb-4d8a-8581-4efdc0c1c210.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629428997263-58b8f3ad-313a-466a-8cef-8e9c6fd26723.png)属于客户端回显。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629429048749-68b80b3e-dbe6-4620-be99-8b743479e839.png)

写个手机号码，然后随便填验证码，抓包。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629429048986-aedfbf92-6007-4f66-abfc-3e6c55e76861.png)

直接替换为正确的验证码就可以。或者也可以修改返回的包，

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629429048995-ee3411bd-03f6-447e-b434-cc6f360a693b.png)

在上面填写正确的验证码的情况下，返回1。而填写错误的验证码会返回3，我们将3修改为1即可。

但是这就涉及到，这个web应用到底是怎么验证的，是以返回包来验证，还是在服务器端验证。在服务器验证的话，改为1也没用。

bp抓取回复的数据包

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629429049897-2201f184-c93a-4cb0-b574-f0d52b4eddf3.png)

### 手机APP验证码
---
title: "httponly绕过"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/web漏洞/XSS跨站攻击/httponly绕过/
categories:
  - 网安笔记
  - web漏洞
  - XSS跨站攻击
  - httponly绕过
tags:
  - Study
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628132918301-6d92440b-aa98-4275-a9bf-b7f7658b568a.png?x-oss-process=image%2Fresize%2Cw_908)

### 1、什么是httponly

如果您在cookie中设置了HttpOnly属性，那么通过js脚本将无法读取到cookie信息，这样能有效的防止XSS攻击，但是并不能防止xss漏洞只能是防止cookie被盗取。

  

  

```
绕过 httponly：
浏览器未保存帐号密码：需要 xss 产生登录地址，利用表单劫持
浏览器保存帐号密码：浏览器读取帐号密
```

  

  

### 涉及资源

```
https://github.com/do0dl3/xss-labs
https://www.cr173.com/soft/21692.html
https://www.oschina.net/question/100267_65116
```

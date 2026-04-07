---
title: "网安笔记 - JAVA安全 - JWT安全以及预编译CASE注入"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 一、思维导图

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630119257487-b0d941ea-4d3f-435f-ab82-0506bf3daf8b.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630119283220-1db84bdf-c111-41e6-9f74-b6a5a22a9f3f.png)

## 二、SQL Injection

### 1、防御sql注入，其实就是session，参数绑定，存储过程这样的注入。

  

```
//利用session防御，session内容正常情况下是用户无法修改的：
select * from users where user = "'" + session.getAttribute("UserID") + "'";

//参数绑定方式，利用了sql的预编译技术
预编译讲解:https://www.cnblogs.com/klyjb/p/11473857.html

String query = "SELECT * FROM users WHERE last_name = ?";
PreparedStatement statement = connection.prepareStatement(query);
statement.setString(1,accountNmae);
ResultSet results = statement.executeQuery();

上面说的方式也不是能够绝对的进行SQL注入防御，只是减轻。
比如参数绑定的方式可以使用下面的方式绕过：
通过使用case when语句可以将order by后的orderExpression表达式中添加select语句。
```

### 2、案例：WEBGOAT sql注入

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630135910641-57923583-0225-4c3c-b297-d2ad457620fa.png)

```
GET /WebGoat/SqlInjectionMitigations/servers?column=ip HTTP/1.1
Host: 10.1.1.7:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
Connection: close
Referer: http://10.1.1.7:8080/WebGoat/start.mvc
Cookie: JSESSIONID=_aLW8RZKIBrdgr4Q8HZNyPnpZYKoGf9n0X272l6_
```

过关手册：[https://blog.csdn.net/u013553529/article/details/82765062](https://blog.csdn.net/u013553529/article/details/82765062)

## 三、JWT安全

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630136275222-a25e6e1a-32b8-4ddf-8d55-60110e4da714.png)

什么是 JWT？

```
JSON Web Token（JSON Web 令牌）是一种跨域验证身份的方案。JWT 不加密传输的数据，但能够通 过数字签名来验证数据未被篡改（但是做完下面的 WebGoat 练习后我对这一点表示怀疑）。 

JWT 分为三部分，头部（Header），声明（Claims），签名（Signature），三个部分以英文句号.隔开。 JWT 的内容以 Base64URL 进行了编码。  
```

```
头部（Header）
{
"alg":"HS256",
"typ":"JWT"
}

声明（Claims）
{
"exp": 1416471934,
"user_name": "user",
"scope": [
"read",
"write"
],
"authorities": [
"ROLE_ADMIN",
"ROLE_USER"
],
"jti": "9bc92a44-0b1a-4c5e-be70-da52075b9a84",
"client_id": "my-client-with-secret"
}

声明（Claims）
{
"exp": 1416471934,
"user_name": "user",
"scope": [
"read",
"write"
],
"authorities": [
"ROLE_ADMIN",
"ROLE_USER"
],
"jti": "9bc92a44-0b1a-4c5e-be70-da52075b9a84",
"client_id": "my-client-with-secret"
}
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630141464637-2f130fe7-ebaa-474d-8fe0-483746553570.png)

用普通用户tom登录，发现access_token为空，将数据包发送之后重新使用tom用户登录获取到access_token。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630142167249-8c350ebf-9dc2-478f-abf9-b07e4e65e12e.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630142254500-471ca11e-e323-45c3-9db5-ca035e4d3bb9.png)

使用在线jwt解码

[https://jwt.io/](https://jwt.io/)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630142326192-b40b7aff-2e5a-4e92-9ac3-414615c6b165.png)

[  
](https://www.cnblogs.com/darkerg/p/undefined)
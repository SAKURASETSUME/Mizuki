---
title: "网安笔记 - web漏洞 - 支付篡改"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629182322161-1a6609f6-67c5-489d-a3ea-dfee7cc121bc.png?x-oss-process=image%2Fresize%2Cw_862)

### 涉及知识

```
#登录应用功能点安全问题
检测功能点，检测，危害，修复方案等

1.登录点暴力破解
2.HTTP/HTTPS 传输
3.Cookie 脆弱点验证
4.Session 固定点测试
5.验证密文比对安全测试
#数据篡改安全问题
原理，检测，危害，修复等
参考：https://www.secpulse.com/archives/67080.html


#商品购买流程：
选择商品和数量-选择支付及配送方式-生成订单编号-订单支付选择-完成支付

#常见篡改参数：
商品编号 ID，购买价格，购买数量，支付方式，订单号，支付状态等

#常见修改方法：
替换支付，重复支付，最小额支付，负数支付，溢出支付，优惠券支付等

6000 大米测试产品
/index.php?m=Member&a=gobuy&iscart=0&id=127&name=%E5%A4%A7%E7%B1%B3%E6%B5%8B%E8%
AF%95%E4%BA%A7%E5%93%81&qty=1&price=6000&gtype=%E7%81%B0%E8%89%B2&pic=/Public/Uplo
ads/thumb/thumb_1393218295.jpg

5400 大米手机 cms
/index.php?m=Member&a=gobuy&iscart=0&id=70&name=%E5%A4%A7%E7%B1%B3%E6%89%8B%E6%9
C%BACMS&qty=2&price=5400&gtype=%E7%81%B0%E8%89%B2&pic=/Public/Uploads/thumb/thumb_13
93218295.jpg

index.php?s=/wap/pay/wchatQrcodePay 微信支付
index.php?s=/wap/pay/alipay 支付宝支付
index.php?s=http://www.xiaodi8.com/alipay 调用其他的支付接口

$pay_name=$_GET['s'];
6000 是存储到数据库里，安全的做法：以数据库的数据值为准
```

### 涉及资源

```
涉及资源：
https://www.zblogcn.com/zblogphp/
https://github.com/huyuanzhi2/password_brute_dictionary
https://pan.baidu.com/s/1fJaW23UdcXcSFigX0-Duwg 提取码：xiao
```

### zblog 密码爆破

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629338072676-eeab6d8a-73eb-4ca8-aecc-7dd6f0a13361.png)

安装完成后登陆地址：[http://localhost/zblog/zb_system/login.php](http://localhost/zblog/zb_system/login.php)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629338341679-3d391677-2fc2-4ef7-a815-58d9859362fa.png)

burp抓包爆破

备注一下一个小bug，由于之前一直是在虚拟机中搭建的靶场然后本地测试的，现在呢突然不想在虚拟机中搭建的靶场直接使用的宿主机搭建的，环境是phpstudy+Chrome+SwitchyOmega, 遇到的一个小bug就是SwitchyOmega代理本地的流量时直接使用127.0.0.1加端口，竟然获取不到流量，我还以为是我设置错了，但是这款工具相对来说还是可以不舍得放弃，就在网上找一些攻略终于找到解决方案，在不代理地址列表写上`<-loopback>`然后burp就可以正常的抓包了。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629339984274-ea098a13-d0f2-4e0c-a8de-87a17b4ab349.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629340183314-0346bb0c-6e58-42c5-b092-90b2594cfe10.png)

现在抓到zblog的登录数据，我们可以爆破用户名和密码，将数据包发送的intruder模块当中，设置变量。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629340519901-f5cab59b-66f6-415f-9cd7-e6ad319071f3.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629340543246-474952c7-7d06-4cd9-87a2-09d0c57a210e.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629340575754-12f98f27-cb6d-4eb4-8789-c2f082e225cf.png)

然后点击start，然后按照状态码排序或者是length排序

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629340761060-b329576d-9f78-4d05-a1ae-7cf67519a7a2.png)

也就是说看到的第65个请求是我们爆破成功的值，通过cmd5解密

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629341011578-2cb07728-ec47-476b-83f1-c8908c894a6d.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629341052131-634c0a14-475a-4cfd-8be2-0581f40343ff.png)

### cookie错弱点验证

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629341817653-9aa6b4a0-9862-4d00-a469-e22e94b9c4aa.png)

安装好cms之后我们访问后台登录地址

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629342100718-c69a8764-d316-4aa9-adf1-089eff46e25c.png)

抓包分析，这一串的cookie是浏览器的缓存信息

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629343437722-e810a2bd-1cf0-45ff-93d7-8b305c08ecf6.png)

在干净没有访问的过的环境当中是没有带cookie

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629343383432-0609ae74-c3a9-4483-981f-508643b97478.png)

源码分析

```
<?php
//单一入口模式
error_reporting(0); //关闭错误显示
$file=addslashes($_GET['r']); //接收文件名
$action=$file==''?'index':$file; //判断为空或者等于index
include('files/'.$action.'.php'); //载入相应文件
?>
```

这里的意思就访问这个文件传递参数r,参数r为空执行index否则接受file变量，然后加载对应的文件。files目录结构

```
adset.php
columnlist.php
commentlist.php
editcolumn.php
editlink.php
editsoft.php
editwz.php
imageset.php
index.php
linklist.php
login.php
manageinfo.php
newcolumn.php
newlink.php
newsoft.php
newwz.php
outlogin.php
reply.php
seniorset.php
siteset.php
softlist.php
wzlist.php
```

因为访问的index.php，在审计一下index.php文件,看到的是执行了以下两个文件，对这两文件进行查看。

```
<?php
require '../inc/checklogin.php';
require '../inc/conn.php';
$indexopen='class="open"';
?>
```

checklogin.php文件

```
<?php
$user=$_COOKIE['user'];
if ($user==""){
header("Location: ?r=login");
exit;	
}
?>
```

这里对user参数接受的cookie进行判断如果为空的话执行login.php程序，所以这里也就造成了若cookie登录的漏洞。

**实验演示：**

请求这个地址：[http://localhost/cookie/admin/?r=index](http://localhost/cookie/admin/?r=index) 并抓包分析。将cookie值改为`user=aaaaa`然后发送数据包

```
GET /cookie/admin/?r=index HTTP/1.1
Host: localhost
sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: user=aaaaaaaaa
Connection: close
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629345456680-aee2ceb6-cfab-4165-baf1-fcad5b7b0399.png)

总结：因为这个网站后台的首页的是index通过传参的方式验证登录。登录之前会对cookie进行验证验证由于方式很过于简单只是对cookie是否为空进行判断，也就是说传递的值不是为空程序就认为你是登录了，因此这就形成了弱cookie登录的漏洞。

上面的这种方式是基于白盒测试的方式，下面演示黑盒测试。

直接访问前台是没有带cookie的，当我们登录之前是没有任何的cookie的信息![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629346877532-059ca01f-1ebe-4ae8-b63d-cd49da3675ee.png)

当我们登录的数据包也是没有包含cookie信息，这里登录的时候会发送两个数据包。第一个是关于用户和密码第二个是cookie信息

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629347041159-7a798948-20e7-4f9c-90d9-7eb2931ba5b2.png)

我们观察到时用用户名作为cookie的信息，是相当的不安全也就是说这是一个可以伪造的cookie信息。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629347153056-3ca11d1b-da8f-419a-a0ae-13ab1578b6c1.png)

要是我们登录正确之后，访问后台信息，无论干什么都会发现一个cookie信息，用来标识身份

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629347287572-a07d635a-61f7-4b5b-8b7a-af8c6120da90.png)

在第二个数据包的时候我们看到了cookie登录信息要是我们伪造一个数据包将cookie信息发送会怎样呢？将数据包发送之后发现确实登录上后台了，也就验证了前面白盒测试的漏洞。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629355903414-c07274fa-ef1f-492f-88b7-0a3066236628.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629355920053-dd8316b7-cf08-413c-9ccc-a3b68f0d411b.png)

  

### shop脆弱支付

可利用漏洞：[https://www.secpulse.com/archives/67080.html](https://www.secpulse.com/archives/67080.html)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629362797275-4d0862b6-81a6-4858-89ca-a80286b009ab.png)

搭建好网站之后转包分析一手

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629363004631-e93d8e30-38bf-420f-91ab-927e54628cd0.png)

我们修改购买的数量为`-1`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629363167500-292d29df-b7a4-4d41-b08c-e2a2f4e54600.png)

**订单编号**

这里我们获取两个订单编码第一个是数量-1的订单编号第二个是订单数量30的订单编号。
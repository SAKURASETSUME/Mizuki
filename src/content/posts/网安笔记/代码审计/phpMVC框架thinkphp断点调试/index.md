---
title: "网安笔记 - 代码审计 - phpMVC框架thinkphp断点调试"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

# 一、思维导图

![](https://cdn.nlark.com/yuque/0/2022/webp/2476579/1647844675027-e63ddf0c-8481-4a12-b906-5874e16a3b16.webp)

1.文件上传漏洞挖掘：

- (1)关键字搜索（函数、键字、全局变量等）：比如$_FILES，move_uploades_file等
- (2)应该功能抓包：寻找任何可能存在上传的应用功能点，比如前台会员中心，后台新闻添加等。
- (3)漏洞举例：逻辑漏洞-先上传文件再判断后缀名，通过MIME类型来判断文件类型、前端校验文件类型而服务端未校验。

2.MVC开发框架类:：[https://www.cnblogs.com/wsybky/p/8638876.html](https://www.cnblogs.com/wsybky/p/8638876.html)

3.Thinkphp框架：[http://sites.thinkphp.cn/1556331](http://sites.thinkphp.cn/1556331)

4.phpstorm+xdebug调试：[https://blog.csdn.net/yinhangbbbbb/article/details/79247331](https://blog.csdn.net/yinhangbbbbb/article/details/79247331)

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647844721797-33df25f4-0e4c-4825-bbe4-a4025b84cd54.png)

# 二、演示案例

演示案例

- PHP文件上传全局变量$_FILES
- PHPStorm+xdebug断点调试演示
- Beescms无框架后台任意文件上传
- Finecms基于前台MVC任意文件上传
- Cltphp基于前台TP5框架任意文件上传

漏洞挖掘过程

- 搜索$_FILES-->后台中心-->上传图像-->跟踪代码-->逻辑判断
- 业务功能分析-->会员中心-->上传图像-->跟踪代码-->逻辑判断
- 搜索文件上传-->会员中心-->上传图像-->跟踪代码-->逻辑判断

# 三、beescms

## 没有测试到漏洞

1、官方下载Beescms v4.0,下载地址: [http://beescms.com/cxxz.html](http://beescms.com/cxxz.html)

2、解压压缩文件,然后把文件放到phpstudy的网站根目录

3、浏览器访问[http://localhost/beescms/install,](http://192.168.10.171/beescms/install,)开始安装

备注：笔者在安装安装的环境是windows+phpstudy2018，在安装的过程中莫名其妙的出现访问`403`

解决方案：**打开phpStudy，点击按键“其他选项菜单”=>找到phpStudy配置=>点击“允许目录列表”。最后重启phpStudy。**

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647857448459-5ab64a39-ce4a-4752-8408-d6ee5ea5baaa.png)

正常安装后

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647857590416-2e93e588-bf46-46e1-80fb-7dd55d71efff.png)

seasy代码审计，全局搜索-->`$_FILES`查找

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647858299998-6da1dbfa-5059-4ee9-96a5-eda59e7900ba.png)

`[http://127.0.0.1/beescms/admin/admin_file_upload.php](http://127.0.0.1/beescms/admin/admin_file_upload.php)`默认的用户名和密码都是`admin`

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647858436937-3c0b1f40-d5da-4cb7-bbf7-d4b0dcf4cddd.png)

上传一张图片，配合burpsuit抓包查看数据包内容

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647858782908-c117f5a0-30f8-4fe0-b926-139497b3afc7.png)

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647858814451-2f8f6a50-d90f-4698-9c62-1fdb267d20a6.png)

注意观察到有两个数据包名称`file_info`和`uppic`在seasy中查找这两个关键字

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647859042610-353782b9-fb61-421c-997e-72d91506a96f.png)

在文件中看到一个`up_file`函数这个是自定义的函数全局搜索可以看到函数的详细内容

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647860889916-8fd5c1e8-c8f4-41db-a60d-ecddfad51bd3.png)

后面发现一个`pathinfo`函数，是一个PHP只带的系统函数

```
<?php
$path_parts = pathinfo('/www/htdocs/inc/lib.inc.php');

echo $path_parts['dirname'], "\n";
echo $path_parts['basename'], "\n";
echo $path_parts['extension'], "\n";
echo $path_parts['filename'], "\n";
?> 
以上例程会输出：

/www/htdocs/inc
lib.inc.php
php
lib.inc
```

发现%00上传绕过失败

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647863398355-3e8b5a23-161e-4137-99c5-8938604c30fe.png)

## 测试到有漏洞

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647863461312-59b807e3-24b3-48d4-af9f-8bbb5d83fc6d.png)

看到这里只是限制了文件的类型，没有其他的限制，也就说这里可能存在MIME类型绕过。

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647863865365-636499ce-dfda-4281-adcd-dd264f3a5c40.png)

可以看到图片马已经上传成功

![](https://cdn.nlark.com/yuque/0/2022/png/2476579/1647864171642-312e5055-adde-4e29-bcdb-cc5c92f0da98.png)
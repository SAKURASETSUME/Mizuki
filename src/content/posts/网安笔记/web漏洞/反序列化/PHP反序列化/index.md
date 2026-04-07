---
title: "PHP反序列化"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/web漏洞/反序列化/PHP反序列化/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

### 一、思维导图

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629513452361-1d1b230d-7fad-4387-ae68-76a3da18a08c.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629513462778-724f3c0d-a1f6-412c-8cfa-4f4cac6d4586.png)

### 二、PHP反序列化

```
#PHP 反序列化
原理：未对用户输入的序列化字符串进行检测，导致攻击者可以控制反序列化过程，从而导致代码
执行，SQL 注入，目录遍历等不可控后果。在反序列化的过程中自动触发了某些魔术方法。当进行
反序列化的时候就有可能会触发对象中的一些魔术方法。

serialize() //将一个对象转换成一个字符串
unserialize() //将字符串还原成一个对象

触发：unserialize 函数的变量可控，文件中存在可利用的类，类中有魔术方法：

参考：https://www.cnblogs.com/20175211lyz/p/11403397.html

__construct()	//创建对象时触发
__destruct() 	//对象被销毁时触发
__call() 			//在对象上下文中调用不可访问的方法时触发
__callStatic() //在静态上下文中调用不可访问的方法时触发
__get() 			//用于从不可访问的属性读取数据
__set() 			//用于将数据写入不可访问的属性
__isset() 		//在不可访问的属性上调用 isset()或 empty()触发
__unset() 		//在不可访问的属性上使用 unset()时触发
__invoke() 		//当脚本尝试将对象调用为函数时触发
```

**无类测试**

- serialize

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629702598464-5fc46fbc-165e-4fe4-94ac-903265291b3f.png)

- unserialize

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629702950773-dd685602-5640-4632-9b1b-ad2eb8b95701.png)

**有类测试**

```
<?php
	class ABC{
    public $test;
    function __construct(){
        $test = 1;
        echo '调用了构造函数<br>';
    }
    function __destruct(){
        echo '调用了析构函数<br>';
    }
    function __wakeup(){
        echo '调用了苏醒函数<br>';
    }
}
echo '创建对象a<br>';
$a = new ABC;
echo '序列化<br>';
$a_ser=serialize($a);
echo '反序列化<br>';
$a_unser=unserialize($a_ser);
echo '对象快要死了！';
?>

运行结果
创建对象a<br>调用了构造函数<br>序列化<br>反序列化<br>调用了苏醒函数<br>对象快要死了！调用了析构函数<br>调用了析构函数<br>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629706689599-8340d273-a326-4ca3-81f0-1464a9e6c3dc.png)

### 三、ctf真题bugku

[https://ctf.bugku.com/challenges#flag.php](https://ctf.bugku.com/challenges#flag.php)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629704253019-9ac23b61-ebf7-46e0-80fa-03f8871f78df.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629704287765-4a0d78dc-5d8b-443e-bbc3-a80b916afc8b.png)

但是flag没有显示，原因是上面的请求了Hint。看源代码中的if和elseif，是这里的原因。

但是删除了?hint=1111之后，再请求，发现还是不对。原因是代码执行顺序的问题。这又是一个坑。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629704316818-2b4f73ca-1d3e-4c09-a484-25dd7c79b0aa.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210502120317.png)

所以我们传入Cookie的值应该为：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629704317436-5ca697f0-0e98-4e3e-923d-10c3a52c368a.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210502120442.png)

修改cookie

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629704317590-0203cfb1-4cd5-4f09-8668-af89495a543c.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210502120525.png)

得到flag

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629704317740-29d6a29f-7381-4c42-9f83-3d7915bd6c8c.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210502120504.png)
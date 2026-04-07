---
title: "web应用漏洞探针"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/漏洞发现/web应用漏洞探针/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

## 一、思维导图

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630153353093-df38faa7-35f1-4078-9431-92271562f68a.png)

## 二、站点判断

```
#已知 CMS
如常见的 dedecms.discuz,wordpress 等源码结构，这种一般采用非框架类开发，但也有少部分采用的
是框架类开发，针对此类源码程序的安全检测，我们要利用公开的漏洞进行测试，如不存在可采用
白盒代码审计自行挖掘。


#开发框架
如常见的 thinkphp，spring,flask 等开发的源码程序，这种源码程序正常的安全测试思路：先获取对
应的开发框架信息(名字，版本)，通过公开的框架类安全问题进行测试，如不存在可采用白盒代码审
计自行挖掘。


#未知 CMS
如常见的企业或个人内部程序源码，也可以是某 CMS 二次开发的源码结构，针对此类的源码程序测
试思路：能识别二次开发就按已知 CMS 思路进行，不能确定二次开发的话可以采用常规综合类扫描
工具或脚本进行探针，也可以采用人工探针（功能点，参数，盲猜），同样在有源码的情况下也可以
进行代码审计自行挖掘。
```

## 三、涉及资源

```
涉及资源：
https://vulhub.org/
https://wpvulndb.com/users/sign_up
https://github.com/wpscanteam/wpscan
https://github.com/ajinabraham/CMSScan
https://pan.baidu.com/s/1KCa-5gU8R8jPXYY19vyvZA 提取码：xiao
https://www.mozhe.cn/bug/detail/S0JTL0F4RE1sY2hGdHdwcUJ6aUFCQT09bW96aGUmozhe
```

## 四、CVE-2018-1273

```
$ cd spring/CVE-2018-1273
$ docker-compose up -d
```

[https://vulhub.org/#/environments/spring/CVE-2018-1273/](https://vulhub.org/#/environments/spring/CVE-2018-1273/)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630157772687-7f3a9933-ccda-40fd-9c66-f0a4c19db885.png)

```
root@a644ddd591a3:/# ls /tmp/success
/tmp/success
```

## 五、演示案例

 开发框架类源码渗透测试报告-资讯-thinkphp,spring

 已知 CMS 非框架类渗透测试报告-工具脚本-wordpress

 已知 CMS 非框架类渗透测试报告-代码审计-qqyewu_php

 未知 CMS 非框架类渗透测试报告-人工-你我都爱的 wg 哦~

### 1、已知CMS非框架类--WordPress

墨者靶场：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630158817638-b42d9ac1-a77b-4468-a1bb-237e8bfae346.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512111841.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630158817208-661663fc-5281-4e84-8b4e-93a8bba5822c.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512111931.png)

首先上来，不知道是啥cms，识别。但是这里已经提示。或者也可以从数据包中来找一些线索。

可以用wpscan工具，或者对应的cms的工具来测试使用。

网址：

wpscan.org https://github.com/wpscanteam/wpscan

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630158817633-459355a6-7330-4609-bc6a-d6accb2fa2dc.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512112430.png)

需要在官网弄个账号，获取token，配合上才能用他的漏洞库。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630158817635-44eb97e8-97da-431a-898e-1a86cf73b282.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512112520.png)

重新来

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630158817636-93a591d7-8b67-47a3-86cd-fd134ab07ad1.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512112637.png)

扫出漏洞：下好exp漏洞利用就行了。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630158818030-293ea503-5dc9-4cf6-9ab8-3fa8eafc4465.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512112706.png)

### 2、已知CMS非框架类---代码审计---qqyewu_php

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630160176235-69395486-dd32-498c-ac87-322eec48db74.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512113033.png)

代码审计

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630160176219-bd659261-7fd4-4e16-9e4f-ab5d0e585a83.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512115110.png)

### 3、真实案例

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630160176283-78eff06e-5964-4ec1-b908-9ef984ec76ec.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210512120753.png)

[https://www.855km.cn/e/admin/](https://www.855km.cn/e/admin/)


---
### 具体思路
先找找cms和框架什么的 去搜搜公开漏洞或者用工具扫 看看能不能直接搞一下
然后去看看功能 有没有web漏洞搞一搞
再不行就去扫一下端口看看 (有888和8888端口一般来说是宝塔)
再没有信息就爆目录 想办法给他备份文件搞过来 看看数据库配置文件 然后用navicat试试能不能外连 如果不行就再找找别的信息
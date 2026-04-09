---
title: "网安笔记 - 漏洞发现 - API接口漏洞发现"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 一、思维导图

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630212546733-d4c76855-654b-4539-9437-e28afea0dc22.png)

## 二、测试思路

```
信息收集之信息利用
第一步：首先识别网站是否有cdn，waf等产品，有则绕过。
第二步：扫描收集到网站的端口信息，真实ip地址，ip绑定的其他域名。
第三步：网站敏感路径扫描
第四步：域名+端口敏感信息扫描
第五步：ip+端口敏感目录扫描

备注：字典不应该只是敏感路径，还应该有备份文件 zip rar tar tar.gz等格式文件
```

```
#端口服务类安全测试
根据前期信息收集针对目标端口服务类探针后进行的安全测试，主要涉及攻击方法：口令安全，WEB
类漏洞，版本漏洞等，其中产生的危害可大可小。属于端口服务/第三方服务类安全测试面。一般在
已知应用无思路的情况下选用的安全测试方案。

#API 接口-WebServiceRESTful API
https://xz.aliyun.com/t/2412
根据应用自身的功能方向决定，安全测试目标需有 API 接口调用才能进行此类测试，主要涉及的安
全问题：自身安全，配合 WEB，业务逻辑等，其中产生的危害可大可小，属于应用 API 接口网络服
务测试面，一般也是在存在接口调用的情况下的测试方案。


WSDL（网络服务描述语言，Web Services Description Language）是一门基于 XML 的语言，用于描述
Web Services 以及如何对它们进行访问。

#漏洞关键字：
配合 shodan，fofa,zoomeye 搜索也不错哦~
inurl:jws?wsdl
inurl:asmx?wsdl
inurl:aspx?wsdl
inurl:ascx?wsdl
inurl:ashx?wsdl
inurl:dll?wsdl
inurl:exe?wsdl
inurl:php?wsdl
inurl:pl?wsdl
inurl:?wsdl
filetype:wsdl wsdl
http://testaspnet.vulnweb.com/acuservice/service.asmx?WSDL
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311118292-df9b427e-e0c8-4914-8369-f16cee0fc205.png)

## 三、演示案例

### 1、域名信息收集

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311229881-7f691fc7-68a7-4926-b5c9-15ae96a53c31.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515180426.png)

收集测试目标

域名访问和IP访问，目录可能会不同：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311230098-021be909-690b-46c2-abc1-39cccf2d84b8.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515180621.png)

收集时候不仅要扫描域名下的目录，还得扫描ip地址下的。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311229838-01400593-bf60-4774-af1f-a530943691f5.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515181029.png)

### 2、Goby端口扫描

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311167936-fc3a9551-a591-4ebc-af44-b96bc3f5361e.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515181615.png)

也可以用Nmap。

### 3、超级弱口令检测工具

下载地址：

https://github.com/shack2/SNETCracker/releases https://www.uedbox.com/post/57215/

界面：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311167958-b259bb8b-d1f2-4f70-9418-7609ac8ba9cf.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515182342.png)

前提是要支持外链，如果对方数据库是在内网，那就不行了。

## 四、网络服务

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311167931-070abf57-60a7-4345-b0ed-f8d005e3f84a.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515182830.png)

### WDSL语言

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311167848-c0db3ac7-9097-4550-abc3-7001db3b1830.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515183154.png)

#### ①API接口测试

xz.aliyun.com/t/2412

### AWVS扫描

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311167962-65449470-bd6d-4dd7-b6df-1602ccb6c8ec.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184020.png)

扫描出来的结果又SQL注入漏洞

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311168635-01ad3918-5312-42cd-9cc0-7b747b0e149c.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184301.png)

把数据包复制一下，在sqlmap安装目录，新建一个文档

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311168826-1a3dfc39-b7c4-4946-8cae-7466f2ceb241.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184337.png)

将数据包复制进去。

但是注意要把测试语句给删掉。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311168821-fb32d0d2-af17-4ddc-bbdb-cd4b77a8abd1.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184410.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311168815-52c8fbc5-e9b4-4cbd-96ed-becbfb5f499f.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184456.png)

sqlmap

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311168947-2c1cfccd-7d75-4e49-8cba-151c1b3a2f13.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184532.png)

--batch就是遇到yes or no的时候全部yes

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311169626-9a0076fd-a6db-4b9b-8a05-724f87885666.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184646.png)

列出表单

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311169644-cf5c7454-cf9d-4f92-a4a2-32664576ccb2.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184706.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630311169660-6bfe4540-2f11-4963-a6a4-14e3f27da033.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515184718.png)
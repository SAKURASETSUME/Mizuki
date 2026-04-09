---
title: "网安笔记 - WAF绕过 - 指纹探针"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

## 一、思维导图

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630374002096-80192c51-03ee-4cda-9c9a-5e4e2b0d3e70.png)

## 二、案例演示目录

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482238977-f9fe21c7-5a6c-4cf7-ad67-86047aae9644.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515225527.png)

## 三、代理池Proxy_pool项目搭建及使用解释

### 1、下载地址

先要安装Redis数据库，教程b站上有，可以参考一下。

https://github.com/jhao104/proxy_pool 安装依赖： pip install -r requirements.txt

## 四、充钱代理池直接干safedog+BT+Aliyun探针

### 1、快代理

https://www.kuaidaili.com/

买这种隧道代理的

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482237841-72c0f5dc-3689-4774-b83f-a4242d42ed75.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515231634.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482237977-6517bc34-3be7-408c-830e-00a444725b7f.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515231726.png)

配置到脚本中就可以了：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482237943-4b8c8746-40dd-4523-a77d-0d105b5414be.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515231811.png)

效果很好：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482237988-8489cf35-29e6-4c12-aeac-8936fe41da3f.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515231920.png)

查看宝塔日志：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482239054-6e41050e-ce4f-4654-9c38-708264a5ec63.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515231956.png)

拦截了别的ip hhh

## 五、Safedog-Awvs漏扫注入测试绕过-延时，白名单

### 1、本地测试

本地测试sqlilabs，并且本地的安全狗也是开启状态，cc防护也开了。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482239119-dadee2ec-20ca-4628-bbd0-558b049937e8.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515232432.png)

直接开扫：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482239976-975164ce-fccc-4996-94c1-bbd0abd56a23.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515232523.png)

速度很快会被安全狗拦截。可以修改User-Agent,也可以用bp拦截，然后通过按键精灵自己控制速度。

## 六、BT（baota）-awvs+xray漏扫Payload绕过

### 1、awvs配置

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482239222-69303a0e-5820-4e51-ac22-690f69ac8e3a.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516161713.png)

### 2、转发

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482241046-00855bc0-0809-401c-b7cb-fda874d114db.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516161756.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482240549-cb2fc0fc-96dd-4271-9419-1cca10faa724.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516161900.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482240653-1e77df15-c5d6-4cf8-b9cc-82415ad7132a.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516161911.png)

awvs转发给burp suite 然后再转发给xray。

## 七、充钱上代理池干

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482240624-5ebc00b6-7dd7-4811-ab0c-adfa3a398eb7.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516162211.png)

成功扫到了，迪哥讲课真有趣

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630482241065-16550052-4742-45db-a5bb-7c5e7246855c.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210516162439.png)
---
title: "网安笔记 - 基础知识部分 - 信息收集-APP"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

### 一、bp抓取手机数据包

手机IP地址：192.168.1.3

kali：192.168.1.9

burp配置

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623418667628-da931a3a-408e-4ce7-b9ea-c65e54188390.png)

手机配置

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623419674947-c5a9c6ff-9b1e-427e-b37e-59b86a196aed.png)

抓包测试

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623418954634-f32f5537-fba4-48a9-85d7-46a9d2d9bf19.png)

配置证书

在浏览器中输入192.168.1.9:8888下载证书并重名为ca.cer 然后导入

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623419652286-58cce6cf-d461-4de3-856b-924818c69562.png)

导入证书：设置-密码与安全-系统安全-加密与凭证-从sd卡安装-然后搜索ca.cer

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623419618483-57f88fc3-b83c-4a47-95ae-80828f3e1238.png)

抓包测试

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623419740073-68dc5d2a-5d72-4667-aadb-ad6007153c75.png)

### 二、对抓取的数据包进行分析

通过对抓取到的数据包进行分析、数据包上面可能有域名有ip地址。对上面的数据包进行信息收集、借助shodan、钟馗之眼、fofa等工具进行端口扫描

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623571180297-c66aa710-bd70-48c1-a079-12e0b4de60fa.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623571217679-1525c491-396c-422c-bc58-54e93c5008ca.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623571237218-018e9779-08f7-4ef1-a534-d19e7cbece34.png)
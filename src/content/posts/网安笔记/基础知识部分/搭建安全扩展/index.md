---
title: "网安笔记 - 基础知识部分 - 搭建安全扩展"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

### 1、涉及的知识点

- 常见搭建平台脚本启用
- 域名旧目录解析安全问题
- 常见文件后缀解析对应安全
- 常见安全测试中的安全防护
- WEB后门与用户及文件权限

  

### 2、常见的问题

```
#ASP,PHP,ASPx,JSP,PY,JAVAWEB等环境

#WEB源码中敏感文件
后台路径，数据库配置文件，备份文件等

#ip或域名解析wEB源码目录对应下的存在的安全问题
域名访问，IP访问（结合类似备份文件目录)

#脚本后缀对应解析（其他格式可相同-上传安全)
#存在下载或为解析问题

#常见防护中的IP验证，域名验证等

#后门是否给予执行权限

#后门是否给予操作目录或文件权限#后门是否给予其他用户权限

#总结下关于可能会存在的安全或防护问题?
```

### 3、web权限的设置

```
     在一般的情况下我们会对某个目录取消执行权限、最典型的就是图片目录这个目录只放图像没有脚本我们会取消执行的权限、这样我们可以防范一部分的文件上传漏洞、即使开发写的代码有问题也不会导致服务器出现安全事故。
     
     绕过方法：
     如果我们上传的文件如果不能正常的执行那么将文件放在其他目录、例如网站的根目录下面
```

### 4、演示案例-环境搭建

#### 1、PHPinfo

- 基于中间件的简要识别

一般可以通过抓包的方式分析出是什么类型的服务器和中间件

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622700527471-3a825366-e98b-45be-9572-c0920e247011.png)

可以看见在自己搭建的平台看见使用的apache(windows) php7.3

- 基于中间件的安全漏洞

可以根据在第一步上面收集到的信息、去找Apache的漏洞和PHP的漏洞

  

- 基于中间件的靶场使用

[https://vulhub.org/#/environments/](https://vulhub.org/#/environments/)

这个是用docker搭建的一个靶场非常的方便

环境搭建并测试,参考文档：[https://vulhub.org/#/docs/install-docker-one-click/](https://vulhub.org/#/docs/install-docker-one-click/)

第一步安装好docker环境并下载文件

```
[root@hdss7-11 ~]# docker -v
Docker version 20.10.6, build 370c289
[root@hdss7-11 ~]# docker-compose -v
docker-compose version 1.18.0, build 8dd22a9
[root@hdss7-11 ~]# cd /opt/vulhub/
[root@hdss7-11 vulhub]# wget https://github.com/vulhub/vulhub/archive/master.zip
```

第二步[https://vulhub.org/#/environments/](https://vulhub.org/#/environments/)查找你想做的环境

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622707451675-f5174469-2a23-4e9d-9b2a-d6bdc5629973.png)

```
[root@hdss7-11 vulhub]# cd vulhub-master/httpd/apache_parsing_vulnerability/
[root@hdss7-11 apache_parsing_vulnerability]# docker-compose up -d
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622707779631-f451c201-18e0-4689-8685-823bb22bc31e.png)

创建文件并命名为`x.php.jpeg`并上传

```
[root@hdss7-11 ~]# cat x.php.jpeg
<?php
       phpinfo();
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622708228398-8da74a73-5168-4203-ac82-8cd6d31e18d3.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622708358457-161dc652-8bfd-4312-ab9e-bc79a6330840.png)

#### 2、wordpress

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622708616162-5775e6c6-510e-4885-aa45-2c33b99d6666.png)

```
[root@hdss7-11 vulhub-master]# find . -name wordpress
./base/wordpress
./wordpress
[root@hdss7-11 vulhub-master]# cd wordpress/
[root@hdss7-11 wordpress]# cd pwnscriptum/
1.png  docker-compose.yml  exploit.py  README.md  README.zh-cn.md
[root@hdss7-11 pwnscriptum]# docker-compose up -d
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1622709589181-6af61eb1-96cd-479d-8616-89bf3a8f7e03.png)
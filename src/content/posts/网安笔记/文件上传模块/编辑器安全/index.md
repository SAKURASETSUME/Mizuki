---
title: "网安笔记 - 文件上传模块 - 编辑器安全"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

```
各个平台解析漏洞讲解IIS,Apache , Nginx

各个wEB编辑器安全讲解
https://navisec.it/编辑器漏洞手册/

各个cMS文件上传简要讲解
wordpress, phpcms
```

### apache解析漏洞

环境搭建：[https://vulhub.org/#/environments/httpd/apache_parsing_vulnerability/](https://vulhub.org/#/environments/httpd/apache_parsing_vulnerability/)

```
jiang@ubuntu:/opt/vulhub/vulhub-master/httpd/apache_parsing_vulnerability$ docker-compose up -d
/home/jiang/.local/lib/python2.7/site-packages/paramiko/transport.py:33: CryptographyDeprecationWarning: Python 2 is no longer supported by the Python core team. Support for it is now deprecated in cryptography, and will be removed in the next release.
  from cryptography.hazmat.backends import default_backend
Starting apache_parsing_vulnerability_apache_1 ... done
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627720368142-177eaaed-d2b6-4e7f-8c09-7be1d0515601.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627720403712-562bd531-2519-4b4a-9cc4-d6a8eaf453fa.png)

### 常见的编辑器

```
fckeditor		exp
ueditor 		漏洞利用
```

在网上找fckeditor漏洞`inurl:fckeditor site:edu.cn`

[https://blog.csdn.net/eldn__/article/details/9197521](https://blog.csdn.net/eldn__/article/details/9197521)

### 几种常见CMS文件上传简要演示

```
通达oA系统

https://pan.baidu.com/s/15gcdBuOFrN1F9xVN7Q7GSA 密码enqx
```

[https://www.cnblogs.com/twlr/p/12989951.html](https://www.cnblogs.com/twlr/p/12989951.html)

  

### 贴近实际应用下的以上知识点演示

```
判断中间件平台，编辑器类型或CMS名称进行测试
```
---
title: "web漏洞"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/基础知识部分/web漏洞/
categories:
  - 网安笔记
  - 基础知识部分
  - web漏洞
tags:
  - Study
---

前言:本章节将讲解各种WEB层面上的有那些漏洞类型,俱体漏洞的危害等级，以简要的影响范围测试进行实例分析，思维导图中的漏洞也是后面我们将要学习到的各个知识点，其中针对漏洞的形成原理，如何发现，如何利用将是本章节学习的重点内容!

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623721425978-e14463d7-40a4-4686-99e5-3ac03dfe8c33.png)

---

**简要知识点**

```
CTE,SRc，红蓝对抗，实战等

#简要说明以上漏洞危害情况
#简要说明以上漏洞等级划分
#简要说明以上漏洞重点内容
#简要说明以上漏洞形势问题
```

### 一、pikachu环境搭建

**靶场搭建：**[https://github.com/zhuifengshaonianhanlu/pikachu](https://github.com/zhuifengshaonianhanlu/pikachu)

**docker环境**

```
[root@oldjiang ~]# docker pull area39/pikachu
[root@oldjiang ~]# docker run -d -p8080:80 area39/pikachu
72ddd9a05d31fdb921765519c413f3f97dbb34560c9c14d9aa59de73e5d6b3eb
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623725817931-b6ba0eae-866c-4410-ba2b-0e09edaa7483.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623725840715-17108d47-0daf-4cf9-a4d9-a4b06c01e1e0.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623725858994-fab78038-e51a-439c-98c5-c27fb0bdc951.png)

### 二、sql注入之数字注入

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623726082542-3c0ab2c3-ac9d-47d9-aeb7-5eb283e338d4.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623726168437-2aea63ff-47d4-4bb6-b842-2eddfc326037.png)

  

在数据库中查看信息

```
mysql> select * from member;
+----+----------+----------------------------------+------+-------------+-----------------------+-------------------+
| id | username | pw                               | sex  | phonenum    | address               | email             |
+----+----------+----------------------------------+------+-------------+-----------------------+-------------------+
|  1 | vince    | e10adc3949ba59abbe56e057f20f883e | boy  | 18626545453 | chain                 | vince@pikachu.com |
|  2 | allen    | e10adc3949ba59abbe56e057f20f883e | boy  | 13676767767 | nba 76                | allen@pikachu.com |
|  3 | kobe     | e10adc3949ba59abbe56e057f20f883e | boy  | 15988767673 | nba lakes             | kobe@pikachu.com  |
|  4 | grady    | e10adc3949ba59abbe56e057f20f883e | boy  | 13676765545 | nba hs                | grady@pikachu.com |
|  5 | kevin    | e10adc3949ba59abbe56e057f20f883e | boy  | 13677676754 | Oklahoma City Thunder | kevin@pikachu.com |
|  6 | lucy     | e10adc3949ba59abbe56e057f20f883e | girl | 12345678922 | usa                   | lucy@pikachu.com  |
|  7 | lili     | e10adc3949ba59abbe56e057f20f883e | girl | 18656565545 | usa                   | lili@pikachu.com  |
+----+----------+----------------------------------+------+-------------+-----------------------+-------------------+
```

**操作方法**

- 在文件/app/vul/sqli/sqli_id.php第27行下面增加一行 echo $query; 然后保存退出

```
27 		$query="select username,email from member where id=$id";
28  			echo $query;
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623727035392-8bae692b-b5a8-4950-b78b-1b28a69f0307.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623727102875-ef393c8b-04ff-48cc-93d2-c1c85b87bd7d.png)

- 打开burp修改数据包

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623727977772-d60e637e-411b-47da-b0e5-1a83f7aad635.png)

- 获取到数据库信息

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623727870910-067e4d6b-2a8a-4b38-8eaa-fc5a2de6ea8a.png)

### 三、文件遍历漏洞

创建文件dir.php

```
root@eb8d8fc8a3e7:/app# pwd
/app
root@eb8d8fc8a3e7:/app# vim dir.php
root@eb8d8fc8a3e7:/app# pwd
/app
root@eb8d8fc8a3e7:/app# cat dir.php
<?php

function my_dir($dir) {
        $files = [];
        if(@$handle = opendir($dir)) {
                while(($file = readdir($handle)) !== false) {
                        if($file != ".." && $file != ".") {
                                if(is_dir($dir . "/" . $file)) { //如果是子文件夹，进行递归
                                        $files[$file] = my_dir($dir . "/" . $file);
                                } else {
                                        $files[] = $file;
                                }
                        }
                }
        closedir($handle);
    }
        return $files;
}

echo "<pre>";
print_r(my_dir("../app"));
echo "</pre>";
root@eb8d8fc8a3e7:/app# chmod +x dir.php
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623732208906-1be70b3b-2f4f-49ef-9bd0-64603ddb3051.png)

**备注：**目录遍历漏洞一般由其他的漏洞配合才能实现漏洞的作用。

### 四、文件上传漏洞

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623738344797-a82edfa6-f1c3-451a-a8ca-6a2607601c5d.png)

```
┌──(root💀kali)-[~/桌面]
└─# cat phpinfo.jpg                                                                                                                                                                     2 ⚙
<?php
phpinfo();
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623738441797-8fa3377f-832f-40f9-ad58-ad37e08b925e.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623738490937-30de4bcb-4317-4c99-a52d-6dad4fe2fb9f.png)

**注意：**文件上传一般是高危漏洞，因为要是上传的是木马文件可以直接拿下服务器。

### 五、文件下载漏洞

右击复制下载地址：[http://10.1.1.133:8080/vul/unsafedownload/execdownload.php?filename=kb.png](http://10.1.1.133:8080/vul/unsafedownload/execdownload.php?filename=kb.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623739441944-aab00923-c2a4-4830-9e35-24fa47e9548d.png)

在网站目录中查看

```
root@eb8d8fc8a3e7:/app/vul/unsafedownload/download# pwd
/app/vul/unsafedownload/download
root@eb8d8fc8a3e7:/app/vul/unsafedownload/download# ls
ai.png  bigben.png  camby.png  kb.png  lmx.png  mbl.png  ns.png  oldfish.png  pj.png  rayal.png  sks.png  smallane.png
```

修改下载文件

```
http://10.1.1.133:8080/vul/unsafedownload/execdownload.php?filename=../unsafedownload.php
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1623739668728-e80bb7e0-a4c1-44cf-9ec2-cc9785b06bc5.png)

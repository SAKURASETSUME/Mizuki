---
title: "pass-04"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/靶场实例/文件上传/uploadlabs/pass-04/
categories:
  - 网安笔记
  - 靶场实例
  - 文件上传
  - uploadlabs
  - pass-04
tags:
  - Study
---

老规矩 源码直接放上来

```php
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".php1",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".pHp1",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".ini");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //收尾去空

        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.$file_name;
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件不允许上传!';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

发现黑名单里过滤了pass03说过的php5等后缀 那么前面的方法就行不通了
我们来看下面的代码 可以发现 这里的文件名过滤都是只写了一次过滤 那么我们就把文件后缀名做一下调整 让它被修改之后变成我们想要的后缀就好了

比如这里 先去了一个空格 再删除了一个点 之后截取了.后面的字符串 转换为小写之后 去除了::$DATA 再去了一个空
以1.php为例 我们最后想要上传一个php后缀的文件 那么直接把后缀构造为"1.php. ." 根据这里写的过滤代码 php后面的.被删除 最后达到我们想要的效果
**在windows操作系统下修改后缀名为.php. .会被直接恢复成.php 要在burpsuite中修改文件名**


### 另一种思路
在Apache中有一个配置文件叫".htaccess" 这玩意可以直接实现在文件名中 有对应的字符串就可以直接把这个文件当做php解析
但是一般上传文件所在的路径是没有这玩意的 所以你要先上传一个.htaccess 再把代码中对应的字符串写在文件名上就可以绕过了
具体.htaccess的代码
```php
<FilesMatch "xxx">
 SetHandler application/x-httpd-php 
 </FilesMatch>
```

代码很简单 只要文件名有"xxx"这个字符串 那么这个文件就会被当做php解析 不管后缀是什么
---
title: "网安笔记 - 靶场实例 - 文件上传 - uploadlabs - pass-18"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

```php
$is_upload = false;
$msg = null;

if(isset($_POST['submit'])){
    $ext_arr = array('jpg','png','gif');
    $file_name = $_FILES['upload_file']['name'];
    $temp_file = $_FILES['upload_file']['tmp_name'];
    $file_ext = substr($file_name,strrpos($file_name,".")+1);
    $upload_file = UPLOAD_PATH . '/' . $file_name;

    if(move_uploaded_file($temp_file, $upload_file)){
        if(in_array($file_ext,$ext_arr)){
             $img_path = UPLOAD_PATH . '/'. rand(10, 99).date("YmdHis").".".$file_ext;
             rename($upload_file, $img_path);
             $is_upload = true;
        }else{
            $msg = "只允许上传.jpg|.png|.gif类型文件！";
            unlink($upload_file);
        }
    }else{
        $msg = '上传出错！';
    }
}
```
这里是个白名单的代码

直接来看这串代码
```php
if(move_uploaded_file($temp_file, $upload_file)){
        if(in_array($file_ext,$ext_arr)){
             $img_path = UPLOAD_PATH . '/'. rand(10, 99).date("YmdHis").".".$file_ext;
             rename($upload_file, $img_path);
             $is_upload = true;
        }else{
            $msg = "只允许上传.jpg|.png|.gif类型文件！";
            unlink($upload_file);
        }
    }else{
        $msg = '上传出错！';
    }
```

可以看出 这串代码有一个逻辑漏洞:
```markdown
它是先把文件进行了移动 再判断后缀名是否符合白名单的
```
操作系统有这么一个特性:
**当你的进程被占用时 它是无法被修改或删除的**

从以下这条代码可以分析出
```php
if(move_uploaded_file($temp_file, $upload_file))
```
在进行白名单过滤前 你的文件已经传到了服务器了 再利用一下操作系统的特性 一直去访问你传到服务器的文件 防止这条语句执行
```php
else{
            $msg = "只允许上传.jpg|.png|.gif类型文件！";
            unlink($upload_file);
        }
```

unlink函数就是删除文件的意思 但是当你用浏览器访问1.php时 1.php是处于被占用状态 操作系统无法删除

具体操作方法:
用burpsuite抓下包 然后直接把X-FORWORD这个头部设置一个变量 进行多次上传 同时在浏览器多次访问文件去占用这个文件就好了
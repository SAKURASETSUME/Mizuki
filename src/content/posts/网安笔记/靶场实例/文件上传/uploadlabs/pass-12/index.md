---
title: "网安笔记 - 靶场实例 - 文件上传 - uploadlabs - pass-12"
category: "网安笔记"
date: 2025-11-04
published: 2025-11-04
author: "Rin"
---

骚话想不出来了 直接看吧

```php
$is_upload = false;
$msg = null;
if(isset($_POST['submit'])){
    $ext_arr = array('jpg','png','gif');
    $file_ext = substr($_FILES['upload_file']['name'],strrpos($_FILES['upload_file']['name'],".")+1);
    if(in_array($file_ext,$ext_arr)){
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $img_path = $_GET['save_path']."/".rand(10, 99).date("YmdHis").".".$file_ext;

        if(move_uploaded_file($temp_file,$img_path)){
            $is_upload = true;
        } else {
            $msg = '上传出错！';
        }
    } else{
        $msg = "只允许上传.jpg|.png|.gif类型文件！";
    }
}
```

这关开始写白名单绕过了 并且过滤也写了循环过滤 是很标准的白名单过滤代码
那么有同学就要问了"哥们哥们这白名单怎么过啊 我传什么都传不上去啊"
诶 你先别急 我们的操作系统总能整点阴间活出来给大伙乐乐

%00这东西是个截断字符 比如你传了个1.php%00.jpg进去 那么传到后端 经过函数处理之后就会变成1.php 直接看这串代码
```php
$img_path = $_GET['save_path']."/".rand(10, 99).date("YmdHis").".".$file_ext;
```
检测的是$file_ext 那你直接在数据包的**filename和upload/后的路径**把后缀名改成.php%00.jpg就好了
**如果以POST请求提交 要把%00进行URL解码**
不过这东西挺过气的 它前提条件是php 5.3以下 而且magic_quote_gpc要关着才能用
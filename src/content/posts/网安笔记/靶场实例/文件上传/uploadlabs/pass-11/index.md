---
title: "pass-11"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/靶场实例/文件上传/uploadlabs/pass-11/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

那个男人回来了

```php
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array("php","php5","php4","php3","php2","html","htm","phtml","pht","jsp","jspa","jspx","jsw","jsv","jspf","jtml","asp","aspx","asa","asax","ascx","ashx","asmx","cer","swf","htaccess","ini");

        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = str_ireplace($deny_ext,"", $file_name);
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $img_path = UPLOAD_PATH.'/'.$file_name;        
        if (move_uploaded_file($temp_file, $img_path)) {
            $is_upload = true;
        } else {
            $msg = '上传出错！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

这关也是个经典绕过方法 看这串代码
```php
 $file_name = str_ireplace($deny_ext,"", $file_name);
```

这串代码的意思是把"$file_name"中 能匹配到黑名单这个数组中的字符串直接替换为空 就比如1.php->1.
但是他只做了一次过滤 那就简单了 我们最后想传过去的是1.php 那么我们直接构造个1.pphphp就好了 php替换为空后1.pphphp就变成1.php了
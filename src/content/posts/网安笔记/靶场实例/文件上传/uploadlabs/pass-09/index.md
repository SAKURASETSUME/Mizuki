---
title: "pass-09"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/靶场实例/文件上传/uploadlabs/pass-09/
categories:
  - 网安笔记
  - 靶场实例
  - 文件上传
  - uploadlabs
  - pass-09
tags:
  - Study
---

来了来了
```php
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess",".ini");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = trim($file_ext); //首尾去空
        
        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件类型不允许上传！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

这里发现他这次没写::$DATA的过滤 这玩意是个什么呢

```markdown
在windows操作系统中，当你看到文件名后面跟着 ::$DATA 时，它表示一个文件的附加数据流，数据流是一种在文件内部存储额外数据的机制。
```

说白了同样也是windows的一个特性 直接用就行了 加在后缀名后面就好了 这玩意在解析后缀时不会影响前面
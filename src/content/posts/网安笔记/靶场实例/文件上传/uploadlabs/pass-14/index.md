---
title: "pass-14"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/靶场实例/文件上传/uploadlabs/pass-14/
categories:
  - 网安笔记
  - 靶场实例
  - 文件上传
  - uploadlabs
  - pass-14
tags:
  - Study
---

```php
function getReailFileType($filename){
    $file = fopen($filename, "rb");
    $bin = fread($file, 2); //只读2字节
    fclose($file);
    $strInfo = @unpack("C2chars", $bin);    
    $typeCode = intval($strInfo['chars1'].$strInfo['chars2']);    
    $fileType = '';    
    switch($typeCode){      
        case 255216:            
            $fileType = 'jpg';
            break;
        case 13780:            
            $fileType = 'png';
            break;        
        case 7173:            
            $fileType = 'gif';
            break;
        default:            
            $fileType = 'unknown';
        }    
        return $fileType;
}

$is_upload = false;
$msg = null;
if(isset($_POST['submit'])){
    $temp_file = $_FILES['upload_file']['tmp_name'];
    $file_type = getReailFileType($temp_file);

    if($file_type == 'unknown'){
        $msg = "文件未知，上传失败！";
    }else{
        $img_path = UPLOAD_PATH."/".rand(10, 99).date("YmdHis").".".$file_type;
        if(move_uploaded_file($temp_file,$img_path)){
            $is_upload = true;
        } else {
            $msg = "上传出错！";
        }
    }
}
```

从这一关开始 往后几关要传图片马上去 制作图片马的程序也很简单 说白了就是直接在图片中加上后门代码就好了
**图片马一般要配合文件包含漏洞使用 因为上传的是图片 无法直接当做php执行**

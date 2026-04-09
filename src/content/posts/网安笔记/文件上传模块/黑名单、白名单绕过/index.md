---
title: "网安笔记 - 文件上传模块 - 黑名单、白名单绕过"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627433334141-cb693e43-53e8-4e28-80b9-b2c08e23f2f6.png?x-oss-process=image%2Fresize%2Cw_752)

```
文件上传常见验证:
后缀名，类型，文件头等
后缀名:黑名单,白名单
文件类型:MIME
信息文件头:内容头信息

简要上传表单代码分析解释
```

[https://www.jianshu.com/p/befa8f0ad5c8](https://www.jianshu.com/p/befa8f0ad5c8)

[https://blog.csdn.net/m0_46436640/article/details/107809772](https://blog.csdn.net/m0_46436640/article/details/107809772)

### PHP函数

```
trim() 函数移除字符串两侧的空白字符或其他预定义字符。

str_ireplace() 函数替换字符串中的一些字符（不区分大小写）。

substr() 函数返回字符串的一部分。

strrpos() 函数查找字符串在另一字符串中最后一次出现的位置。

```

### 第一关

```
function checkFile() {
    var file = document.getElementsByName('upload_file')[0].value;
    if (file == null || file == "") {
        alert("请选择要上传的文件!");
        return false;
    }
    //定义允许上传的文件类型
    var allow_ext = ".jpg|.png|.gif";
    //提取上传文件的类型
    var ext_name = file.substring(file.lastIndexOf("."));
    //判断上传文件类型是否允许上传
    if (allow_ext.indexOf(ext_name + "|") == -1) {
        var errMsg = "该文件不允许上传，请上传" + allow_ext + "类型的文件,当前文件类型为：" + ext_name;
        alert(errMsg);
        return false;
    }
}
```

只是后缀的验证抓包修改后缀即可

创建php.png文件里面写入内容,然后上传burp抓包将php.png修改为php.php,再把数据包发送，最后在浏览器中右击复制文件地址

```
<?php
phpinfo();
?>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627527361798-cfa1f6cc-4cb3-4771-881c-c7752e0942b5.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627527437621-c4f5ca58-d839-4240-bc92-06856caed809.png)

### 第二关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        if (($_FILES['upload_file']['type'] == 'image/jpeg') || ($_FILES['upload_file']['type'] == 'image/png') || ($_FILES['upload_file']['type'] == 'image/gif')) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH . '/' . $_FILES['upload_file']['name']            
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '文件类型不正确，请重新上传！';
        }
    } else {
        $msg = UPLOAD_PATH.'文件夹不存在,请手工创建！';
    }
}
```

第二关有两种绕过方式

- 将后缀名修改为符合要求的后缀名然后发送，在burp中将后缀修改为php
- 以后缀名为PHP直接发送，在浏览器中修改MIME类型为`image/jpeg`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627527943264-62ef531f-8591-457a-a411-e46918847f06.png)

### 第三关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array('.asp','.aspx','.php','.jsp');
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //收尾去空

        if(!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;            
            if (move_uploaded_file($temp_file,$img_path)) {
                 $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '不允许上传.asp,.aspx,.php,.jsp后缀文件！';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

这一关很明显是一个黑名单的方式但是并不是很严谨，可以phtml，php3，php4, php5, pht的这种格式绕过通关大小写的方式绕过，但是前提是要在配置文件里面有这样的一句话

```
AddType application/x-httpd-php .php .phtml .phps .php5 .pht
```

不然的话即使能上传上去也不能正常解析执行，因为服务器不知道这个是什么执行。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627528928771-ccd94930-d404-448d-b816-166639398129.png)

### 第四关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2","php1",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2","pHp1",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //收尾去空

        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
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

这个也是黑名单的方法比之前的方法严格多了，按照上一关的方式不可能突破，这一关先上传`.htaccess` 文件在上传一张图片中包含PHP代码的文件

```
<FilesMatch "gg.jpg">
SetHandler application/x-httpd-php
</FilesMatch>  
```

命名为.htaccess这个文件是伪静态文件也就是说，将文件中含有gg.jpg文件用PHP代码解析执行

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627530201051-6f865eab-8cf5-4b23-8d69-5b82f2425c70.png)

在上传一张gg.jpg包含php代码的文件

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627530259108-f8e40df8-9477-4392-860d-4509fbe017bd.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627530286234-9feaca50-83c6-4416-a064-a7100c8542da.png)

### 第五关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
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

对比上面的文件发现少了一行转换为小写的代码，对此我们可以采用大小写绕过，但是由于Linux是大小写敏感上传的文件不能被正常的执行，在windows上是可以正常的执行。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627531294534-a87ce662-0777-48b7-bd06-562475899e31.png)

也就发现即使上传上去也不能正常执行，这是由于Linux系统特性的原因。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627531328206-81dbfa99-aa83-49fe-82ce-1a7841124b5d.png)

### 第六关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = $_FILES['upload_file']['name'];
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        
        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
            if (move_uploaded_file($temp_file,$img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = '此文件不允许上传';
        }
    } else {
        $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
    }
}
```

比上一关少了一行首尾去空的代码，`后缀名+空格的形式去绕过`，注意：虽然能绕过上传但是并不会被服务器解析执行这是由于Linux系统特性，他不会像windows那样将文件后面的的空格给强制取消。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627542389612-7f03d400-a0db-45aa-b1ab-104894280382.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627542422974-25100a49-7678-4788-b1be-4e7e05e7fc4e.png)

### 第七关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_ext = strrchr($file_name, '.');
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //首尾去空
        
        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.$file_name;
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

可以看到的是只是对文件后面的一个点做了限制，在上传的时候多加一个点就能绕过限制，同样由于Linux服务器的原因他并不会将后面的`.`给截掉也就是说虽然能绕过但是没办法利用。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627542794579-1fb6ae63-aaa5-4a74-914b-55b37647b0cf.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627542920977-41919fd2-da80-4737-8b10-8c18acfc89c9.png)

### 第八关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
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

同样类型是Linux服务器的原因代码没法被执行

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627543193832-b141946b-dddc-4f04-867e-8c7e2b1c9803.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627543204194-dcf0f6c1-bcaf-4767-a33a-efa49c14551a.png)

### 第九关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
        $file_name = trim($_FILES['upload_file']['name']);
        $file_name = deldot($file_name);//删除文件名末尾的点
        $file_ext = strrchr($file_name, '.'); 		// 获取文件后缀名
        $file_ext = strtolower($file_ext); //转换为小写
        $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
        $file_ext = trim($file_ext); //首尾去空
        
        if (!in_array($file_ext, $deny_ext)) {
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.$file_name;
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

按照上面写的可以将文件的后缀名设置为`phP. .` 绕过但同时由于Linux的原因代码无法被正常的执行

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627544413259-b17880cc-1f38-4a4c-841f-8420f2a7eb7d.png)

### 第十关

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])) {
    if (file_exists(UPLOAD_PATH)) {
        $deny_ext = array("php","php5","php4","php3","php2","html","htm","phtml","pht","jsp","jspa","jspx","jsw","jsv","jspf","jtml","asp","aspx","asa","asax","ascx","ashx","asmx","cer","swf","htaccess");

        $file_name = trim($_FILES['upload_file']['name']); //函数移除字符串两侧的空白字符
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

这里的代码对文件名进行修改为`old.pphphp`在线工具当中可以看到函数是直接将`old.pphphp`解析为了php后缀

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627552092280-bbab028d-028f-4ff9-9b03-d1613263965d.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627552179488-b103a466-d758-4631-bff2-6d427db04333.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627552217613-4272c6d4-1fdb-4979-bf42-68be05b6d42b.png)

### 第十一关

```
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

strrpos() 函数查找字符串在另一字符串中最后一次出现的位置。

substr() 函数返回字符串的一部分。  

1. 关键的代码在于这里的’save_path’是一个可控的变量，但是后面还拼接上一个后缀名，也需要绕过

```
$img_path = $_GET['save_path']."/".rand(10, 99).date("YmdHis").".".$file_ext;
```

2. 这个时候可以使用%00截断，但这东西有点过气了，因为需要两个条件

```
php版本小于5.3.4
php的magic_quotes_gpc为OFF状态
```
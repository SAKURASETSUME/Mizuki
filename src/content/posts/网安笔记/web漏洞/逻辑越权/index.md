---
title: "网安笔记 - web漏洞 - 逻辑越权"
category: "网安笔记"
date: 2025-11-04
published: 2025-11-04
author: "Rin"
---

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629182322161-1a6609f6-67c5-489d-a3ea-dfee7cc121bc.png)

### 原理说明

```
 #水平，垂直越权，未授权访问 
 解释，原理，检测，利用，防御等 
 通过更换的某个 ID 之类的身份标识，从而使 A 账号获取（修改、删除等）B 账号数据。 
 使用低权限身份的账号，发送高权限账号才能有的请求，获得其高权限的操作。 
 通过删除请求中的认证信息后重放该请求，依旧可以访问或者完成操作。  


原理： 
前端安全造成：界面 
判断用户等级后，代码界面部分进行可选显示 
后端安全造成：数据库 
user 表(管理员和普通用户同表) 
id,username,password,usertype 
1,admin,123456,1 
2,xiaodi,11111,2 
登录用户 admin 或 xiaodi 时，代码是如何验证这个级别？（usertype 判断） 如果在访问数据包中有传输用户的编号、用户组编号或类型编号的时候，那么尝试对这个值进行修 改，就是测试越权漏洞的基本。  


#修复防御方案
1.前后端同时对用户输入信息进行校验，双重验证机制
2.调用功能前验证用户是否有权限调用相关功能
3.执行关键操作前必须验证用户身份，验证用户是否具备操作数据的权限
4.直接对象引用的加密资源 ID，防止攻击者枚举 ID，敏感数据特殊化处理
5.永远不要相信来自用户的输入，对于可控参数进行严格的检查与过滤
```

  

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629182736947-46092a3c-316a-443e-aee6-9680d0eb7717.png)

### 演示案例

  

- Pikachu-本地水平垂直越权演示（漏洞成因）
- 墨者水平-身份认证失效漏洞实战（漏洞成因）
- 越权检测-小米范越权漏洞检测工具（工具使用）
- 越权检测-Burpsuite 插件 Authz 安装测试（插件使用）

### 涉及资源

[https://github.com/ztosec/secscan-authcheck](https://github.com/ztosec/secscan-authcheck)

[http://pan.baidu.com/s/1pLjaQKF](http://pan.baidu.com/s/1pLjaQKF) (privilegechecker)

[https://www.mozhe.cn/bug/detail/eUM3SktudHdrUVh6eFloU0VERzB4Zz09bW96aGUmozhe](https://www.mozhe.cn/bug/detail/eUM3SktudHdrUVh6eFloU0VERzB4Zz09bW96aGUmozhe)

[https://github.com/alphaSeclab/awesome-burp-suite](https://github.com/alphaSeclab/awesome-burp-suite)

### pikachu

- 水平越权

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629184579763-27b6037e-b344-4b6e-b1b5-6b3a95b6e6d7.png)

将kobe改为Lucy实现水平越权漏洞

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629184569799-34de9aa1-cb7a-436f-b2a4-d2bb1de4c57f.png)

  

- 垂直越权

先用admin/123456账户创建用户并用burp抓包发送到repeter模块当中，在proxy模块中将数据包丢弃。然后换普通用户pikachu/000000登录在浏览器中获取cookie将获取的cookie的替换为repeater中的cookie最后发送

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629188791257-2aff7152-4364-47c5-9eda-0c1f22cd06e3.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629188876377-b8caa0ab-b9ce-4305-9636-f821f2a3a48b.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629188901366-459e94f9-ed69-438b-a80a-0be9a0e79ae2.png)

```
垂直越权:添加用户

前提条件:获取的添加用户的数据包怎么来的数据包:

1.普通用户前端有操作界面可以抓取数据包

2.通过网站源码本地搭建自己去模拟抓取

3.盲猜
```

  

### webug越权

docker搭建webug数据库密码toor

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629277798765-9910e78d-01ef-4738-932c-5c3347a0cd0a.png)

源码分析

```
root@9397cdeda7a6:/# cat `find / -name cross_auth_passwd.php`
<?php


require_once "../../common/common.php";
if (!isset($_SESSION['user'])) {
    header("Location:../login.php");
}

if (isset($_POST['username']) && isset($_POST['password'])) {
    if (!empty($_POST['username']) && !empty($_POST['password'])) {
        $username = $_POST['username'];
        $password = $_POST['password'];
        $sql = "SELECT id, username, password FROM user_test WHERE username = '{$username}' AND password = '{$password}'";
        $res = $dbConnect->query($sql);
        while ($row = mysqli_fetch_assoc($res)) {
            $id = $row['id'];
            header("Location:/pt_env/control/auth_cross/cross_auth_passwd2.php?id={$id}");
        }
    }
}



require_once TPMELATE."/cross_auth_passwd.html";

mysql> use webug;
mysql> select * from user_test;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | admin    | admin    |
|  2 | aaaaa    | asdfsadf |
+----+----------+----------+
2 rows in set (0.00 sec)
```

这里可以看见的是对传入的username和password参数没有修改也就是说这里依然使用SQL注入的风险，但是这里主要是越权也就先不讨论SQL注入的问题。

使用账号`admin`密码`admin`登录出现以下情况。作为小白的我还以为是靶场这样设置的，查了资料后才发现，艹原来这里是个坑

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629194784338-929e8693-2c93-483b-b715-a6f28c8131be.png)

修改代码如下将17行的绝对路径换为相对路径

```
root@9397cdeda7a6:~# tail -8 /var/www/html/control/auth_cross/cross_auth_passwd.php|head -1
            header("Location:./cross_auth_passwd2.php?id={$id}");
root@9397cdeda7a6:~#
```

正常情况是admin用户只能修改admin的密码，aaaaa用户只能修改aaaaa用户的密码,如现在admin用户的密码是admin。我将它修改为123456

```
mysql> select * from user_test;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | admin    | admin    |
|  2 | aaaaa    | 123456   |
+----+----------+----------+
2 rows in set (0.00 sec)

mysql>
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629196309370-5799669e-139c-46c9-a38a-1a853f950dad.png)

可以看到的是我们修改的是成功了，但是呢也发现了一个问题上面传递了参数id=1,而在数据库中刚好有id这一字段也就是说啊，他是通过id来验证用户，那我们试着换下id的参数

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629196469025-31bff83f-b2e9-4b04-961d-5aa135c84495.png)

```
mysql> select * from user_test;
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | admin    | 123456   |
|  2 | aaaaa    | admin    |
+----+----------+----------+
2 rows in set (0.00 sec)
```

在数据库中我们发现id=2的用户密码确实也被修改了，也就是说这里确实存在越权的漏洞。

### burp安装插件

#### Authz

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629276557427-8fcea5f7-6ccc-48ec-bf49-5e05f674098b.png)

安装好之后出现

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629276582403-a1b07741-4bd1-442b-9899-3c39f8847c36.png)

如何使用插件：我们通过代理获取网站登录的数据包，并将数据包发送的`instruder`模块当中(可以制作出大量类似的数据包，当然也可以直接发送到authz插件当中)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629279388416-5c35cb2d-6ab9-49be-9fe0-017ef49229e8.png)![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629279397648-d9eeddbc-5614-4ebd-aa6a-83d809d05c2a.png)

将这些数据包发送到插件当中

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629279445098-c625ab0c-6ca6-4d02-8e45-4e06cceb2cf0.png)

在插件当中运行，设置好cookie选中所有的数据包右击运行

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629279504105-405cb591-d220-4549-a45f-b951db0a36f1.png)

最后获得200和302的状态码，这里也就可以看出哪些是可以正常登陆哪些是错误的。

#### AuthMatrix

  

这个插件是python写的先提前安装python的环境[https://blog.csdn.net/u013175604/article/details/84837360](https://blog.csdn.net/u013175604/article/details/84837360)

环境地址：[https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar](https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629281192735-8b4f52f9-e35e-4712-9e9a-b1ad4e529ce4.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629281228628-0ef7d307-63c0-465f-a288-753054b910e6.png)

这个插件的设置要相对于之前的那个难度要大一些，也不是很难。

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629290590100-b71bf8bf-4f04-4b83-8e68-c3969b7310db.png)

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629290689522-eb626844-2a52-4525-9d50-8e08b18bae7b.png)

将之前的用户提交的cookie信息获取，另外一个用户也是一样

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629290902387-48c4c334-348b-4009-81d6-80f2d7240d1b.png)

将数据包发送至插件当中

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1629291661058-b6848e1b-2710-4327-8fbe-8c5cca4bc99e.png)

然后将在模块当中run就可以了
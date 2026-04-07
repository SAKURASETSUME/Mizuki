---
title: "代理池"
date: 2026-04-07
published: 2026-04-07
author: Rin
permalink: /posts/网安笔记/WAF绕过/代理池/
categories:
  - 网安笔记
  - WAF绕过
  - 代理池
tags:
  - Study
---

## 一、思维导图

WAF拦截会出现在安全测试的各个层面，掌握各个层面的分析和绕过技术最为关键。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326204926-e8d811bb-9c42-47d0-a0a4-8b7befbd8586.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515200623.png)

## 二、演示案例

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326204937-8d9e415b-9deb-47ce-89a2-794a03aa60b6.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515212428.png)

### 1、Safedog-未开CC

CC就是DDOS攻击的一种，默认是不开启的。

判断有没有WAF可以直接在路径上报错显示。

#### ①用目录扫描工具扫

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326204934-7ad0976c-4ae6-4704-ba10-7cb4265fb686.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515213342.png)

扫出来的目录全是假的。

使用抓取进程的抓包工具抓包

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326204979-8b9c6140-fa6c-48eb-a3a6-34b692b2c0e9.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515213616.png)

可以很明显的看出不同，在请求方法上就不同。可以修改为Get方式。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326204945-eeaa993c-a5c5-482d-9625-1cf635286ae8.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515213649.png)

这回就没有误报了。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326205770-55f7987e-2580-43e8-9aac-1fbd252d71ab.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515213723.png)

### 2、Safedog-开启CC

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326205749-7c0e26ae-c7d0-4ff6-a9f8-0b3af5783107.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515213845.png)

开启CC之后，再次使用工具，并且访问网站。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326206038-7e52935d-9ed6-48bd-90db-61ad0ebed26f.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515213935.png)

访问速度过快了。可以设置延迟扫描。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326205866-d3e3d576-5e04-4e2a-b7bf-d65bb86839de.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515214035.png)

或者也可以通过爬虫的白名单来搞

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326205969-354b814f-bf47-4e74-9bba-d077157ba354.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515214404.png)

模拟搜索引擎请求头User-Agent就可以了。进行扫描

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326206683-859cd490-a7b0-4c7b-abfa-0de47eabe169.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515214715.png)

发现没有任何的结果。

#### ①使用python脚本来访问

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326206668-71a85ebe-cce2-427e-9008-7eac91ecacdd.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515215148.png)

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326206773-b5d0d5ad-955c-4423-973b-d758655f2fd7.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515215337.png)

php_b.txt是一个字典

```
import requests
import time

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=4d6f9bc8de5e7456fd24d60d2dfd5e5a',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
}

for paths in open('php_b.txt', encoding='utf-8'):
    url = "http://127.0.0.1/pikachu"
    paths = paths.replace('\n', '')
    urls = url + paths
    proxy = {
        'http': '127.0.0.1:7777'
    }
    try:
        code = requests.get(urls, headers=headers, proxies=proxy).status_code
        # time.sleep(3)
        print(urls + '|' + str(code))
    except Exception as err:
        print('connect error')
        time.sleep(3)
```

![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630328874661-b35b9dbc-b83c-486d-b98c-d62f98df5bc2.png)

抓包分析：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326206723-1ba9300b-4a28-4c1c-9faf-ff1b7b7812df.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515215450.png)

如果不用自定义头：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326206880-ab5da53a-1d02-4b99-8faa-0a0bbc843910.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515215557.png)

可以直接在脚本里使用爬虫引擎的请求头，效果很好。

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326207652-bd2efd59-6274-42d1-a671-b83d781493eb.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515215849.png)

#### ②代理池

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326207810-177b347a-4498-499c-bdc3-37504ed7fdee.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515220116.png)

### 3、阿里云

阿里云-无法模拟搜索引擎爬虫绕过，只能采用代理池或者延时。

### 4、阿里云+宝塔付费安全服务

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326207629-5507a733-1f30-4910-bb13-2d4f0f3711e1.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515221326.png)

通过延时来搞：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326207693-dc95c9f2-bdab-4146-938b-23e9d530c175.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515222025.png)

宝塔里的日志：

[![](https://cdn.nlark.com/yuque/0/2021/png/2476579/1630326207747-1db4d678-5fcc-44aa-be1b-67c3d6edd303.png)](https://gitee.com/darkerg/article-images/raw/master/typora/20210515222053.png)

可以优化日志，因为宝塔检测出一分钟内访问敏感文件了。比如说code.php.bak 可以优化成code.php.bak .访问的还是原来的。
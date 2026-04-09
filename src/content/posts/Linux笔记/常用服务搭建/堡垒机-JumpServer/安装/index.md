---
title: "Linux笔记 - 常用服务搭建 - 堡垒机-JumpServer - 安装"
category: "Linux笔记"
date: 2026-04-09
published: 2026-04-09
author: "Rin"
---

```bash
#提前把内存设置到4G以上 不然跑不起来
#在本机下载 离线上传
cd /opt
tar -zxvf #解压

#进入解压后的目录
cd jumpserver
#执行sh脚本
./jmsctl.sh install
#配置看需求自己配 对外端口要配置 自己配置就行

#启动
./jmsctl.sh start
```

参考：[2023JumpServer入门到精通[精讲版]_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Kx4y1A7CE?vd_source=05d71ca20d1a62ee1c802b01999e7379&spm_id_from=333.788.videopod.episodes)
---
title: "Linux笔记 - 数据库 - Readme"
category: "Linux笔记"
date: 2026-04-15
published: 2026-04-15
author: "Rin"
---

## mysql创建时的一些参数
```bash
docker run -d -p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=root \
-e MYSQL_DATABASE=study \
-v mysql-data:/var/liv/mysql \
-v /app/myconf:/etc/mysql/conf.d \
--restart always --name mysql \
--network sql \
mysql:8.0.26
```

## 使用注意事项
- 由于学习时mysql是在云服务器上用docker安装的 注意保存和推送
- 使用mysql时请注意进入到docker中 不要在Docker Host修改
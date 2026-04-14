---
title: "Linux笔记 - Docker容器化技术 - 基本操作 - 安装Docker"
category: "Linux笔记"
date: 2026-04-14
published: 2026-04-14
author: "Rin"
---

```bash
#这里以CentOS为例
#删除旧版本的Docker
#这里使用了dnf命令 如果没有就自己用yum装一下
sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
                  
#安装工具包 并配置docker下载地址源 建议使用国内源 官网的很慢
sudo yum install -y yum-utils
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

#安装docker
dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

#设置开机自启并启动
systemctl enable docker
systemctl enable --now docker

#测试是否启动成功
docker ps #查看当前运行的容器

#配置docker加速
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-EOF
{
   "registry-mirrors": [
       "https://mirror.ccs.tencentyun.com"
   ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

#重启docker
systemctl daemon-reload
systemctl restart docker
```

手册参考:
[CentOS | Docker Docs](https://docs.docker.com/engine)
---
title: "使用minikube在linux上安装单节点k8s集群"
date: 2018-12-18T20:09:44+08:00
draft: false
categories:
- 技术
---

## 准备好二进制文件
**注意本教程使用的版本如下:**  
* minikube v0.31.0  
* kubeadm v1.13.1  
* kubelet v1.13.1  
* kubectl v1.13.1  

下载minikube, 下载命令:
```
mkdir -p $HOME/.minikube/cache/iso && \
curl -C - -L# -o $HOME/.local/bin/minikube https://github.com/kubernetes/minikube/releases/download/v0.31.0/minikube-linux-amd64
```
或者从[这里](https://github.com/palagend/minikube.git)下载源码编译

借助VPN下载二进制文件: kubeadm, kubelet, kubectl, 下载命令:
```
#VERSION=$(curl https://storage.googleapis.com/kubernetes-release/release/stable.txt)
mkdir -p $HOME/.minikube/cache/v1.13.1 && \
cd $HOME/.minikube/cache/v1.13.1 && \
sudo -E curl -C - -L#O https://storage.googleapis.com/kubernetes-release/release/v1.13.1/bin/linux/amd64/{kubelet,kubeadm,kubectl}
```
下载kubernetes所需的docker镜像, 脚本内容如下:  
cat download-kubernetes.sh
```
#!/bin/bash
#本脚本将拉取以下9个images
#kube-proxy-amd64:v1.13.1
#kube-controller-manager-amd64:v1.13.1
#kube-scheduler-amd64:v1.13.1
#kube-apiserver-amd64:v1.13.1
#pause-amd64:3.1
#coredns:1.2.6
#etcd-amd64:3.2.24
#kubernetes-dashboard-amd64:v1.10.0
#flannel:v0.10.0-amd64

set -e

#运行kubeadm config images list确认指定版本
K8S_VERSION=v1.13.1
ETCD_VERSION=3.2.24
DASHBOARD_VERSION=v1.10.0
FLANNEL_VERSION=v0.10.0-amd64
DNS_VERSION=1.2.6
PAUSE_VERSION=3.1

## 拉取images
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver-amd64:$K8S_VERSION
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-controller-manager-amd64:$K8S_VERSION
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler-amd64:$K8S_VERSION
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy-amd64:$K8S_VERSION
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/etcd-amd64:$ETCD_VERSION
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/pause-amd64:$PAUSE_VERSION
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:$DNS_VERSION
docker pull registry.cn-hangzhou.aliyuncs.com/kubernetes_containers/flannel:$FLANNEL_VERSION
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:$DASHBOARD_VERSION

## 修改tag
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver-amd64:$K8S_VERSION k8s.gcr.io/kube-apiserver:$K8S_VERSION
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-controller-manager-amd64:$K8S_VERSION k8s.gcr.io/kube-controller-manager:$K8S_VERSION
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler-amd64:$K8S_VERSION k8s.gcr.io/kube-scheduler:$K8S_VERSION
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy-amd64:$K8S_VERSION k8s.gcr.io/kube-proxy:$K8S_VERSION
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/etcd-amd64:$ETCD_VERSION k8s.gcr.io/etcd:$ETCD_VERSION
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/pause-amd64:$PAUSE_VERSION k8s.gcr.io/pause:$PAUSE_VERSION
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:$DNS_VERSION k8s.gcr.io/coredns:$DNS_VERSION
docker tag registry.cn-hangzhou.aliyuncs.com/kubernetes_containers/flannel:$FLANNEL_VERSION quay.io/coreos/flannel:$FLANNEL_VERSION
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:$DASHBOARD_VERSION k8s.gcr.io/kubernetes-dashboard:$DASHBOARD_VERSION

## 删除原镜像
docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver-amd64:$K8S_VERSION
docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/kube-controller-manager-amd64:$K8S_VERSION
docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler-amd64:$K8S_VERSION
docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy-amd64:$K8S_VERSION
docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/etcd-amd64:$ETCD_VERSION
docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/pause-amd64:$PAUSE_VERSION
docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:$DNS_VERSION
docker rmi registry.cn-hangzhou.aliyuncs.com/kubernetes_containers/flannel:$FLANNEL_VERSION
docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:$DASHBOARD_VERSION
```
新建minikube的配置文件`$HOME/.minikube/config/config.json`, 内容如下:
```
{
    "WantReportErrorPrompt": false,
    "WantUpdateNotification": false,
    "ChangeMinikubeNoneUser": true,
    "kubernetes-version": "v1.13.1",
    "vm-driver": "none",
    "iso-url": "https://storage.googleapis.com/minikube/iso/minikube-v0.31.0.iso"
}
```

启动minikube, 命令如下:
```
sudo -E minikube start --vm-driver none --v 0 --alsologtostderr --kubernetes-version v1.13.1
```
## 简便起见, 这里提供了一个安装minikube的脚本, 脚本内容如下:  
cat install-minikube.sh
```
#!/bin/bash
#export http_proxy=http://172.19.210.34:7777
#export https_proxy=$http_proxy
export MINIKUBE_WANTUPDATENOTIFICATION=false
export MINIKUBE_WANTREPORTERRORPROMPT=false
export MINIKUBE_HOME=$HOME
export CHANGE_MINIKUBE_NONE_USER=true
mkdir -p $HOME/.kube
touch $HOME/.kube/config

export KUBECONFIG=$HOME/.kube/config

mkdir -p ~/.minikube/config && \
echo '{
    "level": "0",
    "kubernetes-version": "v1.13.1",
    "vm-driver": "none",
    "iso-url": "https://storage.googleapis.com/minikube/iso/minikube-v0.31.0.iso"
}' > ~/.minikube/config/config.json

sudo -E minikube start

# this for loop waits until kubectl can access the api server that Minikube has created
for i in {1..150}; do # timeout for 5 minutes
	kubectl get po &> /dev/null
	if [ $? -ne 1 ]; then
		break
	fi
	sleep 2
done

# kubectl commands are now able to interact with Minikube cluster
```
## 其他
如果安装失败,请清理旧文件,命令如下:
```
sudo rm -rf /etc/kubernetes /var/lib/minikube ~/.minikube
```

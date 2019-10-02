---
title: Docker技术简介
date: 2018-12-18T20:09:44+08:00
draft: false
categories:
- general
---

Docker技术贯穿CI/CD的整个过程，既是基础的技术，又是重要的技术。这里只是想普及一下Docker的技术，
为后续的CI/CD奠定基础，所以尽量从简单通俗的方式介绍Docker技术

---

## 什么是部署
部署就是将开发的应用程序代码和相关文件放置到服务器的指定位置，使得客户端能够通过网络来使用应用程
序提供的服务。

---

## 传统部署

开发人员在本地设置好的环境下开发并调试程序，成功之后提交编译好的程序给
运维人员；然后运维人员在生产服务器上设置好与本地开发环境一致的环境，并把程序上传到服务器启动程序
，调式无误后，部署工作就算完成了。

---

## 容器部署

---

开发人员在本地开发并调试完成后，并不只是把编译好的程序提交给运维人
员，而是先将程序代码和相关文件以及程序所以依赖的环境配置一同打包到一个镜像中（Docker镜像），然后
把这个镜像提交到Docker仓库；运维人员只需要在生产服务器上拉取这个镜像到生产服务器，然后基于这个镜
像拉起一个容器，程序在容器里运行，这个容器里已经包含了程序在本地开发时一致的运行环境。

---

## 容器化部署 vs 传统部署
容器部署和传统部署最显著的不同就是对程序运行时环境（runtime environment）的处理上，前者将运行
时环境与程序本身打包在一起，随程序一起发布、部署。后者是将程序发布，但是程序的环境需要在程序所部
署的地方另外设置。
这种区别可以用”国王的皮鞋“来比喻。

---

## Docker技术的经济效益
这里的**牛皮**就是**运行环境**, **脚**是**应用程序**, **崎岖不平的路面**是各种各样的生产服务器。
**传统部署**就是给所有的服务器蒙上一层“牛皮”,然后让“脚”在上面走(运行)；**容器部署**则是用“牛
皮”包住程序，在服务器上运行，而不需要对服务器做很多的适配工作。

---

传统部署方式，对开发人员来说可能比较省事，程序开发调试完毕就可以扔给运维人员了（光着脚走在牛皮大
道上当然是极好的）；容器部署对于运维人员和管理人员来说是比较省心的，只需要拿到开发人员提交过来的
容器镜像在服务器上运行起来就行了，如果容器出了问题只需要更换为新的容器就可以了。这个代价是要求开发
人员多承担了一道制作皮鞋（容器）的工序。

**但是很明显从整体经济效益和管理成本上来讲，容器部署比传统部署更有优势。**

---

## Docker
上面谈了部署的概念，一直在说**容器**,这里就来看看容器的庐山真面目Docker。其实Docker并不是什么
新技术，而是对原有成熟技术的包装整合形成的生态系统，这个生态系统对开发部署模式产生了深远影响。

---
## Docker技术中的一些概念

* LXC
* Dockerfile
* OCI RunC Containerd
* <del>Kubernetes</del>

---

### LXC
![LXC](http://s3.51cto.com/wyfs02/M01/59/D0/wKioL1TpsMngc0eRAABiI1fwTec847.jpg)  
Docker基于LXC技术，对操作系统做了一层虚拟化。
每一个容器就像一个“世外桃源”，彼此之间相互隔离（隔离性）。这些“世外桃源”虽然彼此隔
离，但是都生活在“地球”（共的操作系统内核）上，所以它们并不能无节制地使用资源（资源限制）。
Docker对容器的隔离和资源限制并不是自己实现的而是依赖于LXC提供的namespace和cgroup模块来实现的（拿来主义）。

---

### Dockerfile
![Dockerfile](http://s3.51cto.com/wyfs02/M02/59/D4/wKiom1Tpsujj_MwQAAESaE06H8Q505.jpg "Dockerfile")

---

### OCI & RunC
> Open Container Initiative，也就是常说的OCI，是由多家公司共同成立的项目，并由linux基金会进行管理，致力于container runtime的标准的制定和runc的开发等工作

**container有很多种，而docker是其中的一种container。**

OCI -> RunC : Interface -> Implementation

---

下图能够解释RunC和Docker的关系：
![containerd](http://xuxinkun.github.io/img/docker-oci-runc-k8s/containerd.png)

---

k8s为了与docker解耦合引入CRI项目：
![k8s](http://xuxinkun.github.io/img/docker-oci-runc-k8s/kubelet.png)

---

## 容器化部署的意识
开发时要有容器部署意识(code,data,conf,lib,doc,log)

应用(app) = 代码(code) + 环境(context)

---

## 参考链接
要想更全面深入地了解Docker技术可以参考下面这些链接：  
[Docker官方文档](https://docs.docker.com/)  
[LXC官方网站](https://linuxcontainers.org/)  
[Kubernetes](https://kubernetes.io/)  
[RunC](https://github.com/opencontainers/runc)  
[RKT](https://coreos.com/rkt/)  
[Docker中文社区](http://www.docker.org.cn/)  
[Kubernetes中文社区](https://www.kubernetes.org.cn/)

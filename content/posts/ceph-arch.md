---
title: "Ceph Arch"
date: 2019-06-28T11:24:03+08:00
draft: false
categories:
 - '技术'
tags:
 - 
featured_image:
---
Ceph生态系统架构可以划分为四部分：

*client*：客户端（数据用户）。client向外export出一个POSIX文件系统接口，供应用程序调用，并连接mon/mds/osd，进行元数据及数据交互；最原始的client使用FUSE来实现的，现在写到内核里面了，需要编译一个ceph.ko内核模块才能使用。

*mon*：集群监视器，其对应的daemon程序为cmon（Ceph Monitor）。mon监视和管理整个集群，对客户端export出一个网络文件系统，客户端可以通过mount -t ceph monitor_ip:/ mount_point命令来挂载Ceph文件系统。根据官方的说法，3个mon可以保证集群的可靠性。

*mds*：元数据服务器，其对应的daemon程序为cmds（Ceph Metadata Server）。Ceph里可以有多个MDS组成分布式元数据服务器集群，就会涉及到Ceph中动态目录分割来进行负载均衡。

*osd*：对象存储集群，其对应的daemon程序为cosd（Ceph Object StorageDevice）。osd将本地文件系统封装一层，对外提供对象存储的接口，将数据和元数据作为对象存储。这里本地的文件系统可以是ext2/3，但Ceph认为这些文件系统并不能适应osd特殊的访问模式，它们之前自己实现了ebofs，而现在Ceph转用btrfs。

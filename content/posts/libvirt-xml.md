---
title: "Libvirt Xml"
date: 2019-06-29T18:10:08+08:00
draft: false
categories:
 - '技术'
tags:
 - 
featured_image:
---

```
#虚拟化类型为kvm(type='kvm')，可选的还有qemu
<domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
#虚拟机名字 openstack1-1
 <name>openstack1-1</name>
#虚拟机预分配内存8388608K,这个是宿主机允许虚拟机使用的最大内存，并不是在虚拟机里用free看到的内存
  <memory unit='KiB'>8388608</memory>
#虚拟机当前定义内存(8388608)，free看到的内存，可以使用virsh setmem调整内存
  <currentMemory unit='KiB'>8388608</currentMemory>
#虚拟机cpu个数
<vcpu placement='static'>4</vcpu>
  <os>
#模拟的系统架构x86_64,模拟机器类型rhel6.5
    <type arch='x86_64' machine='rhel6.5.0'>hvm</type>
#虚拟机开机引导项，hd：硬盘，cdrom：光盘，即先硬盘，后光盘
    <boot dev='hd'/>
    <boot dev='cdrom'/>
    <bootmenu enable='yes'/>
    <bios useserial='yes' rebootTimeout='0'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
#虚拟机cpu模拟类型，host-model，使用宿主机cpu的所有可使用特性
  <cpu mode='host-model'>
    <model fallback='allow'/>
  </cpu>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
#运行虚拟机的程序，qemu-kvm，可以在宿主机使用ps -ef | grep qemu-kvm 看到
    <emulator>/usr/libexec/qemu-kvm</emulator>
#定义虚拟机磁盘
    <disk type='file' device='disk'>
#虚拟机磁盘为qcow2格式，如果你创建或使用的磁盘是raw格式，需要修改为raw
      <driver name='qemu' type='qcow2' cache='none'/>
#磁盘路径
      <source file='/data/vhosts/jython/openstack/openstack1-1.disk'/>
#第一块为vda，第二块就为vdb，不能重复，重复虚拟机启动报错
      <target dev='vda' bus='virtio'/>
    </disk>
    <controller type='ide' index='0'>
    </controller>
    <controller type='virtio-serial' index='0'>
    </controller>
    <controller type='usb' index='0'>
    </controller>
#虚拟机网络为桥接模式bridge，桥接网桥为br-ex，要确保网桥br-ex存在，并且能使用
    <interface type='bridge'>
      <source bridge='br-ex'/>
      <model type='virtio'/>
    </interface>
#第二张网卡，如果需要多块网卡，就复制多次
    <interface type='bridge'>
      <source bridge='br-ex'/>
      <model type='virtio'/>
    </interface>
    <console type='pty'>
    </console>
    <input type='mouse' bus='ps2'/>
#使用vnc协议，autoport='yes':自动分配端口，从5900开始
    <graphics type='vnc' autoport='yes' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
    <video>
      <model type='cirrus' heads='1'/>
    </video>
#气球内存技术，kvm特性之一
    <memballoon model='virtio'>
    </memballoon>
  </devices>
#下面三行是为了实现多vnc客户端连接，即多个用户使用vnc客户端连接到同一台虚拟机，操作实时同步
  <qemu:commandline>
    <qemu:env name='SPICE_DEBUG_ALLOW_MC' value='1'/>
  </qemu:commandline>
</domain>
```

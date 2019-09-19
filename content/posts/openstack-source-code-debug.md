---
title: "Openstack Source Code Debug"
date: 2019-09-19T17:37:08+08:00
draft: false
categories:
 - '技术'
tags:
 - 
featured_image: 2019/09/19/nLaBOs.md.jpg
---

由于openstack版本迭代的太快，很多上一个版本还能用的东西，下个版本又不能用了，我开始接触的时候是M版，等我上手之后，P版已经成熟，Q版也可以使用了。因为我需要对keystone的架构重写，所以我首先要解决的问题就是调试源代码，虽然通过各种书籍理论知道了keystone的架构模型，但实际自己去动源代码，也是很难的。

一开始我参考网上给的调试方法，结果发现，由于版本的更迭，很多东西已经不一样了，比如以前keystone自己通过脚本启动，但现在已经是依靠apache2启动了，所以，开篇之前，说明，我的所以代码都来自P版本，而且因为自己摸索时，经常遇到网上大牛给的方法不够详细，导致我无法进行，所以，我会非常详细的说明每个步骤，每个步骤我都会在P版本测试，如有疑问，欢迎交流。这里大家可以先只装keystone模块，后续需要其它模块的时候再继续装，安装就参照[官网方法](https://docs.openstack.org/keystone/pike/install/)。我这里采用ubuntu版本的。

第一篇，我们需要对openstack采用的架构作一个简单的说明，要读懂调试源代码，首先我们要知道openstack的基本架构，而openstack每个模块都差不多，所以当我们理解一个之后，后面都可以很轻松的实现。

首先，openstack采用WSGI框架，这个大家可参考[这篇文章](https://segmentfault.com/a/1190000003069785)，我觉得是我看过最清晰明了的。然后，还需要了解python paste，可以参考[这篇文章](https://blog.csdn.net/li_101357/article/details/52755367)。开始之前，请确保自己基本了解了这两个东西，这是继续下去的前提。其中paste后面还会涉及一些东西，到时候我会说，这里就先了解一下。

好了，当你清楚WSGI框架之后，我们来说说apache和keystone的关系，现在版本的keystone已经不需要自己启动了，都是service apache2 start即可，apache其实就是帮助keystone实现了套接字，也就是帮助keystone监听相应端口，这里对应的配置文件是/etc/apache2/sites-available/keystone.conf，同时必须在/etc/apache2/sites-enabled/中建立同名的链接才能生效。

才看keystone.conf配置文件：

```
Listen 5000
Listen 35357

<VirtualHost *:5000>
    WSGIScriptAlias / /usr/bin/keystone-wsgi-public
    WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-public
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    LimitRequestBody 114688

    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>

    ErrorLog /var/log/apache2/keystone.log
    CustomLog /var/log/apache2/keystone_access.log combined

    <Directory /usr/bin>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
    </Directory>
</VirtualHost>

<VirtualHost *:35357>
    WSGIScriptAlias / /usr/bin/keystone-wsgi-admin
    WSGIDaemonProcess keystone-admin processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-admin
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    LimitRequestBody 114688

    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>

    ErrorLog /var/log/apache2/keystone.log
    CustomLog /var/log/apache2/keystone_access.log combined

    <Directory /usr/bin>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
    </Directory>
</VirtualHost>

Alias /identity /usr/bin/keystone-wsgi-public
<Location /identity>
    SetHandler wsgi-script
    Options +ExecCGI

    WSGIProcessGroup keystone-public
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
</Location>

Alias /identity_admin /usr/bin/keystone-wsgi-admin
<Location /identity_admin>
    SetHandler wsgi-script
    Options +ExecCGI

    WSGIProcessGroup keystone-admin
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
</Location>
```

这里我们可以看到，apache帮助keystone监听5000和35357端口，一个用于admin访问，一个用于普通用户访问。在这里配置文件中，最重要的是WSGIScriptAlias和Alias后面的第二个路径，它会在apache启动的时候创建各种后续会用到的route处理方法。

这里以/usr/bin/keystone-wsgi-public文件为例讲解，查看该文件

```
#!/usr/bin/python
#PBR Generated from u'wsgi_scripts'

import threading

from keystone.server.wsgi import initialize_public_application

if __name__ == "__main__":
    import argparse
    import socket
    import sys
    import wsgiref.simple_server as wss

    my_ip = socket.gethostbyname(socket.gethostname())

    parser = argparse.ArgumentParser(
        description=initialize_public_application.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage='%(prog)s [-h] [--port PORT] [--host IP] -- [passed options]')
    parser.add_argument('--port', '-p', type=int, default=8000,
                        help='TCP port to listen on')
    parser.add_argument('--host', '-b', default='',
                        help='IP to bind the server to')
    parser.add_argument('args',
                        nargs=argparse.REMAINDER,
                        metavar='-- [passed options]',
                        help="'--' is the separator of the arguments used "
                        "to start the WSGI server and the arguments passed "
                        "to the WSGI application.")
    args = parser.parse_args()
    if args.args:
        if args.args[0] == '--':
            args.args.pop(0)
        else:
            parser.error("unrecognized arguments: %s" % ' '.join(args.args))
    sys.argv[1:] = args.args
    server = wss.make_server(args.host, args.port, initialize_public_application())

    print("*" * 80)
    print("STARTING test server keystone.server.wsgi.initialize_public_application")
    url = "http://%s:%d/" % (server.server_name, server.server_port)
    print("Available at %s" % url)
    print("DANGER! For testing only, do not use in production")
    print("*" * 80)
    sys.stdout.flush()

    server.serve_forever()
else:
    application = None
    app_lock = threading.Lock()

    with app_lock:
        if application is None:
            application = initialize_public_application()
```

这里可以看到，如果本文件直接运行，会执行上面，否则执行else，这里的if其实留给我们测试的，它的作用是不依赖apache，帮我们创建好socket，并监听端口，默认8000，而apache启动时，其实会跳过socket的创建，因为apache帮我们做了，所以直接初始化application，关于application，请回忆上面的WSGI。那么，既然知道了这个，我们就可以使用这个脚本，直接调试了。

比如，我直接运行这个脚本，

![img1](http://s2.ax1x.com/2019/09/19/nLBD3T.png)
 

发现keystone就在8000端口启动了，那么我们尝试访问一下keystone服务，比如申请一个token，重开一个终端，设置用于访问的参数

```
export OS_PROJECT_DOMAIN_NAME=Default

export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=123456
export OS_AUTH_URL=http://controller:8000/v3
export OS_IDENTITY_API_VERSION=3

export OS_IMAGE_API_VERSION=2
```

大家应该记得，我们直接安装时，如果要访问，就是设置的这些参数，只是这里端口改为了8000，其余是一样，效果如下：

![img2](http://s2.ax1x.com/2019/09/19/nLB58K.png)


同时查看开启服务的终端

![img3](http://s2.ax1x.com/2019/09/19/nLDmxU.png)

发现接收到了请求，说明如我们猜测一样。那么我们再试试在这个脚本里打上断点，我采用pdb调试，不会的可以参考这篇文章，也可以成功进入。（最开始写的时候用的pdb调试，后来发现不好用个，配置了远程调试，这是后面补的https://blog.csdn.net/u012198947/article/details/88988321，参考这个使用pycharm远程调试，方便好用）

以一张图来说明：

![img4](http://s2.ax1x.com/2019/09/19/nLDGPx.png)

 

可以看出initialize_application就是关键代码（在keystone-wsgi-admin中，叫initialize_admin_application，keystone-wsgi-public中叫initialize_public_application，后面会看到，其实都是执行initialize_application），下篇我们就进入initialize_application

————————————————
版权声明：本文为CSDN博主「dyplm123」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u012198947/article/details/79695870

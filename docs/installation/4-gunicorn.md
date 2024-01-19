# Gunicorn

与大多数Django应用程序一样，NetBox在HTTP服务器后面作为[WSGI应用程序](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)运行。此文档介绍如何安装和配置[gunicorn](http://gunicorn.org/)（它会自动与NetBox一起安装）来执行此任务，不过还有其他WSGI服务器可用，应该同样有效。[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/)是一个常见的替代方案。

## 配置

NetBox附带了一个用于gunicorn的默认配置文件。要使用它，请将`/opt/netbox/contrib/gunicorn.py`复制到`/opt/netbox/gunicorn.py`。（我们复制此文件而不是直接指向它，以确保将来的升级不会覆盖对其的任何本地更改。）

```no-highlight
sudo cp /opt/netbox/contrib/gunicorn.py /opt/netbox/gunicorn.py
```

虽然提供的配置对于大多数初始安装应该足够了，但您可能希望编辑此文件以更改绑定的IP地址和/或端口号，或进行性能相关的调整。请参阅[Gunicorn文档](https://docs.gunicorn.org/en/stable/configure.html)以获取可用的配置参数。

## systemd设置

我们将使用systemd来控制gunicorn和NetBox的后台工作进程。首先，将`contrib/netbox.service`和`contrib/netbox-rq.service`复制到`/etc/systemd/system/`目录并重新加载systemd守护程序。

!!! 警告 "检查用户和组的分配"
    NetBox打包的标准服务配置文件假定服务将使用`netbox`用户和组名称运行。如果这些在您的安装中不同，请确保相应地更新服务文件。

```no-highlight
sudo cp -v /opt/netbox/contrib/*.service /etc/systemd/system/
sudo systemctl daemon-reload
```

然后，启动`netbox`和`netbox-rq`服务并将它们设置为在启动时启动：

```no-highlight
sudo systemctl start netbox netbox-rq
sudo systemctl enable netbox netbox-rq
```

您可以使用命令`systemctl status netbox`来验证WSGI服务是否正在运行：

```no-highlight
systemctl status netbox.service
```

您应该会看到类似以下的输出：

```no-highlight
● netbox.service - NetBox WSGI Service
     Loaded: loaded (/etc/systemd/system/netbox.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-08-30 04:02:36 UTC; 14h ago
       Docs: https://docs.netbox.dev/
   Main PID: 1140492 (gunicorn)
      Tasks: 19 (limit: 4683)
     Memory: 666.2M
     CGroup: /system.slice/netbox.service
             ├─1140492 /opt/netbox/venv/bin/python3 /opt/netbox/venv/bin/gunicorn --pid /va>
             ├─1140513 /opt/netbox/venv/bin/python3 /opt/netbox/venv/bin/gunicorn --pid /va>
             ├─1140514 /opt/netbox/venv/bin/python3 /opt/netbox/venv/bin/gunicorn --pid /va>
...
```

!!! 注意
    如果NetBox服务启动失败，请使用命令`journalctl -eu netbox`检查可能指示问题的日志消息。

一旦验证了WSGI工作者正在运行，就可以继续进行HTTP服务器设置。
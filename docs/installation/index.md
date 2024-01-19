# 安装

!!! info "NetBox Cloud"
    以下说明适用于将NetBox安装为独立的、自托管的应用程序。如果需要云交付解决方案，请查看NetBox Labs的[NetBox Cloud](https://netboxlabs.com/netbox-cloud/)。

这里提供的安装说明已经在Ubuntu 22.04和CentOS 8.3上进行了测试。在其他发行版上安装依赖所需的特定命令可能会有很大的差异。不幸的是，这不在NetBox维护者的控制范围内。请查阅您的发行版文档以获取有关解决任何错误的帮助。

<iframe width="560" height="315" src="//player.bilibili.com/player.html?aid=581442080&bvid=BV1p64y1A78u&cid=1411844506&p=1" title="Bilibili视频播放器" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

以下部分详细介绍了如何设置一个新的NetBox实例：

1. [PostgreSQL数据库](1-postgresql.md)
2. [Redis](2-redis.md)
3. [NetBox组件](3-netbox.md)
4. [Gunicorn](4-gunicorn.md)
5. [HTTP服务器](5-http-server.md)
6. [LDAP认证](6-ldap.md)（可选）

## 要求

| 依赖项     | 最低版本 |
|------------|-----------|
| Python     | 3.8       |
| PostgreSQL | 12        |
| Redis      | 4.0       |

以下是NetBox应用程序栈的简化概述，供参考：

![非经过身份验证用户看到的NetBox UI](../media/installation/netbox_application_stack.png)

## 升级

如果您要从现有的安装中升级，请参阅[升级指南](upgrading.md)。
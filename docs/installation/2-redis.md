# Redis安装

[Redis](https://redis.io/)是一个内存中的键值存储，NetBox用它来进行缓存和队列操作。本节介绍如何安装和配置本地的Redis实例。如果您已经有一个Redis服务，请跳转到[下一节](3-netbox.md)。

=== "Ubuntu"

    ```no-highlight
    sudo apt install -y redis-server
    ```

=== "CentOS"

    ```no-highlight
    sudo yum install -y redis
    sudo systemctl start redis
    sudo systemctl enable redis
    ```

在继续之前，请验证您安装的Redis版本至少为v4.0：

```no-highlight
redis-server -v
```

您可以在`/etc/redis.conf`或`/etc/redis/redis.conf`中修改Redis配置，但在大多数情况下，默认配置已经足够了。

## 验证服务状态

使用`redis-cli`工具来确保Redis服务正常运行：

```no-highlight
redis-cli ping
```

如果成功，您应该会收到来自服务器的`PONG`响应。
# PostgreSQL数据库安装

本节介绍如何安装和配置本地的PostgreSQL数据库。如果您已经有一个PostgreSQL数据库服务，请跳转到[下一节](2-redis.md)。

!!! warning "需要PostgreSQL 12或更高版本"
    NetBox需要PostgreSQL 12或更高版本。请注意，不支持MySQL和其他关系数据库。

## 安装

=== "Ubuntu"

    ```no-highlight
    sudo apt update
    sudo apt install -y postgresql
    ```

=== "CentOS"

    ```no-highlight
    sudo yum install -y postgresql-server
    sudo postgresql-setup --initdb
    ```

    CentOS默认为PostgreSQL配置了基于ident的主机认证。由于NetBox将需要使用用户名和密码进行身份验证，请修改`/var/lib/pgsql/data/pg_hba.conf`文件，将以下行的`ident`更改为`md5`以支持MD5身份验证：

    ```no-highlight
    host    all             all             127.0.0.1/32            md5
    host    all             all             ::1/128                 md5
    ```

    安装完PostgreSQL后，启动服务并启用它在启动时运行：

    ```no-highlight
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    ```

在继续之前，请验证您已安装了PostgreSQL 12或更高版本：

```no-highlight
psql -V
```

## 创建数据库

至少，我们需要为NetBox创建一个数据库，并为其分配一个用于身份验证的用户名和密码。首先，以系统Postgres用户身份调用PostgreSQL shell。

```no-highlight
sudo -u postgres psql
```

在shell中，输入以下命令来创建数据库和用户（角色），替换您自己的密码值：

```postgresql
CREATE DATABASE netbox;
CREATE USER netbox WITH PASSWORD 'J5brHrAXFLQSif0K';
ALTER DATABASE netbox OWNER TO netbox;
-- 下面两个命令在PostgreSQL 15及更高版本上需要
\connect netbox;
GRANT CREATE ON SCHEMA public TO netbox;
```

!!! danger "使用强密码"
    **不要使用示例中的密码。**选择一个强密码以确保NetBox安装的数据库身份验证安全。

完成后，输入`\q`退出PostgreSQL shell。

## 验证服务状态

您可以通过执行`psql`命令并传递配置的用户名和密码来验证身份验证是否有效。（如果使用远程数据库，请将`localhost`替换为您的数据库服务器。）

```no-highlight
$ psql --username netbox --password --host localhost netbox
Password for user netbox: 
psql (12.5 (Ubuntu 12.5-0ubuntu0.20.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

netbox=> \conninfo
You are connected to database "netbox" as user "netbox" on host "localhost" (address "127.0.0.1") at port "5432".
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
netbox=> \q
```

如果成功，您将进入`netbox`提示符。键入`\conninfo`以确认您的连接，或键入`\q`以退出。
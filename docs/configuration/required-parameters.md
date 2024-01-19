# 必需的配置设置

## ALLOWED_HOSTS

这是一个有效的完全合格域名（FQDN）和/或IP地址列表，可用于访问NetBox服务。通常，这与NetBox服务器的主机名相同，但也可以不同；例如，当使用反向代理在不同于NetBox服务器主机名的FQDN下提供NetBox网站时。为了防止[HTTP主机标头攻击](https://docs.djangoproject.com/en/3.0/topics/security/#host-headers-virtual-hosting)，NetBox不允许通过任何其他主机名（或IP）访问服务器。

!!! note
    此参数必须始终定义为列表或元组，即使只提供单个值。

此选项的值还用于设置`CSRF_TRUSTED_ORIGINS`，该选项将POST请求限制为同一组主机（有关更多信息，请参见[此处](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-CSRF_TRUSTED_ORIGINS)）。请注意，默认情况下，NetBox将`USE_X_FORWARDED_HOST`设置为true，这意味着如果您使用反向代理，需要在此列表中添加用于访问该反向代理的FQDN（有关更多信息，请参见[此处](https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts)）。

示例：

```
ALLOWED_HOSTS = ['netbox.example.com', '192.0.2.123']
```

如果您还不确定NetBox安装的域名和/或IP地址是什么，并且愿意接受这样做的风险，您可以将其设置为通配符（星号）以允许所有主机值：

```
ALLOWED_HOSTS = ['*']
```

---

## DATABASE

NetBox需要访问一个PostgreSQL 12或更高版本的数据库服务来存储数据。该服务可以在NetBox服务器上本地运行，也可以在远程系统上运行。在`DATABASE`字典中必须定义以下参数：

* `NAME` - 数据库名称
* `USER` - PostgreSQL用户名
* `PASSWORD` - PostgreSQL密码
* `HOST` - 数据库服务器的名称或IP地址（如果在本地运行，则使用`localhost`）
* `PORT` - PostgreSQL服务的TCP端口；保留默认端口时留空（TCP/5432）
* `CONN_MAX_AGE` - [持久数据库连接](https://docs.djangoproject.com/en/stable/ref/databases/#persistent-connections)的生命周期，以秒为单位（默认为300）
* `ENGINE` - 要使用的数据库后端；必须是与PostgreSQL兼容的后端（例如`django.db.backends.postgresql`）

示例：

```python
DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'netbox',               # 数据库名称
    'USER': 'netbox',               # PostgreSQL用户名
    'PASSWORD': 'J5brHrAXFLQSif0K', # PostgreSQL密码
    'HOST': 'localhost',            # 数据库服务器
    'PORT': '',                     # 数据库端口（保留默认值）
    'CONN_MAX_AGE': 300,            # 最大数据库连接时长
}
```

!!! note
    NetBox支持由底层Django框架支持的所有PostgreSQL数据库选项。有关可用参数的完整列表，请参阅[Django文档](https://docs.djangoproject.com/en/stable/ref/settings/#databases)。

!!! warning
    请确保在ENGINE设置中使用与PostgreSQL兼容的后端。如果不指定ENGINE，默认值将为django.db.backends.postgresql。

---

## REDIS

[Redis](https://redis.io/)是类似于memcached的轻量级内存数据存储。NetBox使用Redis进行后台任务排队和其他功能。

Redis的配置与`DATABASE`类似，对于`tasks`和`caching`两个子部分的设置是相同的：

* `HOST` - Redis服务器的名称或IP地址（如果在本地运行，则使用`localhost`）
* `PORT` - Redis服务的TCP端口；保留默认端口时留空（6379）
* `USERNAME` - Redis用户名（如果设置）
* `PASSWORD` - Redis密码（如果设置）
* `DATABASE` - 数字数据库ID
* `SSL` - 使用SSL连接到Redis
* `INSECURE_SKIP_TLS_VERIFY` - 将其设置为`True`以**禁用**TLS证书验证（不推荐使用）

以下是示例配置：

```python
REDIS = {
    'tasks': {
        'HOST': 'redis.example.com',
        'PORT': 1234,
        'USERNAME': 'netbox',
        'PASSWORD': 'foobar',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': 'localhost',
        'PORT': 6379,
        'USERNAME': '',
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    }
}
```

!!! note
    如果您正在升级NetBox版本，而版本低于v2.7.0，请注意Redis连接配置设置已更改。需要手动修改以使`REDIS`部分与上述规范保持一致。

!!! warning
    强烈建议将任务和缓存数据库保持分开。在相同的Redis实例上使用相同的数据库号码来进行排队的后台任务可能会在缓存刷新事件期间丢失。

### 使用Redis Sentinel

如果您使用[Redis Sentinel](https://redis.io/topics/sentinel)以实现高可用性，需要进行最少的配置以使NetBox能够识别它。需要从上述中删除`HOST`和`PORT`键，并添加三个新键。

* `SENTINELS`：元组列表或元组，每个内部元组包含要连接到的每个Sentinel实例的Redis服务器的名称或IP地址和端口
* `SENTINEL_SERVICE`：要连接到的主/服务的名称
* `SENTINEL_TIMEOUT`：连接超时，以秒为单位

示例：

```python
REDIS = {
    'tasks': {
        'SENTINELS': [('mysentinel.redis.example.com', 6379)],
        'SENTINEL_SERVICE': 'netbox',
        'SENTINEL_TIMEOUT': 10,
        'PASSWORD': '',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'SENTINELS': [
            ('mysentinel.redis.example.com', 6379),
            ('othersentinel.redis.example.com', 6379)
        ],
        'SENTINEL_SERVICE': 'netbox',
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    }
}
```

!!! note
    可以使用Sentinel只为一个数据库，而不是另一个数据库。

---

## SECRET_KEY

`SECRET_KEY`是一个秘密的伪随机字符串，用于辅助创建用于密码和HTTP Cookie的新加密哈希。在配置文件之外不应共享此处定义的密钥。`SECRET_KEY`可以随时更改而不影响存储的数据，但请注意这样做会使所有现有用户会话无效。由多个节点组成的NetBox部署必须在所有节点上配置相同的秘密密钥。

`SECRET_KEY` **必须**至少为50个字符，并且应包含字母、数字和符号的混合。位于`$INSTALL_ROOT/netbox/generate_secret_key.py`的脚本可以用于生成适当的密钥。请注意，此密钥**不**直接用于对用户密码进行哈希处理或用于NetBox中秘密数据的加密存储。

# LDAP配置

本指南解释了如何使用外部服务器实现LDAP身份验证。如果验证失败，用户身份验证将回退到内置的Django用户。

## 安装要求

### 安装系统包

在Ubuntu上：

```no-highlight
sudo apt install -y libldap2-dev libsasl2-dev libssl-dev
```

在CentOS上：

```no-highlight
sudo yum install -y openldap-devel python3-devel
```

### 安装django-auth-ldap

激活Python虚拟环境并使用pip安装`django-auth-ldap`包：

```no-highlight
source /opt/netbox/venv/bin/activate
pip3 install django-auth-ldap
```

安装后，将该软件包添加到`local_requirements.txt`中，以确保在将来重建虚拟环境时重新安装它：

```no-highlight
sudo sh -c "echo 'django-auth-ldap' >> /opt/netbox/local_requirements.txt"
```

## 配置

首先，在`configuration.py`中启用LDAP身份验证后端（如果已设置为`RemoteUserBackend`，请确保覆盖此定义）：

```python
REMOTE_AUTH_BACKEND = 'netbox.authentication.LDAPBackend'
```

接下来，在与`configuration.py`相同的目录中创建一个文件（通常是`/opt/netbox/netbox/netbox/`）命名为`ldap_config.py`。在`ldap_config.py`中定义下面所需的所有参数。所有`django-auth-ldap`配置选项的完整文档都包含在该项目的[官方文档](https://django-auth-ldap.readthedocs.io/)中。

### 通用服务器配置

!!! info
    当使用Active Directory时，您可能需要在`AUTH_LDAP_SERVER_URI`上指定端口，以便对所有域中的用户进行身份验证。对于安全访问，使用`3269`，对于非安全访问全局目录（Global Catalog）使用`3268`。

```python
import ldap

# 服务器URI
AUTH_LDAP_SERVER_URI = "ldaps://ad.example.com"

# 如果绑定到Active Directory，则可能需要以下设置。
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

# 设置NetBox服务帐户的DN和密码。
AUTH_LDAP_BIND_DN = "CN=NETBOXSA, OU=Service Accounts,DC=example,DC=com"
AUTH_LDAP_BIND_PASSWORD = "demo"

# 如果要忽略证书错误，请包含此设置。这可能需要接受自签名证书。
# 请注意，这是一个NetBox特定的设置，它设置了：
# ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
LDAP_IGNORE_CERT_ERRORS = True

# 如果要根据服务器证书目录在服务器上验证LDAP服务器证书，请包含此设置。
# 请注意，这是一个NetBox特定的设置，它设置了：
# ldap.set_option(ldap.OPT_X_TLS_CACERTDIR, LDAP_CA_CERT_DIR)
LDAP_CA_CERT_DIR = '/etc/ssl/certs'

# 如果要使用自己的CA验证LDAP服务器证书，请包含此设置。
# 请注意，这是一个NetBox特定的设置，它设置了：
# ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, LDAP_CA_CERT_FILE)
LDAP_CA_CERT_FILE = '/path/to/example-CA.crt'
```

可以通过将`AUTH_LDAP_START_TLS = True`设置为启用STARTTLS，并使用`ldap://` URI方案进行配置。

### 用户身份验证

!!! info
    当使用Windows Server 2012+时，`AUTH_LDAP_USER_DN_TEMPLATE`应设置为None。

```python
from django_auth_ldap.config import LDAPSearch

# 此搜索匹配`sAMAccountName`等于提供的用户名的用户。如果用户的用户名不在其DN中（Active Directory），则需要此选项。
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=Users,dc=example,dc=com",
                                    ldap.SCOPE_SUBTREE,
                                    "(sAMAccountName=%(user)s)")

# 如果可以从用户的用户名生成用户的DN，我们不需要搜索。
AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=users,dc=example,dc=com"

# 您可以将用户属性映射到Django属性。
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}
```

### 用于权限的用户组

!!! info
    当使用Microsoft Active Directory时，可以通过使用`NestedGroupOfNamesType()`而不是`GroupOfNamesType()`来激活对嵌套组的支持。您还需要修改导入行以使用`NestedGroupOfNamesType`而不是`GroupOfNamesType`。

```python
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# 此搜索应返回用户所属的所有组。django_auth_ldap使用此来确定组
# 层次结构。
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("dc=example,dc=com", ldap.SCOPE_SUBTREE,
                                    "(objectClass=group)")
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

# 定义登录所需的组。
AUTH_LDAP_REQUIRE_GROUP = "CN=NETBOX_USERS,DC=example,DC=com"

# 镜像LDAP组分配。
AUTH_LDAP_MIRROR_GROUPS = True

# 使用组定义特殊用户类型。在分配超级用户权限时要非常小心。
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active,ou=groups,dc=example,dc=com",
    "is_staff": "cn=staff,ou=groups,dc=example,dc=com",
    "is_superuser": "cn=superuser,ou=groups,dc=example,dc=com"
}

# 为了获得更精细的权限，我们可以将LDAP组映射到Django组。
AUTH_LDAP_FIND_GROUP_PERMS = True

# 缓存组一小时以减少LDAP流量
AUTH_LDAP_CACHE_TIMEOUT = 3600

```

* `is_active` - 所有用户必须映射到至少这个组以启用身份验证。没有这个，用户无法登录。
* `is_staff` - 映射到这个组的用户可以访问管理工具；这相当于手动创建用户时检查“staff status”框。这不授予任何特定权限。
* `is_superuser` - 映射到这个组的用户将被授予超级用户状态。超级用户隐式授予所有权限。

!!! warning
    如果组（分明的名称）在LDAP目录中不存在，身份验证将失败。

## 与Active Directory进行身份验证

将Active Directory集成到身份验证可能会有些具有挑战性，因为它可能需要处理不同的登录格式。此解决方案将允许用户使用其完整的用户主体名称（User Principal Name，UPN）或仅使用用户名来登录，通过根据`sAMAccountName`或`userPrincipalName`来过滤DN。以下配置选项将允许用户以`username`或`username@domain.tld`的格式登录。

与之前一样，配置选项在文件`ldap_config.py`中定义。首先，将`AUTH_LDAP_USER_SEARCH`选项修改为以下内容：

```python
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=Users,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(|(userPrincipalName=%(user)s)(sAMAccountName=%(user)s))"
)
```

此外，`AUTH_LDAP_USER_DN_TEMPLATE`应设置为`None`，如前几节所述。接下来，将`AUTH_LDAP_USER_ATTR_MAP`修改为以下内容：

```python
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "email": "mail",
    "first_name": "givenName",
    "last_name": "sn",
}
```

最后，我们需要添加另一个配置选项，`AUTH_LDAP_USER_QUERY_FIELD`。将以下内容添加到您的LDAP配置文件中：

```python
AUTH_LDAP_USER_QUERY_FIELD = "username"
```

使用这些配置选项，您的用户将能够以UPN后缀或不带UPN后缀的方式登录。

### 示例配置

!!! info
    此配置旨在作为模板提供，但可能需要根据您的环境进行修改。

```python
import ldap
from django_auth_ldap.config import LDAPSearch, NestedGroupOfNamesType

# 服务器URI
AUTH_LDAP_SERVER_URI = "ldaps://ad.example.com:3269"

# 如果要绑定到Active Directory，可能需要以下设置。
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

# 设置NetBox服务账户的DN和密码。
AUTH_LDAP_BIND_DN = "CN=NETBOXSA,OU=Service Accounts,DC=example,DC=com"
AUTH_LDAP_BIND_PASSWORD = "demo"

# 如果要忽略证书错误，请包括此设置。这可能需要接受自签名证书。
# 请注意，这是一个NetBox特有的设置，它设置：
#     ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
LDAP_IGNORE_CERT_ERRORS = False

# 如果要验证LDAP服务器证书与服务器上的CA证书目录，请包括此设置。
# 请注意，这是一个NetBox特有的设置，它设置：
#     ldap.set_option(ldap.OPT_X_TLS_CACERTDIR, LDAP_CA_CERT_DIR)
LDAP_CA_CERT_DIR = '/etc/ssl/certs'

# 如果要验证LDAP服务器证书与自己的CA，请包括此设置。
# 请注意，这是一个NetBox特有的设置，它设置：
#     ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, LDAP_CA_CERT_FILE)
LDAP_CA_CERT_FILE = '/path/to/example-CA.crt'

# 此搜索匹配sAMAccountName等于提供的用户名的用户。如果用户的用户名不在其DN中（Active Directory），则需要此选项。
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=Users,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(|(userPrincipalName=%(user)s)(sAMAccountName=%(user)s))"
)

# 如果可以通过用户的用户名生成用户的DN，则不需要搜索。
AUTH_LDAP_USER_DN_TEMPLATE = None

# 您可以将用户属性映射到Django属性，如下所示。
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "email": "mail",
    "first_name": "givenName",
    "last_name": "sn",
}

AUTH_LDAP_USER_QUERY_FIELD = "username"

# 此搜索应返回用户所属的所有组。django_auth_ldap使用此来确定组
# 层次结构。
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(objectClass=group)"
)
AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()

# 定义要登录所需的组。
AUTH_LDAP_REQUIRE_GROUP = "CN=NETBOX_USERS,DC=example,DC=com"

# 镜像LDAP组分配。
AUTH_LDAP_MIRROR_GROUPS = True

# 使用组定义特殊用户类型。在分配超级用户状态时要特别小心。
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active,ou=groups,dc=example,dc=com",
    "is_staff": "cn=staff,ou=groups,dc=example,dc=com",
    "is_superuser": "cn=superuser,ou=groups,dc=example,dc=com"
}

# 为了更精细的权限，我们可以将LDAP组映射到Django组。
AUTH_LDAP_FIND_GROUP_PERMS = True

# 缓存组1小时以减少LDAP流量
AUTH_LDAP_CACHE_TIMEOUT = 3600
AUTH_LDAP_ALWAYS_UPDATE_USER = True
```

## LDAP故障排除

`systemctl restart netbox` 重新启动NetBox服务，以应用对 `ldap_config.py` 的任何更改。如果存在语法错误，NetBox进程将无法启动，并且错误将被记录到 `/var/log/messages`。

要解决LDAP用户/组查询问题，请将以下 [logging](../configuration/system.md#logging) 配置添加或合并到 `configuration.py` 中：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'netbox_auth_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/opt/netbox/local/logs/django-ldap-debug.log',
            'maxBytes': 1024 * 500,
            'backupCount': 5,
        },
    },
    'loggers': {
        'django_auth_ldap': {
            'handlers': ['netbox_auth_log'],
            'level': 'DEBUG',
        },
    },
}
```

确保指定的日志文件和路径存在，并且可以由应用程序服务帐户进行写入和执行。重新启动NetBox服务并尝试登录到站点，以触发对此文件的日志条目记录。
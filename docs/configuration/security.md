# 安全性和身份验证参数

## ALLOW_TOKEN_RETRIEVAL

默认值：True

如果禁用此选项，则API令牌的值将不会在每个令牌的初始创建后显示。用户在创建令牌之前**必须**记录令牌的值，否则将丢失。请注意，这会影响**所有**用户，不考虑分配的权限。

---

## ALLOWED_URL_SCHEMES

!!! 提示 "动态配置参数"

默认值：`('file', 'ftp', 'ftps', 'http', 'https', 'irc', 'mailto', 'sftp', 'ssh', 'tel', 'telnet', 'tftp', 'vnc', 'xmpp')`

这是一个允许在NetBox中呈现链接时引用的允许的URL方案列表。请注意，只有在此列表中指定的方案才会被接受：如果添加自己的方案，请确保复制所有默认值（不包括不希望的方案）。

---

## AUTH_PASSWORD_VALIDATORS

此参数作为配置Django内置密码验证器的通道，用于本地用户帐户。如果配置，每当用户的密码更新以确保满足最低要求（例如长度或复杂性）时，这些验证器将被应用。下面提供了一个示例。有关可用选项的更多详细信息，请参见[Django文档](https://docs.djangoproject.com/en/stable/topics/auth/passwords/#password-validation)。

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
]
```

---

## CORS_ORIGIN_ALLOW_ALL

默认值：False

如果为True，则将接受来自所有来源的跨源资源共享（CORS）请求。如果为False，则将使用白名单（见下文）。

---

## CORS_ORIGIN_WHITELIST

## CORS_ORIGIN_REGEX_WHITELIST

这些设置指定了被授权进行跨站API请求的来源列表。使用
`CORS_ORIGIN_WHITELIST` 来定义一个精确的主机名列表，或使用 `CORS_ORIGIN_REGEX_WHITELIST` 来定义一组正则表达式。 （如果 `CORS_ORIGIN_ALLOW_ALL` 为True，则这些设置无效。）例如：

```python
CORS_ORIGIN_WHITELIST = [
    'https://example.com',
]
```

---

## CSRF_COOKIE_NAME

默认值：`csrftoken`

用于跨站请求伪造（CSRF）身份验证令牌的cookie的名称。有关更多详细信息，请参见[Django文档](https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-name)。

---

## CSRF_COOKIE_SECURE

默认值：False

如果为true，则用于跨站请求伪造（CSRF）保护的cookie将被标记为安全，这意味着它只能通过HTTPS连接发送。

---

## CSRF_TRUSTED_ORIGINS

默认值：`[]`

定义不安全（例如 `POST`）请求的受信任来源列表。这是传递给Django的 [`CSRF_TRUSTED_ORIGINS`](https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-CSRF_TRUSTED_ORIGINS) 设置。请注意，列出的每个主机必须指定一个方案（例如 `http://` 或 `https://`）。

```python
CSRF_TRUSTED_ORIGINS = (
    'http://netbox.local',
    'https://netbox.local',
)
```

---

## DEFAULT_PERMISSIONS

!!! 信息 "此参数在NetBox v3.6中引入。"

默认值：

```python
{
    'users.view_token': ({'user': '$user'},),
    'users.add_token': ({'user': '$user'},),
    'users.change_token': ({'user': '$user'},),
    'users.delete_token': ({'user': '$user'},),
}
```

此参数定义了自动应用于**任何**经过身份验证的用户的对象权限，而不考虑数据库中定义的权限。默认情况下，此参数被定义为允许所有用户管理自己的API令牌，但可以用于任何目的进行覆盖。

例如，要允许所有用户创建以单词“temp”开头的设备角色，您可以配置如下：

```python
DEFAULT_PERMISSIONS = {
    'dcim.add_devicerole': (
        {'name__startswith': 'temp'},
    )
}
```

!!! 警告
    为此参数设置自定义值将覆盖上面显示的默认权限映射。如果要保留默认映射，请确保在自定义配置中重现它。

---

## EXEMPT_VIEW_PERMISSIONS

默认值：空列表

一个免除视图权限执行的NetBox模型列表。列在此处的模型将被所有用户（包括经过身份验证和匿名用户）查看。

以 `<app>.<model>` 的形式列出模型。例如：

```python
EXEMPT_VIEW_PERMISSIONS = [
    'dcim.site',
    'dcim.region',
    'ipam.prefix',
]
```

要免除**所有**模型的视图权限执行，请设置以下内容。 （请注意，`EXEMPT_VIEW_PERMISSIONS` 必须是可迭代的。）

```python
EXEMPT_VIEW_PERMISSIONS = ['*']
```

!!! 注意
    使用通配符不会影响某些可能敏感的模型，例如用户权限。如果需要免除这些模型，必须单独指定它们。

---

## LOGIN_PERSISTENCE

默认值：False

如果为true，则每个有效请求后，将自动重置用户身份验证会话的生存期。例如，如果 [`LOGIN_TIMEOUT`](#login_timeout) 配置为14天（默认值），并且一个会话在五天后到期的用户发出了一个NetBox请求（带有有效的会话cookie），会话的生存期将被重置为14天。

请注意，启用此设置会导致NetBox在每个请求中更新用户会话在数据库中（或根据[`SESSION_FILE_PATH`](#session_file_path)的配置在文件

中），这可能会在非常活跃的环境中引入重大开销。它还允许活跃用户无限期地保持对NetBox的身份验证。

---

## LOGIN_REQUIRED

默认值：False

将此设置为True将只允许经过身份验证的用户访问NetBox的任何部分。默认情况下，匿名用户被允许访问NetBox中的大多数数据，但不能进行任何更改。

---

## LOGIN_TIMEOUT

默认值：1209600秒（14天）

在登录时为NetBox用户发放的身份验证cookie的生命周期（以秒为单位）。

---

## LOGOUT_REDIRECT_URL

默认值：`'home'`

用户注销后重定向到的视图名称或URL。

---

## SECURE_SSL_REDIRECT

默认值：False

如果为true，则将自动重定向所有非HTTPS请求以使用HTTPS。

!!! 警告
    在启用此选项之前，请确保您的前端HTTP守护程序已正确配置以正确转发HTTP方案。不正确配置的前端可能导致无限循环重定向。

---

## SESSION_COOKIE_NAME

默认值：`sessionid`

用于会话身份验证的会话cookie的名称。有关更多详细信息，请参见[Django文档](https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-name)。

---

## SESSION_COOKIE_SECURE

默认值：False

如果为true，则用于会话身份验证的cookie将被标记为安全，这意味着它只能通过HTTPS连接发送。

---

## SESSION_FILE_PATH

默认值：None

在用户访问NetBox时，会话数据用于跟踪经过身份验证的用户。默认情况下，NetBox将会话数据存储在其PostgreSQL数据库中。但是，这会阻止对没有写入数据库访问权限的NetBox备用实例进行身份验证。或者，可以在此处指定本地文件路径，NetBox将会将会话数据存储为文件而不是使用数据库。请注意，NetBox系统用户必须对此路径具有读写权限。
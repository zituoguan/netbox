# 系统参数

## BASE_PATH

默认值：None

访问NetBox时要使用的基本URL路径。不包括方案或域名。例如，如果安装在 https://example.com/netbox/，则设置为：

```python
BASE_PATH = 'netbox/'
```

---

## DEFAULT_LANGUAGE

默认值：`en-us`（美国英语）

定义了未指定语言/区域设置的请求的默认首选语言/区域设置。这用于更改日期和数字的显示以适应用户的区域设置。参见标准语言代码的[列表](http://www.i18nguy.com/unicode/language-identifiers.html)。（此参数映射到Django的[`LANGUAGE_CODE`](https://docs.djangoproject.com/en/stable/ref/settings/#language-code)内部设置。）

!!! 注意
    更改此参数不会更改NetBox中使用的语言。我们希望在未来的NetBox版本中提供翻译支持。

---

## DOCS_ROOT

默认值：`$INSTALL_ROOT/docs/`

NetBox文档的文件系统路径。在Web界面中提供上下文敏感文档时使用。默认情况下，这将是根NetBox安装路径内的`docs/`目录。（将其设置为`None`以禁用嵌入式文档。）

---

## EMAIL

为了发送电子邮件，NetBox需要配置电子邮件服务器。在`EMAIL`配置参数中，可以定义以下项：

* `SERVER` - 电子邮件服务器的主机名或IP地址（如果在本地运行，请使用`localhost`）
* `PORT` - 用于连接的TCP端口（默认值：`25`）
* `USERNAME` - 用于身份验证的用户名
* `PASSWORD` - 用于身份验证的密码
* `USE_SSL` - 连接到服务器时是否使用SSL（默认值：`False`）
* `USE_TLS` - 连接到服务器时是否使用TLS（默认值：`False`）
* `SSL_CERTFILE` - PEM格式的SSL证书文件的路径（可选）
* `SSL_KEYFILE` - PEM格式的SSL私钥文件的路径（可选）
* `TIMEOUT` - 连接等待的时间，以秒为单位（默认值：`10`）
* `FROM_EMAIL` - 由NetBox发送的电子邮件的发件人地址

!!! 注意
    `USE_SSL` 和 `USE_TLS` 参数是互斥的。

仅在出现关键事件或配置为[日志记录](#logging)时，NetBox才会发送电子邮件。如果要测试电子邮件服务器配置，Django提供了一个方便的[send_mail()](https://docs.djangoproject.com/en/stable/topics/email/#send-mail)函数，可以在NetBox shell中访问：

```no-highlight
# python ./manage.py nbshell
>>> from django.core.mail import send_mail
>>> send_mail(
  'Test Email Subject',
  'Test Email Body',
  'noreply-netbox@example.com',
  ['users@example.com'],
  fail_silently=False
)
```

---

## ENABLE_LOCALIZATION

默认值：False

确定是否启用了本地化功能。这应该只在开发或测试目的下启用，因为netbox尚未完全本地化。开启这个功能将会根据浏览器的地区设置本地化数字和日期格式（覆盖任何配置的[系统默认设置](./date-time.md#date-and-time-formatting)），以及翻译来自第三方模块的某些字符串。

---

## HTTP_PROXIES

默认值：None

用于从NetBox发出的出站请求（例如发送webhook请求）的HTTP代理的字典。代理应根据模式（HTTP和HTTPS）进行指定，如[Python请求库文档](https://requests.readthedocs.io/en/latest/user/advanced/#proxies)中所述。例如：

```python
HTTP_PROXIES = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
}
```

---

## INTERNAL_IPS

默认值：`('127.0.0.1', '::1')`

一组被视为系统内部的IP地址，用于控制调试输出的显示。例如，只有从列出的IP地址之一（并且[`DEBUG`](#debug)为true）的客户端访问NetBox时，调试工具栏才可见。

---

## JINJA2_FILTERS

默认值：`{}`

带有键作为过滤器名称和值作为可调用函数的自定义jinja2过滤器的字典。有关更多信息，请参见[Jinja2文档](https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters)。例如：

```python
def uppercase(x):
    return str(x).upper()

JINJA2_FILTERS = {
    'uppercase': uppercase,
}
```

---

## LOGGING

默认情况下，将记录所有INFO级别或更高级别的消息到控制台。另外，如果[`DEBUG`](#debug)为False，并且已配置电子邮件访问，则会将ERROR和CRITICAL消息发送到[`ADMINS`](#admins)中定义的用户。

NetBox运行的Django框架允许自定义日志格式和目标。有关更多信息，请参阅[Django日志文档](https://docs.djangoproject.com/en/stable/topics/logging/)。以下是一个示例，将所有INFO和更高级别的消息写入本地文件：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/netbox.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### 可用的日志记录器

* `netbox.<app>.<model>` - 用于模型特定日志消息的通用形式
* `netbox.auth.*` - 身份验证事件
* `netbox.api.views.*` - 处理REST API的业务逻辑的视图
* `netbox.reports.*` - 报告执行（`module.name`）
* `netbox.scripts.*` - 自定义脚本执行（`module.name`）
* `netbox.views.*` - 处理Web UI的业务逻辑的视图

---

## MEDIA_ROOT

默认值：$INSTALL_ROOT/netbox/media/

存储媒体文件（例如图像附件）的位置的文件路径。默认情况下，这是基本NetBox安装路径内的`netbox/media/`目录。

---

## REPORTS_ROOT

默认值：`$INSTALL_ROOT/netbox/reports/`

[自定义报告](../customization/reports.md)的文件路径位置。默认情况下，这是基本NetBox安装路径内的`netbox/reports/`目录。

---

## SCRIPTS_ROOT

默认值：`$INSTALL_ROOT/netbox/scripts/`

[自定义脚本](../customization/custom-scripts.md)的文件路径位置。默认情况下，这是基本NetBox安装路径内的`netbox/scripts/`目录。

---

## SEARCH_BACKEND

默认值：`'netbox.search.backends.CachedValueSearchBackend'`

所需搜索后端类的点路径。`CachedValueSearchBackend`是当前在NetBox中提供的唯一搜索后端，但可以使用此设置启用自定义后端。

---

## STORAGE_BACKEND

默认值：None（本地存储）

用于处理上传文件（例如图像附件）的后端存储引擎。NetBox支持与[`django-storages`](https://django-storages.readthedocs.io/en/stable/)包集成，该包提供了多个流行的文件存储服务的后端。如果未配置，将使用本地文件系统存储。

指定的存储后端的配置参数定义在`STORAGE_CONFIG`设置下。

---

## STORAGE_CONFIG

默认值：空

用于存储后端配置为`STORAGE_BACKEND`的配置参数的字典。要在此处使用的特定参数与每个后端特定;有关更多详细信息，请参见[`django-storages`文档](https://django-storages.readthedocs.io/en/stable/)。

如果未定义`STORAGE_BACKEND`，则将忽略此设置。

---

# 身份验证

## 本地身份验证

可以在NetBox的管理用户界面的“身份验证和授权”部分中创建本地用户帐户和组。此界面仅对启用了“staff”权限的用户可用。

每个用户帐户至少必须设置用户名和密码。用户帐户还可以包含名字、姓氏和电子邮件地址。还可以在管理UI中为用户和/或组分配[权限](../permissions.md)。

## 远程身份验证

除了本地身份验证之外，还可以配置NetBox通过远程后端提供用户身份验证。这可以通过将`REMOTE_AUTH_BACKEND`配置参数设置为适当的后端类来完成。NetBox为远程身份验证提供了几种选项。

### LDAP身份验证

```python
REMOTE_AUTH_BACKEND = 'netbox.authentication.LDAPBackend'
```

NetBox包括一个支持LDAP的身份验证后端。有关此后端的更多详细信息，请参阅[LDAP安装文档](../../installation/6-ldap.md)。

### HTTP标头身份验证

```python
REMOTE_AUTH_BACKEND = 'netbox.authentication.RemoteUserBackend'
```

在NetBox中进行远程身份验证的另一种选项是启用基于HTTP标头的用户分配。前端HTTP服务器（例如nginx或Apache）将客户端身份验证作为NetBox外部流程执行，并通过HTTP标头传递有关经过身份验证的用户的信息。默认情况下，用户是通过`REMOTE_USER`标头分配的，但可以通过`REMOTE_AUTH_HEADER`配置参数进行自定义。

还可以通过`REMOTE_USER_FIRST_NAME`、`REMOTE_USER_LAST_NAME`和`REMOTE_USER_EMAIL`标头提供用户配置文件信息。在身份验证过程中，这些信息将保存到用户配置文件中。这些标头可以像`REMOTE_USER`标头一样进行自定义。

### 单一登录（SSO）

```python
REMOTE_AUTH_BACKEND = 'social_core.backends.google.GoogleOAuth2'
```

NetBox支持通过[python-social-auth](https://github.com/python-social-auth)库进行单一登录身份验证。要启用SSO，请在`social_core` Python包内指定所需身份验证后端的路径。请参阅完整的[支持的身份验证后端列表](https://github.com/python-social-auth/social-core/tree/master/social_core/backends)以查看可用选项。

大多数远程身份验证后端需要通过以`SOCIAL_AUTH_`为前缀的设置进行一些额外的配置。这些设置将自动从NetBox的`configuration.py`文件中导入。此外，可以通过`SOCIAL_AUTH_PIPELINE`参数自定义[身份验证流程](https://python-social-auth.readthedocs.io/en/latest/pipeline.html)。（NetBox的默认流程在`netbox/settings.py`中定义，供您参考。）

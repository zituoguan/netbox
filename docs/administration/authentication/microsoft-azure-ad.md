# Microsoft Azure AD

本指南解释了如何使用[Microsoft Azure Active Directory (AD)](https://azure.microsoft.com/en-us/services/active-directory/)作为身份验证后端，配置NetBox的单一登录（SSO）支持。

## Azure AD 配置

### 1. 创建测试用户（可选）

在AD中创建一个新用户，用于测试。如果您已经创建了适合的帐户，可以跳过此步骤。

### 2. 创建应用注册

在Azure Active Directory仪表板中，导航到**添加 > 应用注册**。

![添加应用注册](../../media/authentication/azure_ad_add_app_registration.png)

输入注册的名称（例如"NetBox"），并确保选择了"单租户"选项。

在"重定向 URI"下，选择平台为"Web"，并输入指向您的NetBox安装的路径，以`/oauth/complete/azuread-oauth2/`结尾。请注意，此URI**必须**以`https://`开头，除非您引用本地主机（仅用于开发目的）。

![应用注册参数](../../media/authentication/azure_ad_app_registration.png)

完成后，记下应用程序（客户端）ID；在配置NetBox时将使用它。

![完成的应用注册](../../media/authentication/azure_ad_app_registration_created.png)

!!! 提示 "多租户身份验证"
    NetBox还支持通过Azure AD进行多租户身份验证，但是需要不同的后端和额外的配置参数。请参阅[`python-social-auth`文档](https://python-social-auth.readthedocs.io/en/latest/backends/azuread.html#tenant-support)以获取有关多租户身份验证的详细信息。

### 3. 创建密钥

在查看新创建的应用注册时，点击"客户端凭据"下的"添加证书或密钥"链接。在"客户端密钥"选项卡下，点击"新的客户端密钥"按钮。

![添加客户端密钥](../../media/authentication/azure_ad_add_client_secret.png)

您可以选择指定描述并选择密钥的生存期，但这是可选的。

![客户端密钥参数](../../media/authentication/azure_ad_client_secret.png)

完成后，记下密钥值（而不是密钥ID）；在配置NetBox时将使用它。

![客户端密钥参数](../../media/authentication/azure_ad_client_secret_created.png)

## NetBox 配置

### 1. 输入配置参数

在`configuration.py`中输入以下配置参数，替换为您自己的值：

```python
REMOTE_AUTH_BACKEND = 'social_core.backends.azuread.AzureADOAuth2'
SOCIAL_AUTH_AZUREAD_OAUTH2_KEY = '{APPLICATION_ID}'
SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET = '{SECRET_VALUE}'
```

### 2. 重启NetBox

重新启动NetBox服务，以使新配置生效。通常可以使用以下命令来执行此操作：

```no-highlight
sudo systemctl restart netbox
```

## 测试

如果已经通过身份验证登录了NetBox，请退出，并单击右上角的"登录"按钮。您应该看到正常的登录表单，以及使用Azure AD进行身份验证的选项。单击该链接。

![NetBox Azure AD登录表单](../../media/authentication/netbox_azure_ad_login.png)

您将被重定向到Microsoft的身份验证门户。输入测试帐户的用户名/电子邮件和密码以继续。您可能还需要批准此应用程序访问您的帐户。

![Azure AD登录门户](../../media/authentication/azure_ad_login_portal.png)

如果成功，您将被重定向回NetBox界面，并以AD用户身份登录。您可以通过导航到您的个人资料（使用右上角的按钮）来验证这一点。

此用户帐户已在NetBox本地复制，并且现在可以在NetBox管理UI中分配组和权限。

## 故障排除

### 重定向URI不匹配

Azure要求认证的客户端请求一个与您在第二步中为应用程序配置的内容相匹配的重定向URI。这个URI**必须**以`https://`开头（除非您在开发过程中引用`localhost`）。

如果Azure抱怨所请求的URI以`http://`（而不是HTTPS）开头，那么很可能是您的HTTP服务器配置错误或者位于负载均衡器后面，因此NetBox不知道正在使用HTTPS。要强制使用HTTPS重定向URI，可以在`configuration.py`中设置`SOCIAL_AUTH_REDIRECT_IS_HTTPS = True`，根据[python-social-auth文档](https://python-social-auth.readthedocs.io/en/latest/configuration/settings.html#processing-redirects-and-urlopen)。

### 验证成功后未登录

如果在成功验证后被重定向到NetBox界面，但未登录，请仔细检查配置的后端和应用程序注册。本指南中的说明仅适用于使用单租户应用注册的`azuread.AzureADOAuth2`后端。

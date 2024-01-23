# Okta

本指南解释了如何使用[Okta](https://www.okta.com/)作为身份验证后端，为NetBox配置单一登录（SSO）支持。

## Okta 配置

!!! 提示 "Okta开发者账号"
    Okta提供免费的开发者账号，网址为：<https://developer.okta.com/>。

### 1. 创建测试用户（可选）

在Okta管理门户中创建一个新用户，用于测试。如果您已经创建了适合的帐户，可以跳过此步骤。

### 2. 创建应用注册

在Okta管理仪表板内，导航到**Applications > Applications**，然后点击"Create App Integration"按钮。选择"OIDC"作为登录方法，以及"Web application"作为应用程序类型。

![创建应用注册](../../media/authentication/okta_create_app_registration.png)

在下一页中，为应用集成命名（例如"NetBox"）并指定登录和注销的URI。这些URI应遵循以下格式：

* 登录URI：`https://{netbox}/oauth/complete/okta-openidconnect/`
* 注销URI：`https://{netbox}/oauth/disconnect/okta-openidconnect/`

![Web应用集成](../../media/authentication/okta_web_app_integration.png)

在"Assignments"下，选择适合您的组织的受控访问设置。单击"Save"完成创建。

完成后，请注意以下参数。这些将用于配置NetBox。

* 客户端ID（Client ID）
* 客户端密钥（Client secret）
* Okta域（Okta domain）

![Okta集成参数](../../media/authentication/okta_integration_parameters.png)

## NetBox 配置

### 1. 输入配置参数

在`configuration.py`中输入以下配置参数，替换为您自己的值：

```python
REMOTE_AUTH_BACKEND = 'social_core.backends.okta_openidconnect.OktaOpenIdConnect'
SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY = '{Client ID}'
SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET = '{Client secret}'
SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL = 'https://{Okta域名}/oauth2/'
```

### 2. 重启NetBox

重新启动NetBox服务，以使新配置生效。通常可以使用以下命令来执行此操作：

```no-highlight
sudo systemctl restart netbox
```

## 测试

如果已经通过身份验证登录了NetBox，请退出，并单击右上角的"登录"按钮。您应该看到正常的登录表单，以及使用Okta进行身份验证的选项。单击该链接。

![NetBox Okta登录表单](../../media/authentication/netbox_okta_login.png)

您将被重定向到Okta的身份验证门户。输入测试帐户的用户名/电子邮件和密码以继续。您可能还需要批准此应用程序访问您的帐户。

![Okta登录门户](../../media/authentication/okta_login_portal.png)

如果成功，您将被重定向回NetBox界面，并以Okta用户身份登录。您可以通过导航到您的个人资料（使用右上角的按钮）来验证这一点。

此用户帐户已在NetBox本地复制，并且现在可以在NetBox管理UI中分配组和权限。

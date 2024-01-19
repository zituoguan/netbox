# 认证与权限

## 基于对象的权限

NetBox 拥有一个非常强大的权限系统，远远超出了其底层 Django 框架的基于模型的权限。在 NetBox 中分配权限涉及几个维度：

* 权限适用的对象类型
* 被授予权限的用户和/或群组
* 权限允许的操作（例如查看、添加、更改等）
* 任何限制条件，限制权限的应用到特定子集的对象

限制条件的实施是 NetBox 管理员能够分配每个对象权限的关键：用户可以被限制为只查看或与基于对象属性的任意子集互动。例如，你可能限制某个用户只能查看特定 VRF 中的前缀或 IP 地址。或者你可能限制一个群组只能修改特定区域内的设备。

在创建权限时，权限约束以 JSON 格式声明，并且与 Django ORM 查询非常相似。例如，这里有一个匹配 VLAN ID 在 100 到 199 之间的保留 VLAN 的约束：

```json
[
  {
    "vid__gte": 100,
    "vid__lt": 200
  },
  {
    "status": "reserved"
  }
]
```

有关权限约束的更多信息，请查看[权限文档](../administration/permissions.md)。

## LDAP 认证

NetBox 包含一个内置的认证后端，用于对远程 LDAP 服务器上的用户进行认证。[安装文档](../installation/6-ldap.md)提供了有关此功能的更多详细信息。

## 单点登录 (SSO)

NetBox 与开源 [python-social-auth](https://github.com/python-social-auth) 库集成，提供了[众多选项](https://python-social-auth.readthedocs.io/en/latest/backends/index.html#supported-backends)用于单点登录 (SSO) 认证。这些包括：

* Cognito
* GitHub 和 GitHub Enterprise
* GitLab
* Google
* Hashicorp Vault
* Keycloak
* Microsoft Azure AD
* Microsoft Graph
* Okta
* OIDC

...等等。也可以根据需要使用 python-social-auth 的基本 OAuth、OpenID 和 SAML 类来构建自己的自定义后端。您可以在 NetBox 的[认证文档](../administration/authentication/overview.md)中找到一些配置 SSO 的示例。
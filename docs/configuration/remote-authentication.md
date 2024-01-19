# 远程认证设置

以下列出的配置参数控制NetBox的远程认证。请注意，必须将`REMOTE_AUTH_ENABLED`设置为true，以使这些设置生效。

---

## REMOTE_AUTH_AUTO_CREATE_GROUPS

默认值：`False`

如果为true，NetBox将在`REMOTE_AUTH_GROUP_HEADER`头中指定的组如果不存在将自动创建。（需要`REMOTE_AUTH_ENABLED`。）

---

## REMOTE_AUTH_AUTO_CREATE_USER

默认值：`False`

如果为true，NetBox将自动为通过远程服务认证的用户创建本地帐户。（需要`REMOTE_AUTH_ENABLED`。）

---

## REMOTE_AUTH_BACKEND

默认值：`'netbox.authentication.RemoteUserBackend'`

这是用于外部用户认证的自定义[Django身份验证后端](https://docs.djangoproject.com/en/stable/topics/auth/customizing/)的Python路径。NetBox提供了两个内置后端（如下所示），但其他包或插件也可以提供自定义身份验证后端。为单个后端提供字符串，或为多个后端提供可迭代的后端，将按给定的顺序尝试。

* `netbox.authentication.RemoteUserBackend`
* `netbox.authentication.LDAPBackend`

---

## REMOTE_AUTH_DEFAULT_GROUPS

默认值：`[]`（空列表）

在使用远程认证创建新用户帐户时分配的组列表。（需要`REMOTE_AUTH_ENABLED`。）

---

## REMOTE_AUTH_DEFAULT_PERMISSIONS

默认值：`{}`（空字典）

在使用远程认证创建新用户帐户时分配的权限的映射。字典中的每个键都应设置为要应用于权限的属性的字典，或设置为`None`以允许所有对象。（需要`REMOTE_AUTH_ENABLED`为True和`REMOTE_AUTH_GROUP_SYNC_ENABLED`为False。）

---

## REMOTE_AUTH_ENABLED

默认值：`False`

NetBox可以配置为支持远程用户认证，通过推断由HTTP反向代理（例如nginx或Apache）设置的HTTP头来进行用户认证。将此设置为`True`以启用此功能。（本地认证仍然会生效作为后备。）（如果禁用`REMOTE_AUTH_ENABLED`，`REMOTE_AUTH_DEFAULT_GROUPS`将不起作用）

---

## REMOTE_AUTH_GROUP_HEADER

默认值：`'HTTP_REMOTE_USER_GROUP'`

在使用远程用户认证时，这是通知NetBox当前已认证用户的HTTP头的名称。例如，要使用请求头`X-Remote-User-Groups`，需要将其设置为`HTTP_X_REMOTE_USER_GROUPS`。（需要`REMOTE_AUTH_ENABLED`和`REMOTE_AUTH_GROUP_SYNC_ENABLED`）

---

## REMOTE_AUTH_GROUP_SEPARATOR

默认值：`|`（管道符）

`REMOTE_AUTH_GROUP_HEADER`拆分为单个组的分隔符。这需要与您的认证代理协调。（需要`REMOTE_AUTH_ENABLED`和`REMOTE_AUTH_GROUP_SYNC_ENABLED`）

---

## REMOTE_AUTH_GROUP_SYNC_ENABLED

默认值：`False`

NetBox可以配置为通过推断由HTTP反向代理（例如nginx或Apache）设置的HTTP头来同步远程用户组的用户认证。将此设置为`True`以启用此功能。（本地认证仍然会生效作为后备。）（需要`REMOTE_AUTH_ENABLED`。）

---

## REMOTE_AUTH_HEADER

默认值：`'HTTP_REMOTE_USER'`

在使用远程用户认证时，这是通知NetBox当前已认证用户的HTTP头的名称。例如，要使用请求头`X-Remote-User`，需要将其设置为`HTTP_X_REMOTE_USER`。（需要`REMOTE_AUTH_ENABLED`。）

---

## REMOTE_AUTH_USER_EMAIL

默认值：`'HTTP_REMOTE_USER_EMAIL'`

在使用远程用户认证时，这是通知NetBox当前已认证用户的电子邮件地址的HTTP头的名称。例如，要使用请求头`X-Remote-User-Email`，需要将其设置为`HTTP_X_REMOTE_USER_EMAIL`。（需要`REMOTE_AUTH_ENABLED`。）

---

## REMOTE_AUTH_USER_FIRST_NAME

默认值：`'HTTP_REMOTE_USER_FIRST_NAME'`

在使用远程用户认证时，这是通知NetBox当前已认证用户的名字的HTTP头的名称。例如，要使用请求头`X-Remote-User-First-Name`，需要将其设置为`HTTP_X_REMOTE_USER_FIRST_NAME`。（需要`REMOTE_AUTH_ENABLED`。）

---

## REMOTE_AUTH_USER_LAST_NAME

默认值：`'HTTP_REMOTE_USER_LAST_NAME'`

在使用远程用户认证时，这是通知NetBox当前已认证用户的姓氏的HTTP头的名称。例如，要使用请求头`X-Remote-User-Last-Name`，需要将其设置为`HTTP_X_REMOTE_USER_LAST_NAME`。（需要`REMOTE_AUTH_ENABLED`。）

---

## REMOTE_AUTH_SUPERUSER_GROUPS

默认值：`[]`（空列表）

将远程用户提升为超级用户的组列表。如果在下次登录时组不在列表中，角色将被撤销。（需要`REMOTE_AUTH_ENABLED`和`REMOTE_AUTH_GROUP_SYNC_ENABLED`）

---

## REMOTE_AUTH_SUPERUSERS

默认值：`[]`（空列表）

在登录时提升为超级用户的用户列表。如果下次登录时用户不在列表中，角色将被撤销。（需要`REMOTE_AUTH_ENABLED`和`REMOTE_AUTH_GROUP_SYNC_ENABLED`）

---

## REMOTE_AUTH_STAFF_GROUPS

默认值：`[]`（空列表）

将远程用户提升为工作人员的组列表。如果在下次登录时组不在列表中，角色将被撤销。（需要`REMOTE_AUTH_ENABLED`和`REMOTE_AUTH_GROUP_SYNC_ENABLED`）

---

## REMOTE_AUTH_STAFF_USERS

默认值：`[]`（空列表）

在登录时提升为工作人员的用户列表。如果下次登录时用户不在列表中，角色将被撤销。（需要`REMOTE_AUTH_ENABLED`和`REMOTE_AUTH_GROUP_SYNC_ENABLED`）

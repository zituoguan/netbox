# 导出模板

NetBox允许用户定义自定义模板，用于在导出对象时使用。要创建导出模板，请导航到自定义 > 导出模板。

每个导出模板与某种类型的对象相关联。例如，如果您为VLAN创建一个导出模板，您的自定义模板将显示在VLAN列表的“导出”按钮下。每个导出模板必须有一个名称，并可以选择指定特定的导出[MIME类型](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)和/或文件扩展名。

导出模板必须使用[Jinja2](https://jinja.palletsprojects.com/)编写。

!!! note
    名称 `table` 保留供内部使用。

!!! warning
    导出模板是使用用户提交的代码呈现的，根据某些条件可能存在安全风险。仅授予受信任的用户创建或修改导出模板的权限。

在渲染导出模板时，从数据库返回的对象列表存储在 `queryset` 变量中，通常您会使用 `for` 循环对其进行迭代。可以按名称访问对象属性。例如：

```jinja2
{% for rack in queryset %}
Rack: {{ rack.name }}
Site: {{ rack.site.name }}
Height: {{ rack.u_height }}U
{% endfor %}
```

要在模板中访问对象的自定义字段，请使用 `cf` 属性。例如，`{{ obj.cf.color }}` 将返回 `obj` 上名为 `color` 的自定义字段的值（如果有的话）。

如果需要在导出模板中使用配置上下文数据，您应该使用函数 `get_config_context` 来获取所有配置上下文数据。例如：
```
{% for server in queryset %}
{% set data = server.get_config_context() %}
{{ data.syslog }}
{% endfor %}
```

导出模板的 `as_attachment` 属性控制其在渲染时的行为。如果为 true，则渲染的内容将作为可下载文件返回给用户。如果为 false，则将在浏览器中显示它（例如，用于生成HTML内容时可能会很方便）。

每个导出模板可以选择定义一个MIME类型和文件扩展名。默认MIME类型为 `text/plain`。


## REST API 集成

当需要提供身份验证凭据（例如，当启用了 [`LOGIN_REQUIRED`](../configuration/security.md#login_required) 时）时，建议通过REST API呈现导出模板。这允许客户端指定身份验证令牌。要通过REST API呈现导出模板，请对模型的列表端点进行 `GET` 请求，并附加指定导出模板名称的 `export` 参数。例如：

```
GET /api/dcim/sites/?export=MyTemplateName
```

请注意，响应的主体将仅包含已呈现的导出模板内容，而不是JSON对象或列表。

## 示例

以下是一个设备导出模板示例，将从设备列表生成一个简单的Nagios配置。

```
{% for device in queryset %}{% if device.status and device.primary_ip %}define host{
        use                     generic-switch
        host_name               {{ device.name }}
        address                 {{ device.primary_ip.address.ip }}
}
{% endif %}{% endfor %}
```

生成的输出将类似于以下内容：

```
define host{
        use                     generic-switch
        host_name               switch1
        address                 192.0.2.1
}
define host{
        use                     generic-switch
        host_name               switch2
        address                 192.0.2.2
}
define host{
        use                     generic-switch
        host_name               switch3
        address                 192.0.2.3
}
```

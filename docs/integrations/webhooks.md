# Webhooks

NetBox可以通过[事件规则](../features/event-rules.md)配置，以响应内部对象更改而向远程系统传输出站Webhook。接收方可以根据这些Webhook消息中的数据执行相关任务。

例如，假设您希望在设备的操作状态更改为活动时自动配置监控系统开始监控设备，并在其他状态下将其从监控中删除。您可以在NetBox中为设备模型创建一个Webhook，并制定其内容和目标URL以在接收系统上实现所需的更改。只要满足配置的约束条件，NetBox将自动发送Webhook。

!!! 警告 "安全通知"
    Webhooks支持包含用户提交的代码以生成URL、自定义标头和有效负载，这在某些情况下可能存在安全风险。只授予可信用户创建或修改Webhook的权限。

## Jinja2模板支持

支持[Jinja2模板](https://jinja.palletsprojects.com/)用于`URL`、`additional_headers`和`body_template`字段。这使用户能够在请求标头中传递对象数据，以及制定定制的请求正文。可以通过制定请求内容来启用与外部系统的直接交互，确保出站消息以接收方期望和理解的格式进行。

例如，您可以创建一个NetBox Webhook，以便在创建IP地址时自动触发Slack消息。您可以通过以下配置来实现：

* 对象类型：IPAM > IP地址
* HTTP方法：`POST`
* URL：Slack入站Webhook URL
* HTTP内容类型：`application/json`
* 正文模板：`{"text": "已创建IP地址{{ data['address'] }}由{{ username }}!"}`

### 可用上下文

以下数据在Jinja2模板的上下文中可用：

* `event` - 触发Webhook的事件类型：created、updated或deleted。
* `model` - 触发更改的NetBox模型。
* `timestamp` - 事件发生的时间（以[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)格式）。
* `username` - 与更改相关的用户帐户的名称。
* `request_id` - 唯一的请求ID。这可以用于关联与单个请求相关的多个更改。
* `data` - 对象的当前状态的详细表示。这通常等同于NetBox的REST API中模型的表示。
* `snapshots` - 更改之前和之后对象状态的最小“快照”；以`prechange`和`postchange`命名的字典键提供。虽然不如完全序列化的表示详尽，但包含足够的信息来传达发生了什么变化。

### 默认请求正文

如果未指定正文模板，则请求正文将填充一个包含上下文数据的JSON对象。例如，新创建的站点可能如下所示：

```json
{
    "event": "created",
    "timestamp": "2021-03-09 17:55:33.968016+00:00",
    "model": "site",
    "username": "jstretch",
    "request_id": "fdbca812-3142-4783-b364-2e2bd5c16c6a",
    "data": {
        "id": 19,
        "name": "站点 1",
        "slug": "site-1",
        "status": 
            "value": "active",
            "label": "Active",
            "id": 1
        },
        "region": null,
        ...
    },
    "snapshots": {
        "prechange": null,
        "postchange": {
            "created": "2021-03-09",
            "last_updated": "2021-03-09T17:55:33.851Z",
            "name": "站点 1",
            "slug": "site-1",
            "status": "active",
            ...
        }
    }
}
```

!!! 注意
    从NetBox 3.7开始，设置条件Webhook已被移至[事件规则](../features/event-rules.md)中。

## Webhook处理

使用[事件规则](../features/event-rules.md)，当检测到更改时，任何结果的Webhook都将被放入Redis队列以进行处理。这使得用户的请求可以在无需等待出站Webhook处理完成的情况下完成。然后，`rqworker`进程从队列中提取Webhook并将HTTP请求发送到其各自的目标。可以在系统 > 后台任务下的NetBox管理UI中检查当前的Webhook队列和任何失败的Webhook。

如果响应具有2XX状态代码，则请求被视为成功；否则，请求将被标记为失败。失败的请求可以通过管理UI手动重试。

## 故障排除

为了帮助验证出站Webhook的内容是否被正确呈现，NetBox提供了一个简单的HTTP监听器，可以在本地运行以接收并显示Webhook请求。首先，将所需Webhook的目标URL修改为`http://localhost:9000/`。这将指示NetBox将请求发送到TCP端口9000上的本地服务器。然后，从NetBox根目录启动Webhook接收器服务：

```no-highlight
$ python netbox/manage.py webhook_receiver
Listening on port http://localhost:9000. Stop with CONTROL-C.
```

您可以通过向其发送任何HTTP请求来测试接收器本身。例如：

```no-highlight
$ curl -X POST http://localhost:9000 --data '{"foo": "bar"}'
```

服务器将打印类似以下的输出：

```no-highlight
[1] Tue, 07 Apr 2020 17:44:02 GMT 127.0.0.1 "POST / HTTP/1.1" 200 -
Host: localhost:9000
User-Agent: curl/7.58.0
Accept: */*
Content-Length: 14
Content-Type: application/x-www-form-urlencoded

{"foo": "bar"}
------------
```

请注意，`webhook_receiver`实际上不会对接收到的信息执行任何操作：它只会打印请求标头和正文以供检查。

现在，当NetBox触发并处理Webhook时，您应该在Webhook接收程序正在侦听的终端中看到其标头和内容。如果没有，请检查`rqworker`进程是否正在运行以及Webhook事件是否被放入队列（在NetBox管理UI中可见）。

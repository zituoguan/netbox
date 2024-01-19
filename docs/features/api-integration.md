# API 和集成

NetBox 包含了许多功能，使得它能够与为您的网络提供动力的其他工具和资源集成。

## REST API

NetBox 的 REST API，由 [Django REST 框架](https://www.django-rest-framework.org/) 提供支持，提供了一个既健壮又易于访问的接口，用于创建、修改和删除对象。通过采用 HTTP 进行传输和 JSON 进行数据封装，REST API 易于任何平台上的客户端使用，并非常适合自动化任务。

```no-highlight
curl -s -X POST \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
http://netbox/api/ipam/prefixes/ \
--data '{"prefix": "192.0.2.0/24", "site": {"name": "Branch 12"}}'
```

REST API 使用基于令牌的认证，它将 API 客户端映射到用户账户及其分配的权限。API 端点使用 OpenAPI 完全文档化，并且 NetBox 甚至包含了一个方便的基于浏览器的 API 版本用于探索。开源的 [pynetbox](https://github.com/netbox-community/pynetbox) 和 [go-netbox](https://github.com/netbox-community/go-netbox) API 客户端库也可分别用于 Python 和 Go。

要了解更多关于此功能的信息，请查看 [REST API 文档](../integrations/rest-api.md)。

## GraphQL API

NetBox 还提供了 [GraphQL](https://graphql.org/) API 来补充其 REST API。GraphQL 使得可以对任意对象和字段进行复杂查询，使客户端能够仅从 NetBox 检索其需要的特定数据。这是一个专门用于高效查询的只读 API。与 REST API 一样，GraphQL API 使用基于令牌的认证。

要了解更多关于此功能的信息，请查看 [GraphQL API 文档](../integrations/graphql-api.md)。

## Webhooks

Webhook 是一种机制，用于向一些外部系统传达在 NetBox 中发生的变化。例如，当 NetBox 中的设备状态更新时，您可能想要通知监控系统。要做到这一点，首先创建一个 [webhook](../models/extras/webhook.md)，标识远程接收器（URL）、HTTP 方法和任何其他必要参数。然后，定义一个由设备变化触发的 [事件规则](../models/extras/eventrule.md) 来传输 webhook。

当 NetBox 检测到设备的变化时，包含变化细节及其发起者的 HTTP 请求将被发送到指定的接收器。Webhooks 是构建基于事件的自动化流程的优秀机制。要了解更多关于此功能的信息，请查看 [webhooks 文档](../integrations/webhooks.md)。

## Prometheus 指标

NetBox 包含一个特殊的 `/metrics` 视图，它为 [Prometheus](https://prometheus.io/) 抓取器暴露指标，由开源 [django-prometheus](https://github.com/korfuri/django-prometheus) 库提供支持。要了解更多关于此功能的信息，请查看 [Prometheus 指标文档](../integrations/prometheus-metrics.md)。
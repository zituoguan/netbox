# GraphQL API 概述

NetBox提供了一个只读的[GraphQL](https://graphql.org/) API，以补充其REST API。该API由[Graphene](https://graphene-python.org/)库和[Graphene-Django](https://docs.graphene-python.org/projects/django/en/latest/)驱动。

## 查询

GraphQL允许客户端指定要包含在响应中的任意嵌套字段列表。所有查询都发送到根目录的`/graphql` API端点。例如，要返回每个具有活动状态的电路的电路ID和供应商名称，可以发出如下请求：

```
curl -H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
-H "Accept: application/json" \
http://netbox/graphql/ \
--data '{"query": "query {circuit_list(status:\"active\") {cid provider {name}}}"}'
```

响应将包括请求的数据，以JSON格式呈现：

```json
{
  "data": {
    "circuits": [
      {
        "cid": "1002840283",
        "provider": {
          "name": "CenturyLink"
        }
      },
      {
        "cid": "1002840457",
        "provider": {
          "name": "CenturyLink"
        }
      }
    ]
  }
}
```

!!! 注意
    建议将返回的数据通过JSON解析器（如`jq`）进行更好的可读性处理。

NetBox为每种对象类型提供了单数和复数查询字段：

* `$OBJECT`：返回单个对象。必须指定对象的唯一ID，如`(id: 123)`。
* `$OBJECT_list`：返回对象列表，可以选择使用给定的参数进行筛选。

例如，使用查询`device(id:123)`来获取特定设备（通过其唯一ID标识），使用查询`device_list`（带有可选的筛选条件）来获取所有设备。

有关构建GraphQL查询的详细信息，请参阅[Graphene文档](https://docs.graphene-python.org/en/latest/)以及[GraphQL查询文档](https://graphql.org/learn/queries/)。

## 筛选

GraphQL API使用与UI和REST API相同的筛选逻辑。筛选可以在紧随查询名称后的括号内指定为键值对。例如，以下内容将仅返回状态为活动的North Carolina地区的站点：

```
{"query": "query {site_list(region:\"north-carolina\", status:\"active\") {name}}"}
```
此外，可以在相关对象列表上进行筛选，如下面的查询所示：

```
{
  device_list {
    id
    name
    interfaces(enabled: true) {
      name
    }
  }
}
```

## 多个返回类型

某些查询可以返回多种类型的对象，例如电缆端子可以返回电路端子、控制台端口和许多其他对象。可以使用[内联片段](https://graphql.org/learn/schema/#union-types)进行查询，如下所示：

```
{
    cable_list {
      id
      a_terminations {
        ... on CircuitTerminationType {
          id
          class_type
        }
        ... on ConsolePortType {
          id
          class_type
        }
        ... on ConsoleServerPortType {
          id
          class_type
        }
      }
    }
}

```
字段“class_type”是在查看返回的数据或进行筛选时区分对象类型的简便方法。它包含类名，例如“CircuitTermination”或“ConsoleServerPort”。

## 认证

NetBox的GraphQL API使用与其REST API相同的API身份验证令牌。通过在请求中附加`Authorization` HTTP标头，将身份验证令牌附加到请求中，格式如下：

```
Authorization: Token $TOKEN
```

## 禁用GraphQL API

如果不需要，可以通过将[`GRAPHQL_ENABLED`](../configuration/miscellaneous.md#graphql_enabled)配置参数设置为False并重新启动NetBox来禁用GraphQL API。

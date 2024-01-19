# REST API概述

## 什么是REST API？

REST代表[表征状态传输](https://en.wikipedia.org/wiki/Representational_state_transfer)。它是一种特定类型的API，它使用HTTP请求和[JavaScript对象表示法（JSON）](https://www.json.org/)来促进对应用程序中对象的创建、检索、更新和删除（CRUD）操作。每种操作都与特定的HTTP动词关联：

* `GET`：检索对象或对象列表
* `POST`：创建对象
* `PUT` / `PATCH`：修改现有对象。`PUT`需要指定所有强制字段，而`PATCH`只需要指定正在修改的字段。
* `DELETE`：删除现有对象

此外，`OPTIONS`动词可以用于检查特定的REST API端点，并返回所有支持的操作及其可用的参数。

REST API的主要好处之一是其人性化。因为它使用HTTP和JSON，所以可以使用常见工具在命令行上与NetBox数据进行交互。例如，我们可以使用`curl`和`jq`从NetBox请求一个IP地址并输出JSON。以下命令使用`curl`和`jq`向NetBox发出HTTP `GET`请求，请求有关特定IP地址的信息，该IP地址由其主键标识，并使用`jq`以更人性化的格式呈现返回的原始JSON数据。 （通过`jq`传递输出不是严格要求的，但可以使其更容易阅读。）

```no-highlight
curl -s http://netbox/api/ipam/ip-addresses/2954/ | jq '.'
```

```json
{
  "id": 2954,
  "url": "http://netbox/api/ipam/ip-addresses/2954/",
  "family": {
    "value": 4,
    "label": "IPv4"
  },
  "address": "192.168.0.42/26",
  "vrf": null,
  "tenant": null,
  "status": {
    "value": "active",
    "label": "Active"
  },
  "role": null,
  "assigned_object_type": "dcim.interface",
  "assigned_object_id": 114771,
  "assigned_object": {
    "id": 114771,
    "url": "http://netbox/api/dcim/interfaces/114771/",
    "device": {
      "id": 2230,
      "url": "http://netbox/api/dcim/devices/2230/",
      "name": "router1",
      "display_name": "router1"
    },
    "name": "et-0/1/2",
    "cable": null,
    "connection_status": null
  },
  "nat_inside": null,
  "nat_outside": null,
  "dns_name": "",
  "description": "Example IP address",
  "tags": [],
  "custom_fields": {},
  "created": "2020-08-04",
  "last_updated": "2020-08-04T14:12:39.666885Z"
}
```

IP地址的每个属性都表示为JSON对象的属性。字段可以包括自己的嵌套对象，就像上面的`assigned_object`字段一样。每个对象都包括一个名为`id`的主键，该主键在数据库中唯一标识它。

## 交互式文档

在运行中的NetBox实例上，全面的REST API端点的交互式文档位于`/api/schema/swagger-ui/`。此界面提供了一个方便的沙箱，用于研究和实验特定的端点和请求类型。API本身也可以通过Web浏览器来探索，方法是导航到其根目录`/api/`。

## 端点层次结构

NetBox的整个REST API位于API根目录下，即`https://<hostname>/api/`。URL结构在根级别上按应用程序划分：circuits、DCIM、extras、IPAM、plugins、tenancy、users和virtualization。在每个应用程序中，都存在一个单独的路径用于每个模型。例如，提供程序和电路对象位于“circuits”应用程序下：

* `/api/circuits/providers/`
* `/api/circuits/circuits/`

同样，站点、机架和设备对象位于“DCIM”应用程序下：

* `/api/dcim/sites/`
* `/api/dcim/racks/`
* `/api/dcim/devices/`

可用端点的完整层次结构可以通过在Web浏览器中导航到API根目录来查看。

每个模型通常都有与之关联的两个视图：列表视图和详细视图。列表视图用于检索多个对象的列表并创建新对象。详细视图用于检索、更新或删除单个现有对象。所有对象都通过其数字主键（`id`）引用。

* `/api/dcim/devices/` - 列出现有设备或创建新设备
* `/api/dcim/devices/123/` - 检索、更新或删除ID为123的设备

可以使用一组查询参数来过滤对象的列表。例如，要查找属于ID为123的设备的所有接口：

```
GET /api/dcim/interfaces/?device_id=123
```

有关详细信息，请参阅[过滤文档](../reference/filtering.md)。

## 序列化

REST API使用两种类型的序列化器来表示模型数据：基本序列化器和嵌套序列化器。基本序列化器用于呈现模型的完整视图。这包括组成模型的所有数据库表字段，可能包括附加元数据。基本序列化器包括对父对象的关系，但**不包括**子对象。例如，`VLANSerializer`包括其父VLANGroup（如果有的话）的嵌套表示，但不包括任何分配的前缀。

```json
{
    "id": 1048,
    "site": {
        "id": 7,
        "url": "http://netbox/api/dcim/sites/7/",
        "name": "Corporate HQ",
        "slug": "corporate-hq"
    },
    "group": {
        "id": 4,
        "url": "http://netbox/api/ipam/vlan-groups/4/",
        "name": "Production",
        "slug": "production"
    },
    "vid": 101,
    "name": "Users-Floor1",
    "tenant": null,
    "status": {
        "value": 1,
        "label": "Active"
    },
    "role": {
        "id": 9,
        "url": "http://netbox/api/ipam/roles/9/",
        "name": "User Access",
        "slug": "user-access"
    },
    "description": "",
    "display_name": "101 (Users-Floor1)",
    "custom_fields": {}
}
```

### 关联对象

关联对象（例如`ForeignKey`字段）使用嵌套序列化器表示。嵌套序列化器提供了一个对象的最小表示，仅包括其直接URL以及足够的信息以向用户显示对象。在执行写API操作（`POST`、`PUT`和`PATCH`）时，可以通过数字ID（主键）或足够唯一以返回所需对象的一组属性来指定相关对象。

例如，在创建新设备时，可以通过NetBox ID（PK）指定其机架：

```json
{
    "name": "MyNewDevice",
    "rack": 123,
    ...
}
```

或通过一组足够唯一标识机架的嵌套属性：

```json
{
    "name": "MyNewDevice",
    "rack": {
        "site": {
            "name": "Equinix DC6"
        },
        "name": "R204"
    },
    ...
}
```

请注意，如果提供的参数不能返回完全一个对象，将引发验证错误。

### 通用关系

NetBox中的一些对象具有可以引用多种类型对象的属性，称为通用关系。例如，IP地址可以分配给设备接口或虚拟机接口。在通过REST API进行此分配时，我们必须指定两个属性：

* `assigned_object_type` - 已分配对象的内容类型，定义为`<app>.<model>`
* `assigned_object_id` - 分配对象的唯一数字ID

这些值一起在NetBox中标识一个唯一的对象。分配的对象（如果有）由IP地址模型上的`assigned_object`属性表示。

```no-highlight
curl -X POST \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
-H "Accept: application/json; indent=4" \
http://netbox/api/ipam/ip-addresses/ \
--data '{
    "address": "192.0.2.1/24",
    "assigned_object_type": "dcim.interface",
    "assigned_object_id": 69023
}'
```

```json
{
    "id": 56296,
    "url": "http://netbox/api/ipam/ip-addresses/56296/",
    "assigned_object_type": "dcim.interface",
    "assigned_object_id": 69000,
    "assigned_object": {
        "id": 69000,
        "url": "http://netbox/api/dcim/interfaces/69023/",
        "device": {
            "id": 2174,
            "url": "http://netbox/api/dcim/devices/2174/",
            "name": "device105",
            "display_name": "device105"
        },
        "name": "ge-0/0/0",
        "cable": null,
        "connection_status": null
    },
    ...
}
```

如果您希望将此IP地址分配给虚拟机接口，您将设置`assigned_object_type`为`virtualization.vminterface`，并相应地更新对象ID。

### 简要格式

大多数API端点支持可选的“简要”格式，该格式仅返回响应中每个对象的最小表示。当您只需要一个可用对象的列表而无需任何相关数据时，这非常有用，例如在填写表单中填充下拉列表时。例如，IP地址的默认（完整）格式如下：

```
GET /api/ipam/prefixes/13980/

{
    "id": 13980,
    "url": "http://netbox/api/ipam/prefixes/13980/",
    "family": {
        "value": 4,
        "label": "IPv4"
    },
    "prefix": "192.0.2.0/24",
    "site": {
        "id": 3,
        "url": "http://netbox/api/dcim/sites/17/",
        "name": "Site 23A",
        "slug": "site-23a"
    },
    "vrf": null,
    "tenant": null,
    "vlan": null,
    "status": {
        "value": "container",
        "label": "Container"
    },
    "role": {
        "id": 17,
        "url": "http://netbox/api/ipam/roles/17/",
        "name": "Staging",
        "slug": "staging"
    },
    "is_pool": false,
    "description": "Example prefix",
    "tags": [],
    "custom_fields": {},
    "created": "2018-12-10",
    "last_updated": "2019-03-01T20:02:46.173540Z"
}
```

简要格式要简洁得多：

```
GET /api/ipam/prefixes/13980/?brief=1

{
    "id": 13980,
    "url": "http://netbox/api/ipam/prefixes/13980/",
    "family": 4,
    "prefix": "10.40.3.0/24"
}
```

简要格式适用于列表和单个对象。

### 排除配置上下文

在通过REST API检索设备和虚拟机时，默认情况下，每个对象都会包括其渲染的[配置上下文数据](../features/context-data.md)。具有大量上下文数据的用户在返回多个对象时可能会观察到性能不佳，特别是在页面大小非常大的情况下。为了解决这个问题，可以通过将查询参数`?exclude=config_context`附加到请求中来从响应数据中排除上下文数据。此参数适用于列表视图和详细视图。

## 分页

包含许多对象的API响应将进行分页以提高效率。列表端点返回的根JSON对象包含以下属性：

* `count`：与查询匹配的所有对象的总数
* `next`：指向下一页结果的超链接（如果适用）
* `previous`：指向上一页结果的超链接（如果适用）
* `results`：当前页面上的对象列表

以下是分页响应的示例：

```
HTTP 200 OK
Allow: GET, POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 2861,
    "next": "http://netbox/api/dcim/devices/?limit=50&offset=50",
    "previous": null,
    "results": [
        {
            "id": 231,
            "name": "Device1",
            ...
        },
        {
            "id": 232,
            "name": "Device2",
            ...
        },
        ...
    ]
}
```

默认页面由 [`PAGINATE_COUNT`](../configuration/default-values.md#paginate_count) 配置参数确定，默认为 50。但是，可以通过在请求中指定所需的 `offset` 和 `limit` 查询参数来覆盖此设置。例如，如果您希望一次检索一百个设备，您可以发出以下请求：

```
http://netbox/api/dcim/devices/?limit=100
```

响应将返回第 1 到第 100 个设备。响应中的 `next` 属性提供的 URL 将返回第 101 到第 200 个设备：

```json
{
    "count": 2861,
    "next": "http://netbox/api/dcim/devices/?limit=100&offset=100",
    "previous": null,
    "results": [...]
}
```

最多可以返回的对象数量由 [`MAX_PAGE_SIZE`](../configuration/miscellaneous.md#max_page_size) 配置参数限制，默认为 1000。将其设置为 `0` 或 `None` 将取消最大限制。然后，API 使用者可以传递 `?limit=0` 以单个请求检索 _所有_ 匹配的对象。

!!! 警告
    禁用页面大小限制会导致潜在的非常耗费资源的请求，因为一个 API 请求可以有效地检索整个数据库中的整个表。

## 与对象互动

### 检索多个对象

要查询 NetBox 的对象列表，请向模型的 _list_ 终端发出 `GET` 请求。对象列在响应对象的 `results` 参数下。

```no-highlight
curl -s -X GET http://netbox/api/ipam/ip-addresses/ | jq '.'
```

```json
{
  "count": 42031,
  "next": "http://netbox/api/ipam/ip-addresses/?limit=50&offset=50",
  "previous": null,
  "results": [
    {
      "id": 5618,
      "address": "192.0.2.1/24",
      ...
    },
    {
      "id": 5619,
      "address": "192.0.2.2/24",
      ...
    },
    {
      "id": 5620,
      "address": "192.0.2.3/24",
      ...
    },
    ...
  ]
}
```

### 检索单个对象

要查询 NetBox 的单个对象，请发出 `GET` 请求到模型的 _detail_ 终端，指定其唯一的数字 ID。

!!! 注意
    需要注意的是，需要包括结尾的斜杠。如果省略此斜杠，将返回 302 重定向。

```no-highlight
curl -s -X GET http://netbox/api/ipam/ip-addresses/5618/ | jq '.'
```

```json
{
  "id": 5618,
  "address": "192.0.2.1/24",
  ...
}
```

### 创建新对象

要创建一个新对象，请发出 `POST` 请求到模型的 _list_ 终端，其中包含与要创建的对象相关的 JSON 数据。请注意，所有写操作都需要使用 REST API 令牌；有关更多信息，请参阅[身份验证部分](#authenticating-to-the-api)。还要确保将 `Content-Type` HTTP 标头设置为 `application/json`。

```no-highlight
curl -s -X POST \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
http://netbox/api/ipam/prefixes/ \
--data '{"prefix": "192.0.2.0/24", "site": 6}' | jq '.'
```

```json
{
  "id": 18691,
  "url": "http://netbox/api/ipam/prefixes/18691/",
  "family": {
    "value": 4,
    "label": "IPv4"
  },
  "prefix": "192.0.2.0/24",
  "site": {
    "id": 6,
    "url": "http://netbox/api/dcim/sites/6/",
    "name": "US-East 4",
    "slug": "us-east-4"
  },
  "vrf": null,
  "tenant": null,
  "vlan": null,
  "status": {
    "value": "active",
    "label": "Active"
  },
  "role": null,
  "is_pool": false,
  "description": "",
  "tags": [],
  "custom_fields": {},
  "created": "2020-08-04",
  "last_updated": "2020-08-04T20:08:39.007125Z"
}
```

### 创建多个对象

要使用单个请求创建模型的多个实例，请发出 `POST` 请求到模型的 _list_ 终端，其中包含表示要创建的每个实例的 JSON 对象列表。如果成功，响应将包含新创建实例的列表。下面的示例说明了创建三个新站点的过程。

```no-highlight
curl -X POST -H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
-H "Accept: application/json; indent=4" \
http://netbox/api/dcim/sites/ \
--data '[
{"name": "Site 1", "slug": "site-1", "region": {"name": "United States"}},
{"name": "Site 2", "slug": "site-2", "region": {"name": "United States"}},
{"name": "Site 3", "slug": "site-3", "region": {"name": "United States"}}
]'
```

```json
[
    {
        "id": 21,
        "url": "http://netbox/api/dcim/sites/21/",
        "name": "Site 1",
        ...
    },
    {
        "id": 22,
        "url": "http://netbox/api/dcim/sites/22/",
        "name": "Site 2",
        ...
    },
    {
        "id": 23,
        "url": "http://netbox/api/dcim/sites/23/",
        "name": "Site 3",
        ...
    }
]
```

### 更新对象

要修改已创建的对象，请发出 `PATCH` 请求到模型的 _detail_ 终端，指定其唯一的数值 ID。包括您希望在对象上更新的任何数据。与对象创建一样，还必须指定 `Authorization` 和 `Content-Type` 头。

```no-highlight
curl -s -X PATCH \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
http://netbox/api/ipam/prefixes/18691/ \
--data '{"status": "reserved"}' | jq '.'
```

```json
{
  "id": 18691,
  "url": "http://netbox/api/ipam/prefixes/18691/",
  "family": {
    "value": 4,
    "label": "IPv4"
  },
  "prefix": "192.0.2.0/24",
  "site": {
    "id": 6,
    "url": "http://netbox/api/dcim/sites/6/",
    "name": "US-East 4",
    "slug": "us-east-4"
  },
  "vrf": null,
  "tenant": null,
  "vlan": null,
  "status": {
    "value": "reserved",
    "label": "Reserved"
  },
  "role": null,
  "is_pool": false,
  "description": "",
  "tags": [],
  "custom_fields": {},
  "created": "2020-08-04",
  "last_updated": "2020-08-04T20:14:55.709430Z"
}
```

!!! 注意 "PUT 与 PATCH"
    NetBox REST API 支持使用 `PUT` 或 `PATCH` 来修改现有对象。不同之处在于 `PUT` 请求要求用户指定正在修改的对象的 _完整_ 表示，而 `PATCH` 请求只需包括要更新的属性。对于大多数情况，建议使用 `PATCH`。

### 更新多个对象

可以通过向模型的列表端点发出 `PUT` 或 `PATCH` 请求，并提供一个包含要删除的每个对象的数值 ID 和要更新的属性的字典列表，同时更新多个对象。例如，要将 ID 为 10 和 11 的站点更新为 "active" 状态，请发出以下请求：

```no-highlight
curl -s -X PATCH \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
http://netbox/api/dcim/sites/ \
--data '[{"id": 10, "status": "active"}, {"id": 11, "status": "active"}]'
```

请注意，对象之间的属性无需相同。例如，可以在同一个请求中更新一个站点的状态以及另一个站点的名称。

!!! 注意
    对象的批量更新是一个全或无操作，这意味着如果NetBox无法成功更新指定的任何对象（例如由于验证错误），则整个操作将被中止，不会更新任何对象。

### 删除对象

要从NetBox中删除对象，请发出 `DELETE` 请求到模型的 _detail_ 端点，指定其唯一的数值 ID。必须包括 `Authorization` 头来指定授权令牌，但此类请求不支持在请求体中传递任何数据。

```no-highlight
curl -s -X DELETE \
-H "Authorization: Token $TOKEN" \
http://netbox/api/ipam/prefixes/18691/
```

请注意，`DELETE` 请求不返回任何数据：如果成功，API 将返回 204（无内容）响应。

!!! 注意
    您可以使用带有详细信息（`-v`）标志的 `curl` 来检查 HTTP 响应代码。

### 删除多个对象

NetBox 支持通过向模型的列表端点发出 `DELETE` 请求，同时删除同一类型的多个对象，方法是提供一个包含要删除的每个对象的数值 ID 的字典列表。例如，要删除具有 ID 10、11 和 12 的站点，请发出以下请求：

```no-highlight
curl -s -X DELETE \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
http://netbox/api/dcim/sites/ \
--data '[{"id": 10}, {"id": 11}, {"id": 12}]'
```

!!! 注意
    批量删除对象是一种全有或全无的操作，这意味着如果 NetBox 无法删除任何指定的对象（例如由相关对象的依赖引起的），整个操作将被中止，不会删除任何对象。

## 身份验证

NetBox REST API 主要采用基于令牌的身份验证。为方便起见，当访问可浏览的 API 时，也可以使用基于 cookie 的身份验证。

### 令牌

令牌是映射到 NetBox 用户帐户的唯一标识符。每个用户可以拥有一个或多个令牌，用于在进行 REST API 请求时进行身份验证。要创建令牌，请转到您的用户配置文件下的 API 令牌页面。

默认情况下，所有用户都可以在用户控制面板中或通过 REST API 创建和管理自己的 REST API 令牌。可以通过覆盖 [`DEFAULT_PERMISSIONS`](../configuration/security.md#default_permissions) 配置参数来禁用此功能。

每个令牌包含一个 160 位密钥，表示为 40 个十六进制字符。创建令牌时，通常会将密钥字段留空，以便自动生成一个随机密钥。但是，NetBox 允许您指定密钥，以防需要将先前删除的令牌恢复到运行状态。

此外，可以将令牌设置为在特定时间到期。如果外部客户端需要临时访问 NetBox，则可以使用此功能。

!!! info "限制令牌检索"
    可以通过禁用 [`ALLOW_TOKEN_RETRIEVAL`](../configuration/security.md#allow_token_retrieval) 配置参数来限制检索先前创建的 API 令牌的密钥值的能力。

### 限制写操作

默认情况下，可以使用令牌执行通过 API 执行的所有用户可以通过 Web UI 执行的操作。取消选择“启用写操作”选项将限制使用令牌进行 API 请求仅限于读操作（例如 GET）。

#### 客户端 IP 限制

可以选择通过客户端 IP 地址对每个 API 令牌进行限制。如果为令牌定义了一个或多个允许的 IP 前缀/地址，则对于从定义的范围之外的 IP 地址连接的任何客户端，身份验证将失败。这允许将令牌的使用限制为特定客户端。（默认情况下，允许任何客户端 IP 地址。）

#### 为其他用户创建令牌

可以通过 REST API 为其他用户提供身份验证令牌。为此，请求用户必须分配 `users.grant_token` 权限。虽然所有用户默认情况下都具有创建自己令牌的权限，但此权限是为了允许为其他用户创建令牌。

!!! warning "行使谨慎"
    代表其他用户创建令牌的能力使请求者能够访问已创建的令牌。此功能旨在用于自动化服务的令牌配置，并应极度谨慎使用，以避免安全威胁。

### 身份验证到 API

通过将 `Authorization` 头设置为字符串 `Token` 后跟空格和用户的令牌，将身份验证令牌附加到请求中：

```
$ curl -H "Authorization: Token $TOKEN" \
-H "Accept: application/json; indent=4" \
https://netbox/api/dcim/sites/
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [...]
}
```

一个令牌对于已被豁免权限执行的只读操作是不需要的（使用 [`EXEMPT_VIEW_PERMISSIONS`](../configuration/security.md#exempt_view_permissions) 配置参数）。但是，如果需要一个令牌但在请求中不存在，API 将返回 403（禁止）响应：

```
$ curl https://netbox/api/dcim/sites/
{
    "detail": "Authentication credentials were not provided."
}
```

当使用令牌进行身份验证时，如果其上一次使用的时间距离现在已经超过60秒（或者从未记录过），它的`last_updated`时间将被更新为当前时间。这允许用户确定最近活跃的令牌是哪些。

!!! 注意
    在维护模式启用时，令牌的“上次使用”时间将不会更新。

### 初始令牌分配

理想情况下，每个用户应该通过 Web UI 自行分配他或她自己的 API 令牌。但是，您可能会遇到一种情况，其中一个令牌必须由用户本身通过 REST API 创建。NetBox 提供了一个特殊的端点，使用有效的用户名和密码组合来分配令牌。 （请注意，无论使用的接口如何，用户必须具有创建 API 令牌的权限。）

要通过 REST API 分配令牌，请将 `POST` 请求发送到 `/api/users/tokens/provision/` 端点：

```
$ curl -X POST \
-H "Content-Type: application/json" \
-H "Accept: application/json; indent=4" \
https://netbox/api/users/tokens/provision/ \
--data '{
    "username": "hankhill",
    "password": "I<3C3H8"
}'
```

请注意，在此请求中，我们 _不_ 传递现有的 REST API 令牌。如果提供的凭据有效，将会为用户自动生成一个新的 REST API 令牌。请注意，密钥将会自动生成，并且写入权限将会启用。

```json
{
    "id": 6,
    "url": "https://netbox/api/users/tokens/6/",
    "display": "3c9cb9 (hankhill)",
    "user": {
        "id": 2,
        "url": "https://netbox/api/users/users/2/",
        "display": "hankhill",
        "username": "hankhill"
    },
    "created": "2021-06-11T20:09:13.339367Z",
    "expires": null,
    "key": "9fc9b897abec9ada2da6aec9dbc34596293c9cb9",
    "write_enabled": true,
    "description": ""
}
```

## HTTP 头部

### `API-Version`

此头部指定了正在使用的 API 版本。它将始终与安装的 NetBox 版本匹配。例如，NetBox v3.4.2 将报告 API 版本为 `3.4`。

### `X-Request-ID`

此头部指定了分配给接收到的 API 请求的唯一 ID。它对于将请求与更改记录相关联非常有用。例如，在创建多个新对象之后，您可以根据请求的 ID 过滤对象更改 API 端点以检索结果的更改记录：

```
GET /api/extras/object-changes/?request_id=e39c84bc-f169-4d5f-bc1c-94487a1b18b5
```

请求 ID 也可以用于直接过滤许多对象，以返回由特定请求创建或更新的对象：

```
GET /api/dcim/sites/?created_by_request=e39c84bc-f169-4d5f-bc1c-94487a1b18b5
```

!!! 注意
    此头部包含在 _所有_ NetBox 响应中，尽管在使用 API 时最为实用。

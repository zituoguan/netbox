REST API过滤

## 过滤对象

可以通过将一个或多个查询参数附加到请求URL来过滤API列表端点返回的对象。例如，`GET /api/dcim/sites/?status=active` 将仅返回状态为 "active" 的站点。

可以连接多个参数以进一步缩小结果。例如，`GET /api/dcim/sites/?status=active&region=europe` 将仅返回欧洲地区内的活动站点。

通常，对于单个参数传递多个值将导致逻辑OR操作。例如，`GET /api/dcim/sites/?region=north-america&region=south-america` 将返回北美或南美的站点。但是，在字段可能具有多个值的情况下，例如标签，将使用逻辑AND操作。例如，`GET /api/dcim/sites/?tag=foo&tag=bar` 将仅返回同时应用了 "foo" 和 "bar" 标签的站点。

### 按选择字段过滤

一些模型具有仅限于特定选择的字段，例如Prefix模型上的 `status` 字段。要查找此字段的所有可用选择，请进行身份验证的 `OPTIONS` 请求到模型的列表端点，并使用 `jq` 提取相关参数：

```no-highlight
$ curl -s -X OPTIONS \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
http://netbox/api/ipam/prefixes/ | jq ".actions.POST.status.choices"
[
  {
    "value": "container",
    "display_name": "Container"
  },
  {
    "value": "active",
    "display_name": "Active"
  },
  {
    "value": "reserved",
    "display_name": "Reserved"
  },
  {
    "value": "deprecated",
    "display_name": "Deprecated"
  }
]
```

!!! 注意
    上述仅在用于身份验证请求的API令牌具有权限对该端点进行 `POST` 请求时才起作用。

### 按自定义字段过滤

要按自定义字段值过滤结果，请在自定义字段名称前添加 `cf_`。例如，以下查询将仅返回自定义字段名为 `foo` 等于 123 的站点：

```no-highlight
GET /api/dcim/sites/?cf_foo=123
```

可以将自定义字段与内置字段混合使用以进一步缩小结果。在创建自定义字符串字段时，所选择的过滤类型（松散 versus 精确）决定了是使用部分匹配还是完全匹配。

## 查找表达式

某些模型字段还支持使用其他查找表达式进行过滤。这允许进行否定和其他上下文特定的过滤。

这些查找表达式可以通过在所需字段的名称后添加后缀来应用，例如 `mac_address__n`。在这种情况下，过滤表达式是否定的，并且用两个下划线分隔。以下是不同字段类型支持的查找表达式的示例。

### 数字字段

数字字段（ASN、VLAN ID 等）支持这些查找表达式：

| 过滤   | 描述                    |
|--------|-------------------------|
| `n`    | 不等于                  |
| `lt`   | 小于                    |
| `lte`  | 小于或等于              |
| `gt`   | 大于                    |
| `gte`  | 大于或等于              |
| `empty`| 为空/Null（布尔）        |

以下是一个数字字段查找表达式的示例，它将返回所有VLAN ID大于900的VLAN：

```no-highlight
GET /api/ipam/vlans/?vid__gt=900
```

### 字符串字段

字符串字段（Name、Address 等）支持这些查找表达式：

| 过滤   | 描述                              |
|--------|-----------------------------------|
| `n`    | 不等于                            |
| `ic`   | 包含（不区分大小写）               |
| `nic`  | 不包含（不区分大小写）             |
| `isw`  | 以...开始（不区分大小写）           |
| `nisw` | 不以...开始（不区分大小写）         |
| `iew`  | 以...结束（不区分大小写）           |
| `niew` | 不以...结束（不区分大小写）         |
| `ie`   | 完全匹配（不区分大小写）           |
| `nie`  | 反向精确匹配（不区分大小写）       |
| `empty`| 为空/Null（布尔）                  |

以下是一个字符串字段上的查找表达式的示例，它将返回所有名称中包含 `switch` 的设备：

```no-highlight
GET /api/dcim/devices/?name__ic=switch
```

### 外键和其他字段

某些其他字段，即外键关系支持仅否定表达式 `n`。以下是外键上查找表达式的示例，它将返回所有VLAN Group ID不等于3203的VLAN：

```no-highlight
GET /api/ipam/vlans/?group_id__n=3203
```

## 对象排序

要按特定字段对结果进行排序，请包括 `ordering` 查询参数。例如，根据其设施值对站点列表进行排序：

```no-highlight
GET /api/dcim/sites/?ordering=facility
```

要反转排序，请在字段名称前添加连字符：

```no-highlight
GET /api/dcim/sites/?ordering=-facility
```

可以通过用逗号分隔字段名称来指定多个字段。例如：

```no-highlight
GET /api/dcim/sites/?ordering=facility,-name
```

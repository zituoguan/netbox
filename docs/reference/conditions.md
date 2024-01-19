# 条件

条件是NetBox用于评估一组数据是否符合规定条件的机制。它允许作者通过在一系列逻辑AND和OR语句的层次结构中声明任意数量的属性-值-操作元组来传达简单的逻辑。

## 条件

条件表示为一个JSON对象，具有以下键：

| 键名  | 必需   | 默认值  | 描述             |
|--------|--------|---------|-------------------|
| attr   | 是     | -       | 正在评估的数据内的键的名称 |
| value  | 是     | -       | 将与给定数据进行比较的参考值     |
| op     | 否     | `eq`    | 要执行的逻辑操作             |
| negate | 否     | False   | 是否反转条件的评估结果             |

### 可用的操作

* `eq`：等于
* `gt`：大于
* `gte`：大于或等于
* `lt`：小于
* `lte`：小于或等于
* `in`：存在于值列表中
* `contains`：包含指定的值

### 访问嵌套键

要访问嵌套的键，请使用点来表示到所需属性的路径。例如，假设以下数据：

```json
{
  "a": {
    "b": {
      "c": 123
    }
  }
}
```

以下条件将评估为true：

```json
{
  "attr": "a.b.c",
  "value": 123
}
```

### 示例

`name` 等于 "foo"：

```json
{
  "attr": "name",
  "value": "foo"
}
```

`name` 不等于 "foo"

```json
{
  "attr": "name",
  "value": "foo",
  "negate": true
}
```

`asn` 大于 65000：

```json
{
  "attr": "asn",
  "value": 65000,
  "op": "gt"
}
```

`status` 不是 "planned" 或 "staging"：

```json
{
  "attr": "status.value",
  "value": ["planned", "staging"],
  "op": "in",
  "negate": true
}
```

!!! 注意 "评估静态选择字段"
    在评估静态选择字段时要特别注意，例如上面的 `status` 字段。这些字段通常呈现为一个字典，指定了字段的原始值 (`value`) 和人类友好的标签 (`label`)。请确保指定您要匹配的是这两者中的哪一个。

## 条件集

多个条件可以组合成嵌套的集合，使用AND或OR逻辑。这是通过声明一个具有单个键 (`and` 或 `or`) 的JSON对象来完成的，该键包含一系列条件对象和/或子条件集。

### 示例

`status` 是 "active" 并且 `primary_ip4` 已定义，_或者_ 应用了 "exempt" 标签。

```json
{
  "or": [
    {
      "and": [
        {
          "attr": "status.value",
          "value": "active"
        },
        {
          "attr": "primary_ip4",
          "value": null,
          "negate": true
        }
      ]
    },
    {
      "attr": "tags.slug",
      "value": "exempt",
      "op": "contains"
    }
  ]
}
```

# 自定义字段

NetBox管理员可以通过在大多数对象类型上添加自定义字段来扩展NetBox内置的数据模型。有关更多信息，请参阅[自定义字段文档](../../customization/custom-fields.md)。

## 字段

### 模型

选择适用于此自定义字段的NetBox对象类型或类型。

### 名称

原始字段名称。这将在数据库和API中使用，并且应该仅由字母数字字符和下划线组成。（使用“标签”字段来指定自定义字段的人类友好名称。）

### 标签

自定义字段的可选人类友好名称。如果未定义，将使用字段的“名称”属性。

### 组名

如果此自定义字段应与其他字段分组，请在此处指定组的名称。未定义组的自定义字段将仅按权重和名称排序。

### 类型

此字段保存的数据类型。必须是以下之一：

| 类型               | 描述                             |
|--------------------|----------------------------------|
| 文本               | 自由格式文本（用于单行使用）     |
| 长文本             | 任意长度的自由格式文本；支持Markdown渲染 |
| 整数               | 整数（正数或负数）               |
| 布尔值             | 真或假                           |
| 日期               | ISO 8601格式的日期（YYYY-MM-DD） |
| URL                | 这将在Web用户界面中显示为链接      |
| JSON               | 以JSON格式存储的任意数据         |
| 选择               | 预定义的几个自定义选择项中的一个   |
| 多项选择           | 支持分配多个值的选择字段         |
| 对象               | 定义为`object_type`所定义的NetBox对象的单个对象 |
| 多个对象           | 一个或多个`object_type`所定义的NetBox对象 |

### 对象类型

仅适用于对象和多对象字段。指定正在引用的NetBox对象的类型。

### 权重

用于覆盖按名称对字段按字母顺序排序的数值权重。具有较低权重的自定义字段将在具有较高权重的字段之前列出。（请注意，如果定义了自定义字段组，权重适用于自定义字段组的上下文内。）

### 必填

如果选中，此自定义字段必须使用有效值填充，以使对象通过验证。

### 描述

字段用途的简要描述（可选）。

### 过滤逻辑

定义如何根据自定义字段值对过滤器进行评估。

| 选项     | 描述                  |
|----------|-----------------------|
| 禁用     | 禁用过滤              |
| 宽松匹配 | 匹配值的任何出现      |
| 精确匹配 | 仅匹配完整字段值      |

### UI可见

控制自定义字段是否在NetBox用户界面中显示。

| 选项 | 描述                                                         |
|--------|-------------------------------------------------------------|
| 始终   | 在查看对象时始终显示该字段（默认）                         |
| 如果设置 | 仅当定义了值时才显示该字段                                   |
| 隐藏   | 在查看对象时不显示该字段                                     |

### UI可编辑

控制在NetBox用户界面中对象上是否可以编辑自定义字段。

| 选项 | 描述                                                                                   |
|--------|---------------------------------------------------------------------------------------|
| 是     | 在编辑对象时可以更改字段的值（默认）                                                 |
| 否     | 在编辑对象时，字段的值会显示，但不可更改                                           |
| 隐藏   | 在编辑对象时不显示该字段                                                               |

### 默认值

在创建新对象时为自定义字段提供的默认值（可选）。此值必须表示为JSON。如果这是一个选择或多选字段，则必须是可用选择项之一。

### 选择集

仅适用于选择和多选自定义字段，这是字段的有效选择集。

### 可克隆

如果启用，当克隆现有对象时，将自动预填充此字段的值。

### 最小值

仅适用于数值自定义字段。最小有效值（可选）。

### 最大值

仅适用于数值自定义字段。最大有效值（可选）。

### 验证正则表达式

仅适用于基于字符串的自定义字段。用于验证字段值的正则表达式（可选）。

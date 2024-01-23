# 日志条目

NetBox中的大多数对象都支持日志记录。这是用户记录指示对NetBox中的资源进行的更改或工作的时间记录的能力。例如，数据中心技术员在更换故障电源供应时可能会为设备添加一条日志条目。

## 字段

### 种类

日志条目类型的一般分类（信息，成功，警告或危险）。

!!! tip
    可以通过在[`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices)配置参数下设置`JournalEntry.kind`来定义其他种类。

### 评论

日志条目的正文。支持[Markdown](../../reference/markdown.md)渲染。

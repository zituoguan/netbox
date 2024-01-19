# 搜索

NetBox v3.4引入了一种新的全局搜索机制，它使用`extras.CachedValue`模型将许多模型的离散字段值存储在单个表中。

## SearchIndex

要为模型启用搜索支持，请为其声明并注册`netbox.search.SearchIndex`的子类。通常，这将在应用程序的`search.py`模块中完成。

```python
from netbox.search import SearchIndex, register_search

@register_search
class MyModelIndex(SearchIndex):
    model = MyModel
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = ('site', 'device', 'status', 'description')
```

SearchIndex子类定义了其模型以及一个包含两个元组的列表，指定要索引的模型字段以及与每个字段关联的权重（优先级）。下面提供了字段权重分配的指导信息。

### 字段权重指南

| 权重   | 字段作用                                         | 示例                                               |
|--------|--------------------------------------------------|----------------------------------------------------|
| 50     | 唯一的序列化属性                                | Device.asset_tag                                   |
| 60     | 唯一的序列化属性（每个相关对象）                | Device.serial                                      |
| 100    | 主要人员标识符                                  | Device.name, Circuit.cid, Cable.label              |
| 110    | Slug                                             | Site.slug                                          |
| 200    | 次要标识符                                      | ProviderAccount.account, DeviceType.part_number    |
| 300    | 高度独特的描述性属性                            | CircuitTermination.xconnect_id, IPAddress.dns_name |
| 500    | 描述                                             | Site.description                                   |
| 1000   | 自定义字段默认值                               | -                                                  |
| 2000   | 其他离散属性                                   | CircuitTermination.port_speed                      |
| 5000   | 评论字段                                        | Site.comments                                      |

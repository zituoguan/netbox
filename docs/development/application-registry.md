# 应用程序注册表

注册表是一个内存数据结构，存储各种应用程序范围的参数，例如启用的插件列表。它不向用户公开，也不打算由NetBox核心之外的任何代码修改。

注册表基本上的行为类似于Python字典，有一个明显的异常，即一旦声明了存储（键），它就不能被删除或覆盖。但是，存储的值可以修改；例如，通过将值附加到列表中。存储值通常在应用程序初始化后不会更改。

可以通过从`extras.registry`导入`registry`来检查注册表。

## 存储

### `counter_fields`

一个将模型映射到与其关联的外键的字典，其中缓存的计数字段与之关联。

### `data_backends`

一个将数据后端类型映射到其相应类的字典。这些用于与[远程数据源](../models/core/datasource.md)交互。

### `denormalized_fields`

存储使用`netbox.denormalized.register()`进行的注册。对于每个模型，维护了一个相关模型和其字段映射的列表，以便进行自动更新。

### `model_features`

将特定功能（例如自定义字段）映射到支持它们的NetBox模型的字典，按应用程序排列。例如：

```python
{
    'custom_fields': {
        'circuits': ['provider', 'circuit'],
        'dcim': ['site', 'rack', 'devicetype', ...],
        ...
    },
    'event_rules': {
        'extras': ['configcontext', 'tag', ...],
        'dcim': ['site', 'rack', 'devicetype', ...],
    },
    ...
}
```

支持的模型功能在[功能矩阵](./models.md#features-matrix)中列出。

### `models`

此键列出了在NetBox中已注册但未指定为私有使用的所有模型。 （将`_netbox_private`设置为True的模型将其排除在此列表之外。）与`model_features`下的各个功能一样，模型是按应用程序标签组织的。

### `plugins`

此存储维护了所有已注册的插件项目，例如导航菜单、模板扩展等。

### `search`

将每个模型（通过其应用程序和标签标识）映射到其搜索索引类，如果为其注册了搜索索引类。

### `tables`

将表类映射到由插件使用`register_table_column()`实用函数注册的额外列列表。每个列被定义为名称和列实例的元组。

### `views`

每个模型的已注册视图的分层映射。可以使用`register_model_view()`装饰器添加映射，并可以使用`get_model_urls()`从中生成URL路径。

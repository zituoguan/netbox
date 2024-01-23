# 数据后端

[数据源](../../models/core/datasource.md) 可以定义为引用存在于 NetBox 之外的记录系统上的数据，例如 git 存储库或 Amazon S3 存储桶。插件可以注册自己的后端类来支持额外的资源类型。这可以通过继承 NetBox 的 `DataBackend` 类来完成。

```python title="data_backends.py"
from netbox.data_backends import DataBackend

class MyDataBackend(DataBackend):
    name = 'mybackend'
    label = 'My Backend'
    ...
```

要在 NetBox 中注册一个或多个数据后端，请在此文件的末尾定义一个名为 `backends` 的列表：

```python title="data_backends.py"
backends = [MyDataBackend]
```

!!! 提示
    可以通过在 PluginConfig 实例中设置 `data_backends` 来修改搜索索引列表的路径。

::: core.data_backends.DataBackend

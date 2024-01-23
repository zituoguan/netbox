# 搜索

插件可以定义和注册自己的模型来扩展NetBox的核心搜索功能。通常，插件将包含一个名为`search.py`的文件，其中包含其模型的所有搜索索引（请参阅下面的示例）。

```python
# search.py
from netbox.search import SearchIndex
from .models import MyModel

class MyModelIndex(SearchIndex):
    model = MyModel
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
    )
    display_attrs = ('site', 'device', 'status', 'description')
```

`display_attrs` 中列出的字段不会被缓存用于搜索，但将在全局搜索结果中与对象一起显示。这有助于向用户传达有关对象的其他信息。

要将一个或多个索引注册到NetBox，请在此文件末尾定义一个名为`indexes`的列表：

```python
indexes = [MyModelIndex]
```

!!! 提示
    可以通过在PluginConfig实例中设置`search_indexes`来修改搜索索引列表的路径。

::: netbox.search.SearchIndex

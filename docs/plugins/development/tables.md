# 表格

NetBox使用[`django-tables2`](https://django-tables2.readthedocs.io/)库来渲染动态对象表格。这些表格显示对象列表，并可以根据各种参数进行排序和过滤。

## NetBoxTable

为了提供比`django-tables2`中的默认`Table`类支持的功能更多的功能，NetBox提供了`NetBoxTable`类。这个自定义表格类支持以下功能：

* 用户可配置的列显示和排序
* 自定义字段和自定义链接列
* 相关对象的自动预取

它还包括一些默认列：

* `pk` - 用于选择与每个表格行相关联的对象的复选框（如果适用）
* `id` - 对象的数值数据库ID，作为指向对象视图的超链接（默认情况下隐藏）
* `actions` - 一个下拉菜单，向用户呈现可用于对象的特定操作

### 示例

```python
# tables.py
import django_tables2 as tables
from netbox.tables import NetBoxTable
from .models import MyModel

class MyModelTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    ...

    class Meta(NetBoxTable.Meta):
        model = MyModel
        fields = ('pk', 'id', 'name', ...)
        default_columns = ('pk', 'name', ...)
```

### 表格配置

NetBoxTable类具有动态配置功能，允许用户更改其列显示和排序首选项。要为特定请求配置表格，只需调用其`configure()`方法并传递当前的HTTPRequest对象。例如：

```python
table = MyModelTable(data=MyModel.objects.all())
table.configure(request)
```

这将自动应用表格的任何用户特定首选项。（如果使用NetBox提供的通用视图，表格配置将自动处理。）

## 列

下面列出的表格列类可用于插件。这些类可以从`netbox.tables.columns`导入。

::: netbox.tables.BooleanColumn
    options:
      members: false

::: netbox.tables.ChoiceFieldColumn
    options:
      members: false

::: netbox.tables.ColorColumn
    options:
      members: false

::: netbox.tables.ColoredLabelColumn
    options:
      members: false

::: netbox.tables.ContentTypeColumn
    options:
      members: false

::: netbox.tables.ContentTypesColumn
    options:
      members: false

::: netbox.tables.MarkdownColumn
    options:
      members: false

::: netbox.tables.TagColumn
    options:
      members: false

::: netbox.tables.TemplateColumn
    options:
      members:
        - __init__

## 扩展核心表格

!!! info "此功能在NetBox v3.7中引入。"

插件可以使用`register_table_column()`实用程序函数在核心表格上注册自己的自定义列。这允许插件附加额外的信息，例如与自己的模型的关系，到内置对象列表。

```python
import django_tables2
from django.utils.translation import gettext_lazy as _

from dcim.tables import SiteTable
from utilities.tables import register_table_column

mycol = django_tables2.Column(
    verbose_name=_('My Column'),
    accessor=django_tables2.A('description')
)

register_table_column(mycol, 'foo', SiteTable)
```

通常，在定义自定义列时，您会想要定义一个访问器，以识别所需的模型字段或关系。有关创建自定义列的更多信息，请参阅[django-tables2文档](https://django-tables2.readthedocs.io/)。

::: utilities.tables.register_table_column

# 表单

## 表单类

NetBox 为插件提供了几个基础表单类供使用。

| 表单类                 | 用途                                |
|-----------------------|-------------------------------------|
| `NetBoxModelForm`      | 创建/编辑单个对象                   |
| `NetBoxModelImportForm`| 从 CSV 数据批量导入对象              |
| `NetBoxModelBulkEditForm`| 同时编辑多个对象                   |
| `NetBoxModelFilterSetForm`| 在列表视图中过滤对象              |

### `NetBoxModelForm`

这是创建和编辑 NetBox 模型的基本表单。它扩展了 Django 的 ModelForm，以添加对标签和自定义字段的支持。

| 属性       | 描述                               |
|------------|------------------------------------|
| `fieldsets`| 一个定义表单布局的元组的两元组（可选）|

**示例**

```python
from dcim.models import Site
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import MyModel

class MyModelForm(NetBoxModelForm):
    site = DynamicModelChoiceField(
        queryset=Site.objects.all()
    )
    comments = CommentField()
    fieldsets = (
        ('Model Stuff', ('name', 'status', 'site', 'tags')),
        ('Tenancy', ('tenant_group', 'tenant')),
    )

    class Meta:
        model = MyModel
        fields = ('name', 'status', 'site', 'comments', 'tags')
```

!!! tip "Comment fields"
    如果您的表单具有 `comments` 字段，无需列出它；这将始终显示在页面的最后。

### `NetBoxModelImportForm`

此表单便于从 CSV、JSON 或 YAML 数据中批量导入新对象。与模型表单一样，您需要声明一个指定关联的 `model` 和 `fields` 的 `Meta` 子类。NetBox 还提供了适用于导入各种类型的 CSV 数据的几个表单字段，下面列出了这些字段。

**示例**

```python
from dcim.models import Site
from netbox.forms import NetBoxModelImportForm
from utilities.forms import CSVModelChoiceField
from .models import MyModel


class MyModelImportForm(NetBoxModelImportForm):
    site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name='name',
        help_text='Assigned site'
    )

    class Meta:
        model = MyModel
        fields = ('name', 'status', 'site', 'comments')
```

### `NetBoxModelBulkEditForm`

此表单便于批量编辑多个对象。与模型表单不同，此表单没有子 `Meta` 类，并且必须显式定义每个字段。批量编辑表单中的所有字段通常使用 `required=False` 声明。

| 属性             | 描述                                                    |
|-------------------|--------------------------------------------------------|
| `model`           | 正在编辑的对象的模型                                      |
| `fieldsets`       | 一个定义表单布局的元组的两元组（可选）                 |
| `nullable_fields` | 一个字段的元组，可以使用批量编辑表单将其置为空（可选）  |

**示例**

```python
from django import forms
from dcim.models import Site
from netbox.forms import NetBoxModelImportForm
from utilities.forms import CommentField, DynamicModelChoiceField
from .models import MyModel, MyModelStatusChoices


class MyModelEditForm(NetBoxModelImportForm):
    name = forms.CharField(
        required=False
    )
    status = forms.ChoiceField(
        choices=MyModelStatusChoices,
        required=False
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    comments = CommentField()

    model = MyModel
    fieldsets = (
        ('Model Stuff', ('name', 'status', 'site')),
    )
    nullable_fields = ('site', 'comments')
```

### `NetBoxModelFilterSetForm`

此表单类用于渲染专门用于过滤对象列表的表单。它的字段应与模型的过滤器集上定义的过滤器对应。

| 属性             | 描述                                         |
|-------------------|---------------------------------------------|
| `model`           | 正在编辑的对象的模型                           |
| `fieldsets`       | 一个定义表单布局的元组的两元组（可选）      |

**示例**

```

python
from dcim.models import Site
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms import DynamicModelMultipleChoiceField, MultipleChoiceField
from .models import MyModel, MyModelStatusChoices

class MyModelFilterForm(NetBoxModelFilterSetForm):
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    status = MultipleChoiceField(
        choices=MyModelStatusChoices,
        required=False
    )

    model = MyModel
```

## 通用字段

除了[Django 提供的表单字段](https://docs.djangoproject.com/en/stable/ref/forms/fields/)外，NetBox 还提供了几个字段类，用于在表单中处理特定类型的数据。这些可以从 `utilities.forms.fields` 中导入，下面对其进行了说明。

::: utilities.forms.fields.ColorField
    options:
      members: false

::: utilities.forms.fields.CommentField
    options:
      members: false

::: utilities.forms.fields.JSONField
    options:
      members: false

::: utilities.forms.fields.MACAddressField
    options:
      members: false

::: utilities.forms.fields.SlugField
    options:
      members: false

## 动态对象字段

::: utilities.forms.fields.DynamicModelChoiceField
    options:
      members: false

::: utilities.forms.fields.DynamicModelMultipleChoiceField
    options:
      members: false

## 内容类型字段

::: utilities.forms.fields.ContentTypeChoiceField
    options:
      members: false

::: utilities.forms.fields.ContentTypeMultipleChoiceField
    options:
      members: false

## CSV 导入字段

::: utilities.forms.fields.CSVChoiceField
    options:
      members: false

::: utilities.forms.fields.CSVMultipleChoiceField
    options:
      members: false

::: utilities.forms.fields.CSVModelChoiceField
    options:
      members: false

::: utilities.forms.fields.CSVContentTypeField
    options:
      members: false

::: utilities.forms.fields.CSVMultipleContentTypeField
    options:
      members: false

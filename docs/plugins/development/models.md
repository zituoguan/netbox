# 数据库模型

## 创建模型

如果您的插件在NetBox中引入了新类型的对象，您可能希望为其创建一个[Django模型](https://docs.djangoproject.com/en/stable/topics/db/models/)。模型本质上是数据库表的Python表示，具有表示各个列的属性。可以使用[查询](https://docs.djangoproject.com/en/stable/topics/db/queries/)创建、操作和删除模型的实例（对象）。模型必须在名为`models.py`的文件中定义。

以下是一个包含具有两个字符（文本）字段的模型的示例`models.py`文件：

```python
from django.db import models

class MyModel(models.Model):
    foo = models.CharField(max_length=50)
    bar = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.foo} {self.bar}'
```

每个模型默认包括一个数字主键。此值由数据库自动生成，并可以作为`pk`或`id`引用。

!!! 注意
    模型名称应遵循[PEP8](https://www.python.org/dev/peps/pep-0008/#class-names)标准，并且采用CapWords（没有下划线）。在模型名称中使用下划线将导致权限问题。

## 启用NetBox功能

插件模型可以通过继承NetBox的`NetBoxModel`类来利用某些NetBox功能。此类扩展了插件模型以启用NetBox独有的功能，包括：

* 书签
* 更改日志
* 克隆
* 自定义字段
* 自定义链接
* 自定义验证
* 导出模板
* 记录日志
* 标签
* Webhooks

此类执行两个关键功能：

1. 应用于这些功能的操作所需的任何字段、方法和/或属性
2. 注册模型，表示该模型使用了这些功能

只需在定义插件中的模型时将其子类化为`NetBoxModel`：

```python
# models.py
from django.db import models
from netbox.models import NetBoxModel

class MyModel(NetBoxModel):
    foo = models.CharField()
    ...
```

### NetBoxModel属性

#### `docs_url`

此属性指定可以访问此模型文档的URL。默认情况下，它将返回`/static/docs/models/<app_label>/<model_name>/`。插件模型可以覆盖此属性以返回自定义URL。例如，您可以将用户引导到托管在[ReadTheDocs](https://readthedocs.org/)上的插件文档。

#### `_netbox_private`

默认情况下，插件引入的任何模型都将出现在可用对象类型的列表中，例如在创建自定义字段或某些仪表板小部件时。如果模型仅用于“幕后使用”且不应向最终用户公开，则将`_netbox_private`设置为`True`。这将从通用对象类型列表中省略它。

### 单独启用功能

如果您更喜欢仅为插件模型启用这些功能的子集，NetBox为每个功能提供了单独的“混合”类。在定义模型时，可以单独为每个功能子类化它们。（您的模型还需要继承自Django内置的`Model`类。）

例如，如果我们只想支持标签和导出模板，我们可以从NetBox的`ExportTemplatesMixin`和`TagsMixin`类中继承，并从Django的`Model`类中继承（继承所有可用的混合类基本上与子类化`NetBoxModel`相同）。

```python
# models.py
from django.db import models
from netbox.models.features import ExportTemplatesMixin, TagsMixin

class MyModel(ExportTemplatesMixin, TagsMixin, models.Model):
    foo = models.CharField()
    ...
```

## 数据库迁移

一旦您完成了为插件定义模型，就需要创建数据库模式迁移。迁移文件本质上是一组用于操作PostgreSQL数据库以支持新模型或更改现有模型的指令。通常可以使用Django的`makemigrations`管理命令自动创建迁移。（确保首先安装和启用了您的插件，否则找不到它。）

!!! 注意 启用开发者模式
    NetBox在`makemigrations`命令周围执行了一项保护措施，以防止普通用户意外创建错误的模式迁移。为了在插件开发中启用此命令，请在`configuration.py`中设置`DEVELOPER=True`。

```no-highlight
$ ./manage.py makemigrations my_plugin 
Migrations for 'my_plugin':
  /home/jstretch/animal_sounds/my_plugin/migrations/0001_initial.py
    - Create model MyModel
```

接下来，我们可以使用`migrate`命令将迁移应用于数据库：

```no-highlight
$ ./manage.py migrate my_plugin
Operations to perform:
  Apply all migrations: my_plugin
Running migrations:
  Applying my_plugin.0001_initial... OK
```

有关数据库迁移的更多信息，请参阅[Django文档](https://docs.djangoproject.com/en/stable/topics/migrations/)。

## 功能混合参考

!!! 警告
    请注意，目前仅支持出现在此文档中的类。虽然“features”模块中可能存在其他类，但它们尚不支持供插件使用。

::: netbox.models.features.BookmarksMixin

::: netbox.models.features.ChangeLoggingMixin

::: netbox.models.features.CloningMixin

::: netbox.models.features.CustomLinksMixin

::: netbox.models.features.CustomFieldsMixin

::: netbox.models.features.CustomValidationMixin

::: netbox.models.features.EventRulesMixin

!!! 注意
    `EventRulesMixin`在NetBox v3.7中从`WebhooksMixin`中更名而来。

::: netbox.models.features.ExportTemplatesMixin

::: netbox.models.features.JournalingMixin

::: netbox.models.features.TagsMixin

## 选择集

对于支持从预定义选择列表中选择一个或多个值的模型字段，NetBox提供了`ChoiceSet`实用类。这可以用来替代常规的选择元组，以提供增强功能，即动态配置和着色。（有关受支持的模型字段的`choices`参数，请参阅[Django文档](https://docs.djangoproject.com/en/stable/ref/models/fields/#choices)。）

要为模型字段定义选择项，请子类化`ChoiceSet`并定义一个名为`CHOICES`的元组，其中每个成员都是一个两个或三个元组。这些元素是：

* 数据库值
* 相应的用户友好标签
* 分配的颜色（可选）

下面提供了一个完整示例。

!!! 注意
    作者可能会发现有用的是将每个数据库值声明为类上的常量，并在`CHOICES`成员内引用它们。这种约定允许从类外部引用这些值，但不是强制性的。

### 动态配置

NetBox中的某些模型字段选择可以由管理员配置。例如，Site模型的`status`字段的默认值可以被替换或补充为自定义选择。要为ChoiceSet子类启用动态配置，请将其`key`定义为字符串，指定其适用的模型和字段名称。例如：

```python
from utilities.choices import ChoiceSet

class StatusChoices(ChoiceSet):
    key = 'MyModel.status'
```

要扩展或替换此选择集的默认值，NetBox管理员可以在[`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices)配置参数下引用它。例如，`my_plugin`中的`MyModel`上的`status`字段将被引用为：

```python
FIELD_CHOICES = {
    'my_plugin.MyModel.status': (
        # 自定义选择
    )
}
```

### 示例

```python
# choices.py
from utilities.choices import ChoiceSet

class StatusChoices(ChoiceSet):
    key = 'MyModel.status'

    STATUS_FOO = 'foo'
    STATUS_BAR = 'bar'
    STATUS_BAZ = 'baz'

    CHOICES = [
        (STATUS_FOO, 'Foo', 'red'),
        (STATUS_BAR, 'Bar', 'green'),
        (STATUS_BAZ, 'Baz', 'blue'),
    ]
```

!!! 警告
    为了使动态配置正常工作，`CHOICES`必须是可变列表，而不是元组。

```python
# models.py
from django.db import models
from .choices import StatusChoices

class MyModel(models.Model):
    status = models.CharField(
        max_length=50,
        choices=StatusChoices,
        default=StatusChoices.STATUS_FOO
    )
```

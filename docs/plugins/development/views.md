# 视图

## 编写视图

如果您的插件将在NetBox Web界面中提供自己的页面或页面，您需要定义视图。视图是一段业务逻辑，当对特定URL发出请求时，它执行操作和/或呈现页面。HTML内容是使用[模板](./templates.md)呈现的。视图通常在`views.py`中定义，URL模式在`urls.py`中定义。

例如，让我们编写一个视图，该视图显示一个随机动物和它发出的声音。我们将使用Django的通用`View`类来最小化需要的样板代码量。

```python
from django.shortcuts import render
from django.views.generic import View
from .models import Animal

class RandomAnimalView(View):
    """
    Display a randomly-selected animal.
    """
    def get(self, request):
        animal = Animal.objects.order_by('?').first()
        return render(request, 'netbox_animal_sounds/animal.html', {
            'animal': animal,
        })
```

这个视图从数据库中检索一个随机的Animal实例，并在呈现名为`animal.html`的模板时将其作为上下文变量传递。HTTP `GET`请求由视图的`get()`方法处理，`POST`请求由其`post()`方法处理。

我们上面的示例非常简单，但视图可以做几乎任何事情。通常情况下，您的插件的核心功能将驻留在视图中。视图也不仅限于返回HTML内容：视图可以返回CSV文件或图像，例如。有关视图的更多信息，请参阅[Django文档](https://docs.djangoproject.com/en/stable/topics/class-based-views/)。

### URL注册

要使视图对用户可访问，我们需要在`urls.py`中注册一个URL。我们通过定义包含路径列表的`urlpatterns`变量来实现这一点。

```python
from django.urls import path
from . import views

urlpatterns = [
    path('random/', views.RandomAnimalView.as_view(), name='random_animal'),
]
```

URL模式有三个组成部分：

* `route` - 专用于此视图的唯一URL部分
* `view` - 视图本身
* `name` - 用于在内部识别URL路径的短名称

这使我们的视图可在URL `/plugins/animal-sounds/random/`上访问。 （请记住，我们的`AnimalSoundsConfig`类将插件的基本URL设置为`animal-sounds`。）访问此URL应该显示具有我们自定义内容的基本NetBox模板。

### 视图类

NetBox提供了几个通用视图类（下面的文档中有详细说明），用于执行常见操作，例如创建、查看、修改和删除对象。插件可以子类化这些视图以供其自己使用。

| 视图类            | 描述                        |
|-------------------|----------------------------|
| `ObjectView`      | 查看单个对象                |
| `ObjectEditView`  | 创建或编辑单个对象          |
| `ObjectDeleteView`| 删除单个对象                |
| `ObjectChildrenView` | 父对象上下文中的子对象列表 |
| `ObjectListView`  | 查看对象列表                |
| `BulkImportView`  | 导入一组新对象              |
| `BulkEditView`    | 同时编辑多个对象            |
| `BulkDeleteView`  | 同时删除多个对象            |

!!! warning
    请注意，目前仅支持此文档中出现的类。虽然`views.generic`模块中可能存在其他类，但它们尚不支持供插件使用。

#### 示例用法

```python
# views.py
from netbox.views.generic import ObjectEditView
from .models import Thing

class ThingEditView(ObjectEditView):
    queryset = Thing.objects.all()
    template_name = 'myplugin/thing.html'
    ...
```
## 对象视图

以下是NetBox对象视图的类定义。这些视图处理单个对象的CRUD操作。视图、添加/编辑和删除视图都继承自`BaseObjectView`，不打算直接使用它。

::: netbox.views.generic.base.BaseObjectView
    options:
      members:
        - get_queryset
        - get_object
        - get_extra_context

::: netbox.views.generic.ObjectView
    options:
      members:
        - get_template_name

::: netbox.views.generic.ObjectEditView
    options:
      members:
        - alter_object

::: netbox.views.generic.ObjectDeleteView
    options:
      members: false

::: netbox.views.generic.ObjectChildrenView
    options:
      members:
        - get_children
        - prep_table_data

## 多对象视图

以下是NetBox的多对象视图的类定义。这些视图处理一组对象的同时操作。列表、导入、编辑和删除视图都继承自`BaseMultiObjectView`，不打算直接使用它。

::: netbox.views.generic.base.BaseMultiObjectView
    options:
      members:
        - get_queryset
        - get_extra_context

::: netbox.views.generic.ObjectListView
    options:
      members:
        - get_table
        - export_table
        - export_template

::: netbox.views.generic.BulkImportView
    options:
      members:
        - save_object

::: netbox.views.generic.BulkEditView
    options:
      members: false

::: netbox.views.generic.BulkDeleteView
    options:
      members:
        - get_form

## 功能视图

提供这些视图以启用或增强NetBox模型功能，例如更改日志记录或日志记录。通常不需要对其进行子类化：它们可以直接使用，例如在URL路径中使用。

::: netbox.views.generic.ObjectChangeLogView
    options:
      members:
        - get_form

::: netbox.views.generic.ObjectJournalView
    options:
      members:
        - get_form

## 扩展核心视图

### 额外的选项卡

插件可以通过使用`register_model_view()`将自定义视图注册到核心NetBox模型中，以将其"附加"到核心NetBox模型。要在NetBox UI中包含此视图的选项卡，请声明一个名为`tab`的TabView实例：

```python
from dcim.models import Site
from myplugin.models import Stuff
from netbox.views import generic
from utilities.views import ViewTab, register_model_view

@register_model_view(Site, name='myview', path='some-other-stuff')
class MyView(generic.ObjectView):
    ...
    tab = ViewTab(
        label='Other Stuff',
        badge=lambda obj: Stuff.objects.filter(site=obj).count(),
        permission='myplugin.view_stuff'
    )
```

::: utilities.views.register_model_view

::: utilities.views.ViewTab

### 额外的模板内容

插件可以将自定义内容注入到核心NetBox视图的某些区域。这是通过子类化`PluginTemplateExtension`、指定特定的NetBox模型，并定义要呈现自定义内容的所需方法来实现的。有五种方法可用：

| 方法              | 视图        | 描述                                   |
|-------------------|-------------|----------------------------------------|
| `left_page()`     | 对象视图    | 注入页面左侧的内容                    |
| `right_page()`    | 对象视图    | 注入页面右侧的内容                    |
| `full_width_page()`| 对象视图   | 注入整个页面底部的内容                |
| `buttons()`       | 对象视图    | 在页面顶部添加按钮                    |
| `list_buttons()`  | 列表视图    | 在页面顶部添加按钮                    |

此外，还提供了一个`render()`方法，以方便起见。此方法接受要呈现的模板名称以及要传递的任何其他上下文数据。它的使用是可选的。

当实例化PluginTemplateExtension时，上下文数据分配给`self.context`。可用数据包括：

* `object` - 正在查看的对象（仅限对象视图）
* `model` - 列表视图的模型（仅限列表视图）
* `request` - 当前请求
* `settings` - 全局NetBox设置
* `config` - 插件特定的配置参数

例如，在模板中访问`{{ request.user }}`将返回当前用户。

声明的子类应该被收集到一个列表或元组中，以与NetBox集成。默认情况下，NetBox在`template_content.py`文件中查找名为`template_extensions`的可迭代对象。 （这可以通过在插件的PluginConfig上设置`template_extensions`为自定义值来覆盖。）以下是一个示例。

```python
from netbox.plugins import PluginTemplateExtension
from .models import Animal

class SiteAnimalCount(PluginTemplateExtension):
    model = 'dcim.site'

    def right_page(self):
        return self.render('netbox_animal_sounds/inc/animal_count.html', extra_context={
            'animal_count': Animal.objects.count(),
        })

template_extensions = [SiteAnimalCount]
```

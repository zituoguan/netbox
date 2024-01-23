# 过滤器和过滤器集

过滤器集定义了在 NetBox 中过滤或搜索一组对象的可用机制。例如，可以通过其父区域或组、状态、设施 ID 等来过滤站点。无论是通过 UI、REST API 还是 GraphQL API 进行请求，都将一致使用相同的模型来定义过滤器集。NetBox 使用 [django-filters2](https://django-tables2.readthedocs.io/en/latest/) 库来定义过滤器集。

## 过滤器集类

为了支持 NetBox 模型标准的附加功能，例如标签分配和自定义字段支持，可以使用 `NetBoxModelFilterSet` 类供插件使用。这应该用作从 `NetBoxModel` 继承的插件模型的基础过滤器集类。在此类中，可以根据 `django-filters` 文档的指导声明单独的过滤器。下面提供了一个示例。

```python
# filtersets.py
import django_filters
from netbox.filtersets import NetBoxModelFilterSet
from .models import MyModel

class MyFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=(
            ('foo', 'Foo'),
            ('bar', 'Bar'),
            ('baz', 'Baz'),
        ),
        null_value=None
    )

    class Meta:
        model = MyModel
        fields = ('some', 'other', 'fields')
```

### 声明过滤器集

要在 NetBox 的通用视图子类中使用过滤器集（例如 `ObjectListView` 或 `BulkEditView`），请在视图类上定义 `filterset` 属性：

```python
# views.py
from netbox.views.generic import ObjectListView
from .filtersets import MyModelFilterSet
from .models import MyModel

class MyModelListView(ObjectListView):
    queryset = MyModel.objects.all()
    filterset = MyModelFilterSet
```

要在 REST API 端点上启用过滤器集，请在 API 视图上设置 `filterset_class` 属性：

```python
# api/views.py
from myplugin import models, filtersets
from . import serializers

class MyModelViewSet(...):
    queryset = models.MyModel.objects.all()
    serializer_class = serializers.MyModelSerializer
    filterset_class = filtersets.MyModelFilterSet
```

## 过滤器类

### TagFilter

`TagFilter` 类适用于支持标签分配的所有模型（那些从 `NetBoxModel` 或 `TagsMixin` 继承的模型）。此过滤器子类 django-filter 的 `ModelMultipleChoiceFilter` 以与 NetBox 的 `TaggedItem` 类一起使用。

```python
from django_filters import FilterSet
from extras.filters import TagFilter

class MyModelFilterSet(FilterSet):
    tag = TagFilter()
```

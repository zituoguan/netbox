# REST API

插件可以在NetBox的REST API上声明自定义端点，以检索或操作模型或其他数据。这些行为与视图非常相似，但不是使用模板渲染任意内容，而是使用序列化器以JSON格式返回数据。

一般来说，要在插件中实现REST API功能，并没有太多特定于NetBox的组件。NetBox使用[Django REST Framework](https://www.django-rest-framework.org/)（DRF）来实现其REST API，插件作者将发现他们可以在插件的实现中复制NetBox中找到的相同模式。这里包含了一些简要的示例供参考。

## 代码布局

推荐的方法是将API序列化器、视图和URL分别放在`api/`目录下的不同模块中，以保持整洁，特别是对于较大的项目。位于`api/__init__.py`的文件可以从每个子模块中导入相关组件，以允许在其他地方直接导入所有API组件。然而，这只是一种约定，不是严格要求。

```no-highlight
project-name/
  - plugin_name/
    - api/
      - __init__.py
      - serializers.py
      - urls.py
      - views.py
    ...
```

## 序列化器

### 模型序列化器

序列化器负责将Python对象转换为适合传递给消费者的JSON数据，反之亦然。NetBox为插件提供了`NetBoxModelSerializer`类，用于处理标签和自定义字段数据的分配。（这些功能也可以通过`CustomFieldModelSerializer`和`TaggableModelSerializer`类逐个包含。）

#### 示例

要为插件模型创建序列化器，请在`api/serializers.py`中继承`NetBoxModelSerializer`。在序列化器的`Meta`类中指定模型类和要包含在其中的字段是一般建议。通常建议在每个序列化器上包含一个`url`属性，这将呈现访问正在呈现的对象的直接链接。

```python
# api/serializers.py
from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from my_plugin.models import MyModel

class MyModelSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:myplugin-api:mymodel-detail'
    )

    class Meta:
        model = MyModel
        fields = ('id', 'foo', 'bar', 'baz')
```

### 嵌套序列化器

通常有两种情况下，显示对象的最小表示通常是可取的：

1. 显示与正在查看的对象相关的对象（例如，站点分配给站点的区域）
2. 使用“简要”模式列出许多对象

为了适应这些情况，建议为每个模型的“完整”序列化器创建嵌套序列化器。NetBox提供了`WritableNestedSerializer`类，专门用于此目的。该类在写入时接受主键值，但在读取请求时显示对象表示。它还包括一个只读的`display`属性，传递对象的字符串表示。

#### 示例

```python
# api/serializers.py
from rest_framework import serializers
from netbox.api.serializers import WritableNestedSerializer
from my_plugin.models import MyModel

class NestedMyModelSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:myplugin-api:mymodel-detail'
    )

    class Meta:
        model = MyModel
        fields = ('id', 'display', 'foo')
```

## 视图集

与用户界面一样，REST API视图负责处理显示和与NetBox对象交互的业务逻辑。NetBox提供了`NetBoxModelViewSet`类，它扩展了DRF内置的`ModelViewSet`以处理批量操作和对象验证。

与用户界面不同，通常只需要每个模型一个视图集：此视图集处理所有请求类型（`GET`、`POST`、`DELETE`等）。

### 示例

要为插件模型创建视图集，请在`api/views.py`中继承`NetBoxModelViewSet`，并定义`queryset`和`serializer_class`属性。

```python
# api/views.py
from netbox.api.viewsets import ModelViewSet
from my_plugin.models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
```

## 路由器

路由器将URL映射到REST API视图（端点）。NetBox没有为此提供任何自定义组件；DRF提供的[`DefaultRouter`](https://www.django-rest-framework.org/api-guide/routers/#defaultrouter)类应足够满足大多数用例。

路由器应在`api/urls.py`中公开。此文件**必须**定义一个名为`urlpatterns`的变量。

### 示例

```python
# api/urls.py
from netbox.api.routers import NetBoxRouter
from .views import MyModelViewSet

router = NetBoxRouter()
router.register('my-model', MyModelViewSet)
urlpatterns = router.urls
```

这将使插件的视图在`/api/plugins/my-plugin/my-model/`上可访问。

!!! 警告
    这里提供的示例仅用作最小参考实现。本文档不涵盖插件作者可能需要解决的身份验证、性能或其他问题。

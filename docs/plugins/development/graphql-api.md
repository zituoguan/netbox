# GraphQL API

## 定义模式类

插件可以通过注册自己的模式类来扩展 NetBox 的 GraphQL API。默认情况下，NetBox 将尝试从插件中导入 `graphql.schema`，如果存在的话。可以通过在 PluginConfig 实例上定义 `graphql_schema`，将其覆盖为所需 Python 类的点路径。该类必须是 `graphene.ObjectType` 的子类。

### 示例

```python
# graphql.py
import graphene
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import filtersets, models

class MyModelType(NetBoxObjectType):

    class Meta:
        model = models.MyModel
        fields = '__all__'
        filterset_class = filtersets.MyModelFilterSet

class MyQuery(graphene.ObjectType):
    mymodel = ObjectField(MyModelType)
    mymodel_list = ObjectListField(MyModelType)

schema = MyQuery
```

## GraphQL 对象

NetBox 提供了两个用于插件的对象类型类。

::: netbox.graphql.types.BaseObjectType
    options:
      members: false

::: netbox.graphql.types.NetBoxObjectType
    options:
      members: false

## GraphQL 字段

NetBox 提供了两个用于插件的字段类。

::: netbox.graphql.fields.ObjectField
    options:
      members: false

::: netbox.graphql.fields.ObjectListField
    options:
      members: false

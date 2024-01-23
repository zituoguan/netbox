# 添加模型

## 1. 定义模型类

每个应用程序中的模型都存储在`models.py`或在`models/`目录下的子模块中。创建模型时，请确保将其子类化为`netbox.models`中的[适当基本模型](models.md)。通常情况下，这将是NetBoxModel或OrganizationalModel。记得将模型类添加到模块的`__all__`列表中。

每个模型应该至少定义：

* 一个`Meta`类，指定确定性排序（如果按除主要ID之外的字段排序）
* 一个`__str__()`方法，返回实例的用户友好的字符串表示
* 一个`get_absolute_url()`方法，返回实例的直接URL（使用`reverse()`）

## 2. 定义字段选择项

如果模型具有一个或多个带有静态选择的字段，请在`choices.py`中定义这些选择项，通过子类化`utilities.choices.ChoiceSet`。

## 3. 生成数据库迁移

一旦模型定义完成，通过运行`manage.py makemigrations -n $NAME --no-header`来生成数据库迁移。始终在生成迁移时指定一个短的唯一名称。

!!! 信息 "需要配置"
    在您的NetBox配置中设置`DEVELOPER = True`以启用新迁移的创建。

## 4. 添加所有标准视图

大多数模型将需要在`views.py`中创建视图类，以提供以下操作：

* 列表视图
* 详细视图
* 编辑视图
* 删除视图
* 批量导入
* 批量编辑
* 批量删除

## 5. 添加URL路径

为前一步创建的每个视图添加相关的URL路径到`urls.py`中。

## 6. 添加相关表单

根据要添加的模型类型，您可能需要定义几种类型的表单类。这些包括：

* 基本模型表单（用于创建/编辑单个对象）
* 批量编辑表单
* 批量导入表单（用于基于CSV的导入）
* 过滤器集表单（用于过滤对象列表视图）

## 7. 创建FilterSet

每个模型应该有一个对应的FilterSet类定义。这用于过滤UI和API查询。子类化`netbox.filtersets`中与模型的父类匹配的适当类。

## 8. 创建表格类

通过子类化`utilities.tables.BaseTable`在`tables.py`中为模型创建一个表格类。在表的`Meta`类下，确保列出字段和默认列。

## 9. 创建SearchIndex子类

如果此模型将包含在全局搜索结果中，请为其创建`netbox.search.SearchIndex`的子类，并指定要进行索引的字段。

## 10. 创建对象模板

为对象视图创建HTML模板。 （其他视图通常使用通用模板。）此模板应扩展`generic/object.html`。

## 11. 将模型添加到导航菜单

在`netbox/netbox/navigation/menu.py`中添加相关的导航菜单项。

## 12. REST API组件

为每个模型创建以下内容：

* `api/serializers.py`中的详细（完整）模型序列化程序
* `api/nested_serializers.py`中的嵌套序列化程序
* `api/views.py`中的API视图
* `api/urls.py`中的端点路由

## 13. GraphQL API组件

通过子类化`netbox.graphql.types`中的适当类为模型在`graphql/types.py`中创建一个Graphene对象类型。

还要根据已建立的约定扩展`graphql/schema.py`中定义的模式类，使用单独的对象和对象列表字段。

## 14. 添加测试

为以下内容添加测试：

* UI视图
* API视图
* 过滤器集

## 15. 文档

在`docs/models/<app_label>/<model_name>.md`中为模型创建新的文档页面。在适当的位置在“features”文档下包括此文件。

还要将模型添加到`docs/development/models.md`中的索引中。

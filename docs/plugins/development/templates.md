# 模版

模板用于渲染从一组上下文数据生成的HTML内容。NetBox提供了一组适用于插件视图的内置模板。插件作者可以扩展这些模板，以最小化创建自定义模板所需的工作量，同时确保它们生成的内容与NetBox的布局和样式匹配。这些模板都是用[Django模板语言（DTL）](https://docs.djangoproject.com/en/stable/ref/templates/language/)编写的。

## 模板文件结构

插件模板应位于插件根目录下的`templates/<plugin-name>/`路径中。例如，如果您的插件的名称是`my_plugin`并且您创建了一个名为`foo.html`的模板，它应该保存在`templates/my_plugin/foo.html`中。 （当然，您也可以在此点下使用子目录。）这确保了Django的模板引擎可以定位要渲染的模板。

## 标准块

以下模板块在所有模板上都可用。

| 名称         | 必需   | 描述               |
|--------------|--------|--------------------|
| `title`      | 是     | 页面标题           |
| `content`    | 是     | 页面内容           |
| `head`       | -      | 包含在HTML `<head>`元素中的内容 |
| `footer`     | -      | 页脚内容           |
| `footer_links` | -   | 页脚的链接部分     |
| `javascript` | -    | 包含在HTML `<body>`元素末尾的Javascript内容 |

!!! note
    有关模板块的工作原理的更多信息，请查阅[Django文档](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#block)。

## 基础模板

### layout.html

路径：`base/layout.html`

NetBox提供了一个基本模板，以确保一致的用户体验，插件可以在其中扩展其自己的内容。这是一个通用模板，当下面列出的功能特定模板都不适用时，可以使用它。

#### 块

| 名称      | 必需 | 描述           |
|-----------|------|--------------|
| `header`  | -    | 页面头部     |
| `tabs`    | -    | 水平导航选项卡 |
| `modals`  | -    | Bootstrap 5模态元素 |

#### 示例

下面包含一个扩展`layout.html`的插件模板的示例。

```jinja2
{% extends 'base/layout.html' %}

{% block header %}
  <h1>我的自定义标题</h1>
{% endblock header %}

{% block content %}
  <p>{{ some_plugin_context_var }}</p>
{% endblock content %}
```

模板的第一行指示Django扩展NetBox基本模板，并且`block`部分将我们的自定义内容注入其中的`header`和`content`块中。

!!! note
    Django使用其自己的自定义[模板语言](https://docs.djangoproject.com/en/stable/topics/templates/#the-django-template-language)来呈现模板。这与Jinja2非常相似，但在创建新模板之前，作者需要了解一些重要的区别。在尝试创建新模板之前，请务必熟悉Django的模板语言。

## 通用视图模板

### object.html

路径：`generic/object.html`

此模板由`ObjectView`通用视图使用，用于显示单个对象。

#### 块

| 名称                | 必需 | 描述                                |
|---------------------|------|------------------------------------|
| `breadcrumbs`       | -    | 面包屑列表项（HTML `<li>`元素） |
| `object_identifier` | -    | 对象的唯一标识符（字符串）         |
| `extra_controls`    | -    | 要显示的其他操作按钮               |

#### 上下文

| 名称     | 必需 | 描述           |
|----------|------|--------------|
| `object` | 是   | 正在查看的对象实例 |

### object_edit.html

路径：`generic/object_edit.html`

此模板由`ObjectEditView`通用视图使用，用于创建或修改单个对象。

#### 块

| 名称             | 必需 | 描述                                                        |
|------------------|------|------------------------------------------------------------|
| `form`           | -    | 自定义表单内容（在HTML `<form>`元素内部                 |
| `buttons`        | -    | 表单提交按钮                                              |

#### 上下文

| 名称         | 必需 | 描述                                   |
|--------------|------|---------------------------------------|
| `object`     | 是   | 正在修改的对象实例（或无，如果正在创建） |
| `form`       | 是   | 用于创建/修改对象的表单类                |
| `return_url` | 是   | 用户在提交表单后重定向的URL             |

### object_delete.html

路径：`generic/object_delete.html`

此模板由`ObjectDeleteView`通用视图使用，用于删除单个对象。

#### 块

无

#### 上下文

| 名称         | 必需 | 描述                                   |
|--------------|------|---------------------------------------|
| `object`     | 是   | 正在删除的对象实例                    |
| `form`       | 是   | 用于确认对象删除的表单类              |
| `return_url` | 是   | 用户在提交表单后重定向的URL             |

### object_list.html

路径：`generic/object_list.html`

此模板由`ObjectListView`通用视图使用，用于显示多个对象的可过滤列表。

#### 块

| 名称             | 必需 | 描述                                   |
|------------------|------|---------------------------------------|
| `extra_controls` | -    | 其他操作按钮                           |
| `bulk_buttons`   | -    | 要在对象列表下方显示的其他批量操作按钮 |

#### 上下文

| 名称          | 必需 | 描述                                                                                 |
|---------------|------|-------------------------------------------------------------------------------------

|
| `model`       | 是   | 对象类                                                                              |
| `table`       | 是   | 用于呈现对象列表的表格类                                                              |
| `permissions` | 是   | 当前用户的添加、修改和删除权限的映射                                                 |
| `actions`     | 是   | 要显示的按钮列表（`add`、`import`、`export`、`bulk_edit`和/或`bulk_delete`）          |
| `filter_form` | -    | 用于过滤对象列表的绑定过滤器表单                                                      |
| `return_url`  | -    | 在提交批量操作表单时传递的返回URL                                                     |

### bulk_import.html

路径：`generic/bulk_import.html`

此模板由`BulkImportView`通用视图使用，用于一次性从CSV数据导入多个对象。

#### 块

无

#### 上下文

| 名称         | 必需 | 描述                                                  |
|--------------|------|------------------------------------------------------|
| `model`      | 是   | 对象类                                               |
| `form`       | 是   | CSV导入表单类                                        |
| `return_url` | -    | 在提交批量操作表单时传递的返回URL                    |
| `fields`     | -    | 表单字段的字典，用于显示导入选项                     |

### bulk_edit.html

路径：`generic/bulk_edit.html`

此模板由`BulkEditView`通用视图使用，用于同时修改多个对象。

#### 块

无

#### 上下文

| 名称         | 必需 | 描述                                            |
|--------------|------|------------------------------------------------|
| `model`      | 是   | 对象类                                         |
| `form`       | 是   | 批量编辑表单类                                 |
| `table`      | 是   | 用于呈现对象列表的表格类                         |
| `return_url` | 是   | 用户在提交表单后重定向的URL                    |

### bulk_delete.html

路径：`generic/bulk_delete.html`

此模板由`BulkDeleteView`通用视图使用，用于同时删除多个对象。

#### 块

| 名称            | 必需 | 描述                             |
|-----------------|------|---------------------------------|
| `message_extra` | -    | 附加警告消息内容               |

#### 上下文

| 名称         | 必需 | 描述                                            |
|--------------|------|------------------------------------------------|
| `model`      | 是   | 对象类                                         |
| `form`       | 是   | 批量删除表单类                                 |
| `table`      | 是   | 用于呈现对象列表的表格类                         |
| `return_url` | 是   | 用户在提交表单后重定向的URL                    |

## 标签

以下自定义模板标签在NetBox中可用。

!!! info
    这些标签会由模板后端自动加载：您无需在模板中包含`{% load %}`标签以激活它们。

::: utilities.templatetags.builtins.tags.badge

::: utilities.templatetags.builtins.tags.checkmark

::: utilities.templatetags.builtins.tags.customfield_value

::: utilities.templatetags.builtins.tags.tag

## 过滤器

以下自定义模板过滤器在NetBox中可用。

!!! info
    这些过滤器会由模板后端自动加载：您无需在模板中包含`{% load %}`标签以激活它们。

::: utilities.templatetags.builtins.filters.bettertitle

::: utilities.templatetags.builtins.filters.content_type

::: utilities.templatetags.builtins.filters.content_type_id

::: utilities.templatetags.builtins.filters.linkify

::: utilities.templatetags.builtins.filters.meta

::: utilities.templatetags.builtins.filters.placeholder

::: utilities.templatetags.builtins.filters.render_json

::: utilities.templatetags.builtins.filters.render_markdown

::: utilities.templatetags.builtins.filters.render_yaml

::: utilities.templatetags.builtins.filters.split

::: utilities.templatetags.builtins.filters.tzoffset

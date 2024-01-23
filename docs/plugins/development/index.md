# 插件开发

!!! tip "插件开发教程"
    刚开始使用插件？请查看我们的[**NetBox插件开发教程**](https://github.com/netbox-community/netbox-plugin-tutorial)！这个详细的指南将逐步引导您从零开始创建一个完整的插件。它甚至包括一个[演示插件仓库](https://github.com/netbox-community/netbox-plugin-demo)，以确保您可以在任何时候加入。这将让您迅速掌握插件的开发！

通过使用插件，NetBox可以扩展以支持额外的数据模型和功能。插件本质上是一个独立的[Django应用程序](https://docs.djangoproject.com/en/stable/)，它与NetBox一起安装以提供自定义功能。在单个NetBox实例中可以安装多个插件，并且每个插件可以独立启用和配置。

!!! info "Django开发"
    Django是NetBox构建的Python框架。由于Django本身有很好的文档，因此本文档仅涵盖与NetBox插件开发唯一相关的方面。

插件可以实现多种功能，包括：

* 创建Django模型以将数据存储在数据库中
* 在Web用户界面中提供自己的“页面”（视图）
* 注入模板内容和导航链接
* 扩展NetBox的REST和GraphQL API
* 加载额外的Django应用程序
* 添加自定义请求/响应中间件

但是，请注意，每个功能都是可选的。例如，如果您的插件仅添加了一个中间件或一个现有数据的API端点，那么不需要定义任何新模型。

!!! warning
    尽管功能强大，但NetBox插件API在其范围内受到限制。插件API在这里完全讨论：NetBox代码库中未在此处记录的任何部分都不是支持的插件API的一部分，不应该被插件使用。NetBox内部元素随时都可能发生变化，而无需警告。强烈建议插件作者仅使用此处正式支持的组件以及由底层Django框架提供的组件来开发插件，以避免未来版本中的破坏性更改。

## 插件结构

尽管插件的具体结构基本上由其作者自行决定，但一个典型的NetBox插件可能如下所示：

```no-highlight
project-name/
  - plugin_name/
    - api/
      - __init__.py
      - serializers.py
      - urls.py
      - views.py
    - migrations/
      - __init__.py
      - 0001_initial.py
      - ...
    - templates/
      - plugin_name/
        - *.html
    - __init__.py
    - filtersets.py
    - graphql.py
    - models.py
    - middleware.py
    - navigation.py
    - signals.py
    - tables.py
    - template_content.py
    - urls.py
    - views.py
  - README.md
  - setup.py
```

顶级目录是项目根目录，可以具有您喜欢的任何名称。根目录中应该立即存在以下几个项目：

* `setup.py` - 这是用于在Python环境中安装插件包的标准安装脚本。
* `README.md` - 对插件的简要介绍，如何安装和配置它，何处寻求帮助以及任何其他相关信息。建议使用诸如Markdown之类的标记语言编写`README`文件，以便以人类友好的方式显示。
* 插件源目录。这必须是有效的Python包名称，通常仅包含小写字母、数字和下划线。

插件源目录包含实际Python代码和其他插件使用的资源。其结构由作者自行决定，但建议按照[ Django文档](https://docs.djangoproject.com/en/stable/intro/reusable-apps/)中概述的最佳实践进行。至少，此目录**必须**包含包含NetBox的`PluginConfig`类实例的`__init__.py`文件，如下所示。

## PluginConfig

`PluginConfig`类是NetBox的`AppConfig`类的一个NetBox特定包装器。它用于在Python包中声明NetBox插件功能。每个插件应该提供其自己的子类，定义其名称、元数据以及默认和必需的配置参数。下面是一个示例：

```python
from netbox.plugins import PluginConfig

class FooBarConfig(PluginConfig):
    name = 'foo_bar'
    verbose_name = 'Foo Bar'
    description = 'An example NetBox plugin'
    version = '0.1'
    author = 'Jeremy Stretch'
    author_email = 'author@example.com'
    base_url = 'foo-bar'
    required_settings = []
    default_settings = {
        'baz': True
    }
    django_apps = ["foo", "bar", "baz"]

config = FooBarConfig
```

NetBox会查找插件的`__init__.py`中的`config`变量以加载其配置。通常，这将设置为PluginConfig子类，但您可能希望根据环境变量或其他因素动态生成PluginConfig类。

### PluginConfig属性

| 名称                  | 描述                                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------|
| `name`                | 插件名称（与插件源目录相同）                                                                   |
| `verbose_name`        | 插件的人类友好名称                                                                                       |
| `version`             | 当前版本（鼓励使用[语义化版本](https://semver.org/)）                                               |
| `description`         | 插件目的的简要描述                                                                                |
| `author`              | 插件作者的名称                                                                                                  |
| `author_email`        | 作者的公共电子邮件地址                                                                                            |
| `base_url`            | 用于插件URL的基本路径（可选）。如果未指定，将使用项目的`name`。                        |
| `required_settings`   | 用户必须定义的任何配置参数的列表                                              |
| `default_settings`    | 包含配置参数及其默认值的字典                                                        |
| `django_apps`         | 附加的Django应用程序的列表，以与插件一起加载                                           |
| `min_version`         | 插件与之兼容的NetBox的最低版本                                                          |
| `max_version`         | 插件与之兼容的NetBox的最高版本                                                          |
| `middleware`          | 添加到NetBox内置中间件后面的中间件类的列表                                               |
| `queues`              | 创建自定义后台任务队列的列表                                                                     |
| `search_extensions`   | 搜索索引类列表的点路径（默认为`search.indexes`）                                        |
| `data_backends`       | 数据源后端类列表的点路径（默认为`data_backends.backends`）                             |
| `template_extensions` | 模板扩展类列表的点路径（默认为`template_content.template_extensions`）                    |
| `menu_items`          | 插件提供的菜单项列表的点路径（默认为`navigation.menu_items`）                            |
| `graphql_schema`      | 插件的GraphQL模式类的点路径，如果有的话（默认为`graphql.schema`）                             |
| `user_preferences`    | 插件定义的用户首选项映射的点路径（默认为`preferences.preferences`）                           |

所有必需的设置必须由用户配置。如果配置参数在`required_settings`和`default_settings`中都列出，则将忽略默认设置。

!!! tip "访问配置参数"
    可以使用`get_plugin_config()`函数访问插件配置参数。例如：
    
    ```python
    from netbox.plugins import get_plugin_config
    get_plugin_config('my_plugin', 'verbose_name')
    ```

#### 关于`django_apps`的重要说明

加载附加的应用程序可能会引发更多的问题，而且可能会使在NetBox本身中识别问题变得更加困难。`django_apps`属性仅用于需要更深度的Django集成的高级用例。

从此列表中的应用程序将在定义的顺序之前插入插件的`PluginConfig`。将插件的`PluginConfig`模块添加到此列表会更改此行为，允许在插件之后加载应用程序。

任何附加的应用程序必须在与NetBox相同的Python环境中安装，否则在加载插件时将引发`ImproperlyConfigured`异常。

## 创建setup.py

`setup.py`是用于打包和安装插件的[设置脚本](https://docs.python.org/3.8/distutils/setupscript.html)。该脚本的主要功能是调用setuptools库的`setup()`函数，以创建Python分发包。我们可以传递许多关键字参数来控制包的创建，以及提供有关插件的元数据。下面是一个示例`setup.py`：

```python
from setuptools import find_packages, setup

setup(
    name='my-example-plugin',
    version='0.1',
    description='An example NetBox plugin',
    url='https://github.com/jeremystretch/my-example-plugin',
    author='Jeremy Stretch',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
```

其中许多内容都不言自明，但有关更多信息，请参阅[setuptools文档](https://setuptools.readthedocs.io/en/latest/setuptools.html)。

!!! info
    `zip_safe=False`是**必需的**，因为当前的插件版本由于上游python问题 [issue19699](https://bugs.python.org/issue19699) 不是zip安全的。  

## 创建虚拟环境

强烈建议为插件的开发创建Python [虚拟环境](https://docs.python.org/3/tutorial/venv.html)，而不是使用系统范围的包。这将使您完全控制所有依赖项的安装版本，并避免与系统包的冲突。此环境可以放在您喜欢的任何地方，但是它应该从版本控制中排除。 （一个常见的约定是将所有虚拟环境保存在用户的主目录中，例如`~/.virtualenvs/`。）

```shell
python3 -m venv ~/.virtualenvs/my_plugin
```

要使NetBox在此环境中可用，您可以创建一个指向其位置的路径文件。这将在激活时将NetBox添加到Python路径中。请确保调整下面的命令，以指定您实际的虚拟环境路径、Python版本和NetBox安装位置。

```shell
echo /opt/netbox/netbox > $VENV/lib/python3.8/site-packages/netbox.pth
```

## 开发安装

为了简化开发，建议在这一点上使用setuptools的`develop`模式安装插件。这将在Python环境中创建指向插件开发目录的符号链接。从插件的根目录中使用`setup.py`调用`develop`参数（而不是`install`）：

```no-highlight
$ python setup.py develop
```

## 配置NetBox

要在NetBox中启用插件，请将其添加到`configuration.py`中的`PLUGINS`参数中：

```python
PLUGINS = [
    'my_plugin',
]
```

# 插件

插件是打包的 [Django](https://docs.djangoproject.com/) 应用程序，可以与 NetBox 一起安装，以提供核心应用程序中没有的自定义功能。插件可以引入其自己的模型和视图，但不能干扰现有组件。NetBox 用户可以选择安装社区提供的插件，或自行构建插件。

## 功能

NetBox 插件架构允许以下操作：

* **添加新数据模型。** 插件可以引入一个或多个模型来存储数据。 （模型本质上是 SQL 数据库中的表。）
* **添加新的 URL 和视图。** 插件可以在 `/plugins` 根路径下注册 URL，以为用户提供可浏览的视图。
* **向现有模型模板添加内容。** 模板内容类可用于在核心 NetBox 模型的视图中注入自定义 HTML 内容。此内容可以显示在页面的左侧、右侧或底部。
* **添加导航菜单项。** 每个插件可以在导航菜单中注册新链接。每个链接可以具有一组特定操作的按钮，类似于内置导航项。
* **添加自定义中间件。** 每个插件都可以注册自定义的 Django 中间件。
* **声明配置参数。** 每个插件可以在其独特的命名空间中定义所需、可选和默认配置参数。插件配置参数由用户在 `configuration.py` 中的 `PLUGINS_CONFIG` 下定义。
* **限制 NetBox 版本的安装。** 插件可以指定其兼容的最低和/或最高 NetBox 版本。

## 限制

无论是出于政策还是技术限制，插件与 NetBox 核心的交互都会受到某些限制。插件可能无法：

* **修改核心模型。** 插件不能以任何方式更改、删除或覆盖核心 NetBox 模型。此规则的目的是确保核心数据模型的完整性。
* **在 `/plugins` 根路径之外注册 URL。** 所有插件的 URL 限制在此路径下，以防止与核心或其他插件的路径冲突。
* **覆盖核心模板。** 插件可以在支持的地方注入附加内容，但不能操纵或删除核心内容。
* **修改核心设置。** 插件提供了配置注册表，但它们不能更改或删除核心配置。
* **禁用核心组件。** 插件不允许禁用或隐藏核心 NetBox 组件。

## 安装插件

以下说明详细描述了安装和启用 NetBox 插件的过程。

### 安装软件包

根据其安装说明下载并安装插件软件包。通过 PyPI 发布的插件通常使用 pip 安装。请确保在 NetBox 的虚拟环境中安装插件。

```no-highlight
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install <package>
```

或者，您可以手动安装插件，通过运行 `python setup.py install`。如果您正在开发插件并希望仅临时安装它，请改用 `python setup.py develop` 运行。

### 启用插件

在 `configuration.py` 中，将插件的名称添加到 `PLUGINS` 列表中：

```python
PLUGINS = [
    'plugin_name',
]
```

### 配置插件

如果插件需要任何配置，请在 `configuration.py` 中的 `PLUGINS_CONFIG` 参数下定义它。插件的 README 文件应详细说明可用的配置参数。

```no-highlight
PLUGINS_CONFIG = {
    'plugin_name': {
        'foo': 'bar',
        'buzz': 'bazz'
    }
}
```

### 运行数据库迁移

如果插件引入了新的数据库模型，请运行提供的模式迁移：

```no-highlight
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py migrate
```

### 收集静态文件

插件可以打包要由 HTTP 前端直接提供的静态文件。确保将这些文件与 `collectstatic` 管理命令复制到静态根目录：

```no-highlight
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py collectstatic
```

### 重启 WSGI 服务

重启 WSGI 服务以加载新插件：

```no-highlight
# sudo systemctl restart netbox
```

## 移除插件

按照以下步骤完全删除插件。

### 更新配置

从 `configuration.py` 中的 `PLUGINS` 列表中删除插件。还要从 `PLUGINS_CONFIG` 中删除任何相关的配置参数。

### 删除 Python 包

使用 `pip` 来删除已安装的插件：

```no-highlight
$ source /opt/netbox/venv/bin/activate
(venv) $ pip uninstall <package>
```

### 重启 WSGI 服务

重启 WSGI 服务：

```no-highlight
# sudo systemctl restart netbox
```

### 删除数据库表格

!!! 注意
    此步骤仅适用于已创建一个或多个数据库表格的插件（通常是通过引入新模型）。如果不确定，请查看插件的文档。

进入 PostgreSQL 数据库 shell 以确定插件是否已创建任何 SQL 表格。在下面的示例中，将 `pluginname` 替换为要删除的插件的名称。 （您还可以运行不带模式的 `\dt` 命令来列出 _所有_ 表格。）

```no-highlight
netbox=> \dt pluginname_*
                   List of relations
                   List of relations
 Schema |       Name     | Type  | Owner
--------+----------------+-------+--------
 public | pluginname_foo | table | netbox
 public | pluginname_bar | table | netbox
(2 rows)
```

!!! 警告
    删除表格时请格外小心。强烈建议用户在执行这些操作之前立即备份数据库。

删除列表中的每个表格以从数据库中删除它：

```no-highlight
netbox=> DROP TABLE pluginname_foo;
DROP TABLE
netbox=> DROP TABLE pluginname_bar;
DROP TABLE
```

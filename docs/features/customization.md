# 自定义

虽然 NetBox 力求满足每个网络的需求，但用户的需求是为了适应他们独特的环境，这是不容忽视的。NetBox 以此为出发点而构建，可以通过多种方式进行自定义，以更好地适应您的特定需求。

## 标签

NetBox 中的大多数对象都可以分配用户创建的标签，以帮助组织和过滤。标签值完全是任意的：它们可以用来存储键值对数据，或者仅作为可以过滤对象的标签使用。每个标签还可以分配颜色，以便在用户界面中更快地区分。

可以根据对象应用的标签来过滤对象。例如，以下 API 请求将检索所有标记为 "monitored" 的设备：

```no-highlight
GET /api/dcim/devices/?tag=monitored
```

可以多次指定 `tag` 过滤器，以匹配只有_所有_指定标签的对象：

```no-highlight
GET /api/dcim/devices/?tag=monitored&tag=deprecated
```

## 书签

!!! 信息 "此功能在 NetBox v3.6 中引入。"

用户可以将他们最常访问的对象添加为书签，以便于访问。书签列在用户的个人资料下，并可以在用户的个人仪表板上显示自定义过滤和排序。

## 自定义字段

虽然 NetBox 开箱即用提供了相当广泛的数据模型，但可能会出现需要存储与 NetBox 对象相关的某些额外数据的需求。例如，您可能需要在安装设备时记录发票 ID，或在创建新 IP 前缀时记录批准权威。NetBox 管理员可以在内置对象上创建自定义字段以满足这些需求。

NetBox 支持许多类型的自定义字段，从基本数据类型（如字符串和整数）到复杂结构（如选择列表或原始 JSON）。甚至可以添加引用 NetBox 其他对象的自定义字段。自定义字段数据直接存储在与之关联的对象数据库中，确保了最小的性能影响。自定义字段数据可以通过 REST API 进行读写，就像内置字段一样。

要了解更多关于此功能的信息，请查看[自定义字段文档](../customization/custom-fields.md)。

## 自定义链接

自定义链接允许您方便地从 NetBox UI 中引用与 NetBox 对象相关的外部资源。例如，您可能希望将 NetBox 中建模的每个虚拟机链接到某些编排应用中的相应视图。您可以为虚拟机模型创建一个模板化的自定义链接，指定类似以下内容的链接 URL：

```no-highlight
http://server.local/vms/?name={{ object.name }}
```

现在，当在 NetBox 中查看虚拟机时，用户将看到一个带有所选标题和链接的便捷按钮（包括正在查看的 VM 的名称）。自定义链接的文本和 URL 都可以以这种方式模板化，自定义链接可以分组到下拉菜单中，以更有效地显示。

要了解更多关于此功能的信息，请查看[自定义链接文档](../customization/custom-links.md)。

## 自定义验证

虽然 NetBox 采用强大的内置对象验证来确保其数据库的完整性，但您可能希望强制执行针对某些对象的创建和修改的额外规则。例如，您可能要求 NetBox 中定义的每台设备都遵循特定的命名方案并包含资产标签。您可以在 NetBox 中配置自定义验证规则以强制执行这些要求，针对设备模型：

```python
CUSTOM_VALIDATORS = {
    "dcim.device": [
        {
            "name": {
                "regex": "[a-z]+\d{3}"
            },
            "asset_tag": {
                "required": True
            }
        }
    ]
}
```

要了解更多关于此功能的信息，请查看[自定义验证文档](../customization/custom-validation.md)。

## 导出模板

大多数 NetBox 对象可以以两种内置的 CSV 格式批量导出：当前视图（用户当前在对象列表中看到的内容）或所有可用数据。NetBox 还提供了通过导出模板定义自己的自定义数据导出格式的功能。导出模板本质上是与特定对象类型相关联的 [Jinja2](https://jinja.palletsprojects.com/) 模板代码。从 NetBox UI 中的对象列表中，用户可以选择任何已创建的导出模板，根据模板逻辑导出对象。

导出模板不必渲染 CSV 数据：其输出可以是任何基于字符的格式。例如，您可能希望使用制表符作为分隔符来渲染数据，甚至直接从 IP 地址列表中创建 DNS 地址记录。导出模板是一种快速获取所需数据和所需格式的好方法。

要了解更多关于此功能的信息，请查看[导出模板文档](../customization/export-templates.md)。

## 报告

NetBox 管理员可以安装自定义 Python 脚本，称为 _报告_，这些脚本在 NetBox 内运行，并可以在 NetBox UI 中执行和分析。报告是根据一组任意规则评估 NetBox 对象的好方法。例如，您可以编写一个报告来检查每台路由器是否具有分配了 IP 地址的环回接口，或每个站点是否定义了一组最小的 VLAN。

当报告运行时，它记录有关正在执行的操作的日志消息，并最终结果为通过或失败。报告可以通过 UI、REST API 或 CLI（作为管理命令）执行。它们可以立即运行或计划在将来的时间运行。

要了解更多关于此功能的信息，请查看[报告文档](../customization/reports.md)。

## 自定义脚本

自定义脚本与报告类似，但更强大。自定义脚本可以通过表单（或 API 数据）提示用户输入，并且建立在不仅仅是报告的基础上。自定义脚本通常用于自动化任务，如在 NetBox 中填充新对象，或与外部系统交换数据。与报告一样，它们可以通过 UI、REST API 或 CLI 运行，并且可以计划在将来的时间执行。

自定义脚本可以使用完整的 Python 环境，包括 NetBox 的所有内部机制：脚本可以做的事情没有人为限制。因此，自定义脚本被视为高级功能，需要对 Python 和 NetBox 的数据模型有足够的熟悉。

要了解更多关于此功能的信息，请查看[自定义脚本文档](../customization/custom-scripts.md)。
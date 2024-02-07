# NetBox v3.7

## v3.7.2 (2024-02-05)

### Enhancements

* [#13729](https://github.com/netbox-community/netbox/issues/13729) - 从更改日志数据中省略敏感数据源参数
* [#14645](https://github.com/netbox-community/netbox/issues/14645) - 限制在接口列表下显示的已分配IP地址的数量

### Bug Fixes

* [#14500](https://github.com/netbox-community/netbox/issues/14500) - 在查看前缀时优化可用子前缀和范围的计算
* [#14511](https://github.com/netbox-community/netbox/issues/14511) - 修复连接到提供商网络的接口的GraphQL支持
* [#14572](https://github.com/netbox-community/netbox/issues/14572) - 更正个别报告和脚本模块列出的作业数量
* [#14703](https://github.com/netbox-community/netbox/issues/14703) - 在遇到配置错误的仪表板时恢复到默认布局
* [#14755](https://github.com/netbox-community/netbox/issues/14755) - 通过REST API创建自定义字段选择集时修复选择值和标签的验证
* [#14838](https://github.com/netbox-community/netbox/issues/14838) - 在编辑事件规则时更改操作类型时避免损坏JSON数据
* [#14839](https://github.com/netbox-community/netbox/issues/14839) - 尝试终止到虚拟机接口的隧道时修复表单验证错误
* [#14840](https://github.com/netbox-community/netbox/issues/14840) - 修复在渲染引用用户的自定义字段时的`NoReverseMatch`异常
* [#14847](https://github.com/netbox-community/netbox/issues/14847) - 仅在选择IKEv1时可以设置IKE策略模式
* [#14851](https://github.com/netbox-community/netbox/issues/14851) - 删除用户时自动移除任何相关的书签
* [#14879](https://github.com/netbox-community/netbox/issues/14879) - 在REST API数据源表示中包括自定义字段
* [#14885](https://github.com/netbox-community/netbox/issues/14885) - 在VPN隧道创建表单中添加缺失的"组"字段
* [#14892](https://github.com/netbox-community/netbox/issues/14892) - 由于缺少用户名，在命令行运行报告/脚本时修复异常
* [#14920](https://github.com/netbox-community/netbox/issues/14920) - 在批量导入虚拟设备上下文时包含显示可用状态选择的按钮
* [#14945](https://github.com/netbox-community/netbox/issues/14945) - 修复设备类型组件的"全选"按钮
* [#14947](https://github.com/netbox-community/netbox/issues/14947) - 确保总是在对象的更改日志中记录标签的应用和移除
* [#14962](https://github.com/netbox-community/netbox/issues/14962) - 修复直接分配给站点（而不是通过集群）的VM的配置上下文渲染
* [#14999](https://github.com/netbox-community/netbox/issues/14999) - 为接口FHRP组分配修复"创建并添加另一个"链接
* [#15015](https://github.com/netbox-community/netbox/issues/15015) - 在前缀视图下分配下一个可用IP地址时预填充分配的租户
* [#15020](https://github.com/netbox-community/netbox/issues/15020) - 更改集群的分配站点时自动更新所有VM
* [#15025](https://github.com/netbox-community/netbox/issues/15025) - `can_add()`模板过滤器应接受模型（而不是实例）

---

## v3.7.1 (2024-01-17)

### Bug Fixes

* [#13844](https://github.com/netbox-community/netbox/issues/13844) - 在前缀表单下过滤VLAN时使用`available_at_site`过滤器
* [#14663](https://github.com/netbox-community/netbox/issues/14663) - 修复在将初始终止设置为VM接口时创建隧道
* [#14706](https://github.com/netbox-community/netbox/issues/14706) - 放宽隧道终止到IP地址的一对一映射
* [#14709](https://github.com/netbox-community/netbox/issues/14709) - 修复隧道终止类型选择名称中的拼写错误
* [#14749](https://github.com/netbox-community/netbox/issues/14749) - 从DeviceBay上删除错误的翻译包装器`installed_device`
* [#14778](https://github.com/netbox-community/netbox/issues/14778) - 自定义字段API序列化程序应接受所有可选字段的null值
* [#14791](https://github.com/netbox-community/netbox/issues/14791) - 在父前缀中搜索时隐藏可用前缀
* [#14793](https://github.com/netbox-community/netbox/issues/14793) - 添加丢失的Diffie-Hellman group 15
* [#14816](https://github.com/netbox-community/netbox/issues/14816) - 确保默认联系人分配排序一致
* [#14817](https://github.com/netbox-community/netbox/issues/14817) - 放宽大量导入时IKE和IPSec模型的必填字段
* [#14827](https://github.com/netbox-community/netbox/issues/14827) - 确保响应事件时处理所有匹配的事件规则

---

## v3.7.0 (2023-12-29)

### Breaking Changes

* Webhook模型中已删除以下字段：`content_types`、`type_create`、`type_update`、`type_delete`、`type_job_start`、`type_job_end`、`enabled`和`conditions`。现在，Webhook通过[event rules](../features/event-rules.md)与事件关联。在升级时，任何现有的Webhook将自动创建新的事件规则。
* [自定义字段模型](../models/extras/customfield.md)上的`ui_visibility`字段已被替换为两个新字段：`ui_visible`和`ui_editable`。在升级时，这两个新字段的值将自动从原始字段映射过来。
* 用于通过模型功能查询内容类型的内部ConfigRevision模型已被删除。它已由NetBox的ContentType (`core.models.ContentType`)代理模型上的新`with_feature()`管理器方法替换。
* 内部的ConfigRevision模型已从`extras`移动到`core`。在升级过程中将保留配置历史记录。
* [L2VPN](../models/vpn/l2vpn.md)和[L2VPNTermination](../models/vpn/l2vpntermination.md)模型已从`ipam`应用移动到新的`vpn`应用。所有对象数据将保留，但请注意，相关的API端点也已移动到`/api/vpn/`。
* `CustomFieldsMixin`、`SavedFiltersMixin`和`TagsMixin`类已从`extras.forms.mixins`模块移动到`netbox.forms.mixins`。
* `netbox.models.features.WebhooksMixin`类已重命名为`EventRulesMixin`。

### New Features

#### VPN Tunnels ([#9816](https://github.com/netbox-community/netbox/issues/9816))

引入了几个新模型，以支持[VPN隧道管理](../features/vpn-tunnels.md)。用户现在可以定义具有两个或多个终止的隧道，以表示点对点或集线式拓扑。每个终止都是对设备或虚拟机上的虚拟接口的终止。此外，用户可以定义IKE和IPSec提议和策略，这些可以应用于隧道以记录加密和身份验证策略。

#### Event Rules ([#14132](https://github.com/netbox-community/netbox/issues/14132))

此版本引入了[event规则](../features/event-rules.md)，可以用于在NetBox中发生的事件自动发送Webhook或执行自定义脚本。例如，现在可以在创建具有特定状态或标签的新站点时自动运行自定义脚本。

事件规则替代并扩展了以前内置到Webhook模型中的功能。在升级时，任何现有的Webhook将自动创建新的事件规则。

#### Virtual Machine Disks ([#8356](https://github.com/netbox-community/netbox/issues/8356))

引入了新的[VirtualDisk](../models/virtualization/virtualdisk.md)模型，以支持将离散的虚拟磁盘分配给虚拟机。VirtualMachine模型上保留了`size`字段，并将自动填充所有分配的虚拟磁盘的累积大小。选择不使用新模型的用户可以像以前的版本一样独立使用VirtualMachine `size`属性。

#### Object Protection Rules ([#10244](https://github.com/netbox-community/netbox/issues/10244))

引入了新的[`PROTECTION_RULES`](../configuration/data-validation.md#protection_rules)配置参数。与[自定义验证规则](../customization/custom-validation.md)可以用于强制执行某些对象属性值的方式类似，保护规则可防止删除不符合指定条件的对象。这使管理员可以防止删除具有"active"状态的站点等对象。

#### 改进的自定义字段可见性控制 ([#13299](https://github.com/netbox-community/netbox/issues/13299))

[自定义字段模型](../models/extras/customfield.md)上的`ui_visible`字段已被两个新字段`ui_visible`和`ui_editable`所取代，它们分别控制查看和编辑

对象时自定义字段的显示方式和是否显示。将这两个功能分成独立的字段允许更多地控制每个自定义字段如何呈现给用户。这些字段的值将在升级过程中自动根据原始字段的值设置。

#### 改进的全局搜索结果 ([#14134](https://github.com/netbox-community/netbox/issues/14134))

全局搜索结果现在包括有关每个对象的其他上下文，例如描述、状态和/或相关对象。要显示的属性集特定于每个对象类型，并通过在对象的[SearchIndex类](../plugins/development/search.md#netbox.search.SearchIndex)下设置`display_attrs`来定义。

#### 为插件注册表格列 ([#14173](https://github.com/netbox-community/netbox/issues/14173))

插件现在可以为核心NetBox表格[注册自己的自定义列](../plugins/development/tables.md#extending-core-tables)。例如，插件可以使用新的`register_table_column()`实用程序函数在SiteTable上注册一个新列，并且用户可以选择显示该列。

#### 为插件注册数据后端 ([#13381](https://github.com/netbox-community/netbox/issues/13381))

插件现在可以[注册自己的数据后端](../plugins/development/data-backends.md)以用于[同步数据源](../features/synchronized-data.md)。这使得插件可以在提供的git、S3和本地路径后端之外引入新的后端。

### Enhancements

* [#12135](https://github.com/netbox-community/netbox/issues/12135) - 防止删除具有子项分配的接口以避免孤立的接口
* [#12216](https://github.com/netbox-community/netbox/issues/12216) - 为电路类型添加`color`字段
* [#13230](https://github.com/netbox-community/netbox/issues/13230) - 允许在计算机柜的利用率时排除设备类型
* [#13334](https://github.com/netbox-community/netbox/issues/13334) - 在Job模型上添加`error`字段以记录与其执行相关的任何错误
* [#13427](https://github.com/netbox-community/netbox/issues/13427) - 引入一种机制，可以用来排除不符合指定条件的对象的删除，类似于[自定义验证规则](../customization/custom-validation.md)
* [#13690](https://github.com/netbox-community/netbox/issues/13690) - 在通过Web UI删除对象之前显示要删除的任何相关对象
* [#13794](https://github.com/netbox-community/netbox/issues/13794) - 任何与Tenant有关系的模型现在都自动包含在租户视图下的相关对象列表中
* [#13808](https://github.com/netbox-community/netbox/issues/13808) - 为虚拟机添加`/render-config` REST API端点
* [#14035](https://github.com/netbox-community/netbox/issues/14035) - 在全局搜索结果中按值对等权重对对象排序以提高可读性
* [#14147](https://github.com/netbox-community/netbox/issues/14147) - 通过新的`CHANGELOG_SKIP_EMPTY_CHANGES`配置参数避免记录空的更改日志条目
* [#14156](https://github.com/netbox-community/netbox/issues/14156) - 为联系人分配启用自定义字段
* [#14240](https://github.com/netbox-community/netbox/issues/14240) - 增加自定义字段最小和最大数字验证器的最大值
* [#14361](https://github.com/netbox-community/netbox/issues/14361) - 为Webhook添加`description`字段
* [#14365](https://github.com/netbox-community/netbox/issues/14365) - 引入`job_start`和`job_end`信号以允许自动化插件操作
* [#14434](https://github.com/netbox-community/netbox/issues/14434) - 为电缆添加特定于模型的终止对象过滤器（例如`interface_id`和`consoleport_id`）
* [#14436](https://github.com/netbox-community/netbox/issues/14436) - 为所有GenericForeignKey字段添加PostgreSQL索引
* [#14579](https://github.com/netbox-community/netbox/issues/14579) - 允许用户指定UI翻译的首

选语言

### Translations

* [#14075](https://github.com/netbox-community/netbox/issues/14075) - 添加西班牙语翻译
* [#14096](https://github.com/netbox-community/netbox/issues/14096) - 添加法语翻译
* [#14145](https://github.com/netbox-community/netbox/issues/14145) - 添加葡萄牙语翻译
* [#14266](https://github.com/netbox-community/netbox/issues/14266) - 添加俄语翻译

### Bug Fixes

* [#14432](https://github.com/netbox-community/netbox/issues/14432) - 修复全局搜索结果属性的超链接
* [#14472](https://github.com/netbox-community/netbox/issues/14472) - 修复对象编辑表单中隐藏自定义字段的显示
* [#14499](https://github.com/netbox-community/netbox/issues/14499) - 放宽IKE和IPSec提议上的加密/身份验证算法要求
* [#14550](https://github.com/netbox-community/netbox/issues/14550) - 修复更改现有事件规则的操作类型

### Other Changes

* [#13550](https://github.com/netbox-community/netbox/issues/13550) - 优化`ActionsMixin`下声明视图操作的格式（保留向后兼容性）
* [#13645](https://github.com/netbox-community/netbox/issues/13645) - 仅在启用Sentry报告时才需要安装`sentry-sdk` Python库
* [#14036](https://github.com/netbox-community/netbox/issues/14036) - 将插件资源从`extras`应用移动到`netbox`（保留向后兼容性）
* [#14153](https://github.com/netbox-community/netbox/issues/14153) - 使用代理ContentType管理器上的新`with_feature()`方法替换`FeatureQuery`
* [#14311](https://github.com/netbox-community/netbox/issues/14311) - 将L2VPN模型从`ipam`应用移动到新的`vpn`应用
* [#14312](https://github.com/netbox-community/netbox/issues/14312) - 将ConfigRevision模型从`extras`应用移动到`core`
* [#14326](https://github.com/netbox-community/netbox/issues/14326) - 将自定义字段特性混合类从`extras`应用移动到`netbox`
* [#14395](https://github.com/netbox-community/netbox/issues/14395) - 将`extras.webhooks_worker.process_webhook()`移动到`extras.webhooks.send_webhook()`（保留向后兼容性）
* [#14424](https://github.com/netbox-community/netbox/issues/14424) - 从StagedChange中删除更改日志记录功能
* [#14458](https://github.com/netbox-community/netbox/issues/14458) - 删除过时的`clearcache`管理命令
* [#14536](https://github.com/netbox-community/netbox/issues/14536) - 默认情况下强制对非VRF前缀和IP地址执行唯一性检查（`ENFORCE_GLOBAL_UNIQUE`现在默认为true）

### REST API Changes

* 引入了以下端点：
    * `/api/extras/event-rules/`
    * `/api/virtualization/virtual-disks/`
    * `/api/vpn/ike-policies/`
    * `/api/vpn/ike-proposals/`
    * `/api/vpn/ipsec-policies/`
    * `/api/vpn/ipsec-profiles/`
    * `/api/vpn/ipsec-proposals/`
    * `/api/vpn/tunnels/`
    * `/api/vpn/tunnel-terminations/`
* 以下端点已移动：
    * `/api/ipam/l2vpns/` -> `/api/vpn/l2vpns/`
    * `/api/ipam/l2vpn-terminations/` -> `/api/vpn/l2vpn-terminations/`
* circuits.CircuitType
    * 添加了可选的`color`选择字段
* core.Job
    * 添加了只读的`error`字符字段
* extras.Webhook
    * 删除了以下字段（已移动到新的`EventRule`模型）：
        * `content_types`
        * `type_create`
        * `type_update`
        * `type_delete`
        * `type_job_start`
        * `type_job_end`
        * `enabled`
        * `conditions`
    * 添加了可选

的`description`字段
* dcim.DeviceType
    * 添加了`exclude_from_utilization`布尔字段
* extras.CustomField
    * 删除了`ui_visibility`字段
    * 添加了`ui_visible`和`ui_editable`选择字段
* tenancy.ContactAssignment
    * 添加了对自定义字段的支持
* virtualization.VirtualDisk
    * 添加了只读的`virtual_disk_count`整数字段
* virtualization.VirtualMachine
    * 添加了`/render-config`端点
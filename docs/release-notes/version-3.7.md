NetBox v3.7.0 是2023年12月29日发布的版本，它引入了一系列新功能、增强和修复了一些问题。以下是该版本的一些重要变化和功能：

### 主要变更

- Webhook模型中已删除以下字段：`content_types`、`type_create`、`type_update`、`type_delete`、`type_job_start`、`type_job_end`、`enabled` 和 `conditions`。现在，Webhooks通过[事件规则](../features/event-rules.md)与事件相关联。在升级时，现有的Webhooks将自动为其创建新的事件规则。
- 自定义字段模型上的 `ui_visibility` 字段已被替换为两个新字段：`ui_visible` 和 `ui_editable`。在升级过程中，这些新字段的值将自动从原始字段映射。
- 用于查询模型特征的 `FeatureQuery` 类已被移除，它已被NetBox的ContentType（`core.models.ContentType`）代理模型上的新 `with_feature()` 管理方法替代。
- 内部的 ConfigRevision 模型已从 `extras` 移动到 `core`。在升级过程中将保留配置历史记录。
- [L2VPN](../models/vpn/l2vpn.md) 和 [L2VPNTermination](../models/vpn/l2vpntermination.md) 模型已从 `ipam` 应用程序移动到新的 `vpn` 应用程序。但请注意，相关的API端点也已经移动到 `/api/vpn/`。
- `CustomFieldsMixin`、`SavedFiltersMixin` 和 `TagsMixin` 类已从 `extras.forms.mixins` 模块移动到 `netbox.forms.mixins`。
- `netbox.models.features.WebhooksMixin` 类已重命名为 `EventRulesMixin`。

### 新功能

#### VPN隧道

- 引入了多个新模型，以启用[VPN隧道管理](../features/vpn-tunnels.md)。用户现在可以定义具有两个或多个终结点的隧道，以表示点对点或枢纽和辐射拓扑。每个终结点都与设备或虚拟机上的虚拟接口连接。此外，用户可以定义IKE和IPSec提案和策略，这些可以应用于隧道，以记录加密和身份验证策略。

#### 事件规则

- 此版本引入了[事件规则](../features/event-rules.md)，可以用于在NetBox中发生事件时自动发送Webhook或执行自定义脚本。例如，现在可以在创建具有特定状态或标签的新站点时自动运行自定义脚本。

事件规则取代了之前内置在Webhook模型中的功能。在升级时，现有的Webhooks将自动为其创建新的事件规则。

#### 虚拟机磁盘

- 引入了新的 [VirtualDisk](../models/virtualization/virtualdisk.md) 模型，以启用对虚拟机的离散虚拟磁盘分配进行跟踪。VirtualMachine 模型上的 `size` 字段已保留，并将自动填充所有分配的虚拟磁盘的累积大小。选择不使用新模型的用户可以像之前版本一样独立使用VirtualMachine的 `size` 属性。

#### 对象保护规则

- 引入了新的 [`PROTECTION_RULES`](../configuration/data-validation.md#protection_rules) 配置参数。与[自定义验证规则](../customization/custom-validation.md)类似，保护规则用于防止删除不符合指定标准的对象。这使管理员可以防止例如删除具有“活动”状态的站点。

#### 改进的自定义字段可见性控制

- 自定义字段模型上的 `ui_visibility` 字段已被两个新字段 `ui_visible` 和 `ui_editable` 替代，它们分别控制在查看和编辑对象时如何以及是否显示自定义字段。将这两个功能分离为独立字段允许更多控制每个自定义字段如何呈现给用户。在升级过程中，这些字段的值将从原始字段的值自动设置。

#### 改进的全局搜索结果

- 全局搜索结果现在包括关于每个对象的其他上下文信息，例如描述、状态和/或相关对象。要显示的属性集因对象类型而异，并通过在对象的 [SearchIndex类](../plugins/development/search.md#netbox.search.SearchIndex) 下设置 `display_attrs` 来定义。

#### 插件的表格列注册

- 插件现在可以为核心NetBox表格注册自己的自定义列。例如，插件可以使用新的 `register_table_column()` 实用程序函数在 SiteTable 上注册新列，用户可以选择显示该列。

#### 插件的数据后端注册

- 插件现在可以为[同步数据源](../features/synchronized-data.md)注册自己的数据后端。这使插件可以引入除了本地提供的git、S3和本地路径后端之外的新后端。

### 增强

- 避免删除已分配子接口的接口，以避免孤立的接口。
- 为电路类型添加了一个 `color` 字段。
- 允许在计算机柜利用率时排除设备类型。
- 在Job模型上添加了一个 `error` 字段，用于记录与其执行相关的任何错误。
- 引入了一个机制，用于从通用对象类型列表中排除模型。
- 在通过Web UI删除对象之前，显示任何要删除的相关对象。
- 任何与Tenant相关的模型现在都会自动包括在租户视图下的相关对象列表中。
- 为虚拟机添加了 `/render-config` REST API端点。
- 全局搜索

结果中以值排序具有等效权重的对象，以提高可读性。
- 通过新的 `CHANGELOG_SKIP_EMPTY_CHANGES` 配置参数避免记录空的变更日志条目。
- 启用联系人分配的自定义字段。
- 增加了自定义字段最小值和最大值数值验证器的最大值。
- 为Webhook添加了 `description` 字段。
- 引入了 `job_start` 和 `job_end` 信号，以允许自动化插件操作。

### 修复的问题

- 修复了全局搜索结果属性的超链接。
- 修复了在对象编辑表单中显示隐藏自定义字段的问题。
- 放宽了IKE和IPSec提案上的加密/身份验证算法要求。
- 修复了更改事件规则的操作类型的问题。

### 其他变更

- 优化了在 `ActionsMixin` 下声明视图操作的格式（保留了向后兼容性）。
- 只有在启用Sentry报告时才需要安装 `sentry-sdk` Python库。
- 将插件资源从 `extras` 应用程序移动到 `netbox`（保留了向后兼容性）。
- 使用代理ContentType管理器上的新的 `with_feature()` 方法替代 `FeatureQuery`。
- 将L2VPN模型从 `ipam` 应用程序移动到新的 `vpn` 应用程序。
- 将ConfigRevision模型从 `extras` 应用程序移动到 `core`。
- 将Form特性混合类从 `extras` 应用程序移动到 `netbox`。
- 将 `extras.webhooks_worker.process_webhook()` 移动到 `extras.webhooks.send_webhook()`（保留了向后兼容性）。
- 从StagedChange中移除更改日志功能。
- 删除了过时的 `clearcache` 管理命令。
- 默认情况下强制执行非VRF前缀和IP地址的唯一性（`ENFORCE_GLOBAL_UNIQUE` 现在默认为true）。

### REST API变更

- 引入了以下端点：
  - `/api/extras/event-rules/`
  - `/api/virtualization/virtual-disks/`
  - `/api/vpn/ike-policies/`
  - `/api/vpn/ike-proposals/`
  - `/api/vpn/ipsec-policies/`
  - `/api/vpn/ipsec-profiles/`
  - `/api/vpn/ipsec-proposals/`
  - `/api/vpn/tunnels/`
  - `/api/vpn/tunnel-terminations/`
- 移动了以下端点：
  - `/api/ipam/l2vpns/` -> `/api/vpn/l2vpns/`
  - `/api/ipam/l2vpn-terminations/` -> `/api/vpn/l2vpn-terminations/`
- circuits.CircuitType
  - 添加了可选的 `color` 选择字段
- core.Job
  - 添加了只读的 `error` 字符字段
- extras.Webhook
  - 移除了以下字段（这些字段已经移动到新的 `EventRule` 模型）：
    - `content_types`
    - `type_create`
    - `type_update`
    - `type_delete`
    - `type_job_start`
    - `type_job_end`
    - `enabled`
    - `conditions`
  - 添加了可选的 `description` 字段
- dcim.DeviceType
  - 添加了 `exclude_from_utilization` 布尔字段
- extras.CustomField
  - 移除了 `ui_visibility` 字段
  - 添加了 `ui_visible` 和 `ui_editable` 选择字段
- tenancy.ContactAssignment
  - 增加了对自定义字段的支持
- virtualization.VirtualDisk
  - 添加了只读的 `virtual_disk_count` 整数字段
- virtualization.VirtualMachine
  - 添加了 `/render-config` 端点
  
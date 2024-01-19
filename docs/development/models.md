# NetBox模型

## 模型类型

NetBox模型代表离散的对象类型，例如设备或IP地址。根据[Django约定](https://docs.djangoproject.com/en/stable/topics/db/models/)，每个模型都定义为Python类，并在PostgreSQL数据库中拥有自己的表。所有NetBox数据模型都可以按类型分类。

Django的[内容类型](https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/)框架用于将Django模型映射到数据库表。ContentType实例通过其`app_label`和`name`引用模型：例如，DCIM应用程序中的Site模型被称为`dcim.site`。内容类型与对象的主键组合形成对象的全局唯一标识符（例如`dcim.site:123`）。

### 功能矩阵

根据其分类，每个NetBox模型可能支持不同的功能，以增强其操作。通过从指定的混合类继承，可以启用每个功能，并且一些功能还使用[应用程序注册表](./application-registry.md#model_features)。

| 功能                                                      | 功能混合器           | 注册表键       | 描述                                                                             |
|------------------------------------------------------------|-------------------------|--------------------|-----------------------------------------------------------------------------------------|
| [更改日志记录](../features/change-logging.md)            | `ChangeLoggingMixin`    | -                  | 对这些对象的更改会自动记录在更改日志中                   |
| 复制                                                    | `CloningMixin`          | -                  | 提供`clone()`方法以准备副本                                         |
| [自定义字段](../customization/custom-fields.md)         | `CustomFieldsMixin`     | `custom_fields`    | 这些模型支持添加用户定义字段                                |
| [自定义链接](../customization/custom-links.md)           | `CustomLinksMixin`      | `custom_links`     | 这些模型支持分配自定义链接                                     |
| [自定义验证](../customization/custom-validation.md) | `CustomValidationMixin` | -                  | 支持强制执行自定义验证规则                                     |
| [导出模板](../customization/export-templates.md)   | `ExportTemplatesMixin`  | `export_templates` | 用户可以为这些模型创建自定义导出模板                               |
| [作业结果](../features/background-jobs.md)              | `JobsMixin`             | `jobs`             | 用户可以为这些模型创建自定义导出模板                               |
| [记录日志](../features/journaling.md)                    | `JournalingMixin`       | `journaling`       | 这些模型支持持久性历史评论                                    |
| [同步数据](../integrations/synchronized-data.md)  | `SyncedDataMixin`       | `synced_data`      | 某些模型数据可以自动从远程数据源同步                              |
| [标签](../models/extras/tag.md)                         | `TagsMixin`             | `tags`             | 模型可以带有用户定义的标签                                         |
| [事件规则](../features/event-rules.md)                  | `EventRulesMixin`       | `event_rules`      | 事件规则可以在事件发生时自动发送Webhook或运行自定义脚本            |

## 模型索引

### 主要模型

这些被认为是用于建模网络基础设施的“核心”应用程序模型。

* [circuits.Circuit](../models/circuits/circuit.md)
* [circuits.Provider](../models/circuits/provider.md)
* [circuits.ProviderAccount](../models/circuits/provideraccount.md)
* [circuits.ProviderNetwork](../models/circuits/providernetwork.md)
* [core.DataSource](../models/core/datasource.md)
* [dcim.Cable](../models/dcim/cable.md)
* [dcim.Device](../models/dcim/device.md)
* [dcim.DeviceType](../models/dcim/devicetype.md)
* [dcim.Module](../models/dcim/module.md)
* [dcim.ModuleType](../models/dcim/moduletype.md)
* [dcim.PowerFeed](../models/dcim/powerfeed.md)
* [dcim.PowerPanel](../models/dcim/powerpanel.md)
* [dcim.Rack](../models/dcim/rack.md)
* [dcim.RackReservation](../models/dcim/rackreservation.md)
* [dcim.Site](../models/dcim/site.md)
* [dcim.VirtualChassis](../models/dcim/virtualchassis.md)
* [dcim.VirtualDeviceContext](../models/dcim/virtualdevicecontext.md)
* [ipam.Aggregate](../models/ipam/aggregate.md)
* [ipam.ASN](../models/ipam/asn.md)
* [ipam.FHRPGroup](../models/ipam/fhrpgroup.md)
* [ipam.IPAddress](../models/ipam/ipaddress.md)
* [ipam.IPRange](../models/ipam/iprange.md)
* [ipam.Prefix](../models/ipam/prefix.md)
* [ipam.RouteTarget](../models/ipam/routetarget.md)
* [ipam.Service](../models/ipam/service.md)
* [ipam.ServiceTemplate](../models/ipam/servicetemplate.md)
* [ipam.VLAN](../models/ipam/vlan.md)
* [ipam.VRF](../models/ipam/vrf.md)
* [tenancy.Contact](../models/tenancy/contact.md)
* [tenancy.Tenant](../models/tenancy/tenant.md)
* [virtualization.Cluster](../models/virtualization/cluster.md)
* [virtualization.VirtualMachine](../models/virtualization/virtualmachine.md)
* [vpn.IKEPolicy](../models/vpn/ikepolicy.md)
* [vpn.IKEProposal](../models/vpn/ikeproposal.md)
* [vpn.IPSecPolicy](../models/vpn/ipsecpolicy.md)
* [vpn.IPSecProfile](../models/vpn/ipsecprofile.md)
* [vpn.IPSecProposal](../models/vpn/ipsecproposal.md)
* [vpn.L2VPN](../models/vpn/l2vpn.md)
* [vpn.Tunnel](../models/vpn/tunnel.md)
* [wireless.WirelessLAN](../models/wireless/wirelesslan.md)
* [wireless.WirelessLink](../models/wireless/wirelesslink.md)

### 组织模型

组织模型用于组织和分类主要模型。

* [circuits.CircuitType](../models/circuits/circuittype.md)
* [dcim.DeviceRole](../models/dcim/devicerole.md)
* [dcim.Manufacturer](../models/dcim/manufacturer.md)
* [dcim.Platform](../models/dcim/platform.md)
* [dcim.RackRole](../models/dcim/rackrole.md)
* [ipam.ASNRange](../models/ipam/asnrange.md)
* [ipam.RIR](../models/ipam/rir.md)
* [ipam.Role](../models/ipam/role.md)
* [ipam.VLANGroup](../models/ipam/vlangroup.md)
* [tenancy.ContactRole](../models/tenancy/contactrole.md)
* [virtualization.ClusterGroup](../models/virtualization/clustergroup.md)
* [virtualization.ClusterType](../models/virtualization/clustertype.md)

### 嵌套组模型

嵌套组模型的行为类似于组织模型，但在递归层次结构内自我嵌套。例如，Region模型可用于表示国家、州和城市的层次结构。

* [dcim.Location](../models/dcim/location.md)（曾称为RackGroup）
* [dcim.Region](../models/dcim/region.md)
* [dcim.SiteGroup](../models/dcim/sitegroup.md)
* [tenancy.ContactGroup](../models/tenancy/contactgroup.md)
* [tenancy.TenantGroup](../models/tenancy/tenantgroup.md)
* [wireless.WirelessLANGroup](../models/wireless/wirelesslangroup.md)

### 组件模型

组件模型表示属于设备或虚拟机的单个物理或虚拟组件。

* [dcim.ConsolePort](../models/dcim/consoleport.md)
* [dcim.ConsoleServerPort](../models/dcim/consoleserverport.md)
* [dcim.DeviceBay](../models/dcim/devicebay.md)
* [dcim.FrontPort](../models/dcim/frontport.md)
* [dcim.Interface](../models/dcim/interface.md)
* [dcim.InventoryItem](../models/dcim/inventoryitem.md)
* [dcim.ModuleBay](../models/dcim/modulebay.md)
* [dcim.PowerOutlet](../models/dcim/poweroutlet.md)
* [dcim.PowerPort](../models/dcim/powerport.md)
* [dcim.RearPort](../models/dcim/rearport.md)
* [virtualization.VirtualDisk](../models/virtualization/virtualdisk.md)
* [virtualization.VMInterface](../models/virtualization/vminterface.md)

### 组件模板模型

这些模型作为模板，用于复制设备和虚拟机组件。组件模板模型支持有限的功能集，包括更改日志记录、自定义验证和事件规则。

* [dcim.ConsolePortTemplate](../models/dcim/consoleporttemplate.md)
* [dcim.ConsoleServerPortTemplate](../models/dcim/consoleserverporttemplate.md)
* [dcim.DeviceBayTemplate](../models/dcim/devicebaytemplate.md)
* [dcim.FrontPortTemplate](../models/dcim/frontporttemplate.md)
* [dcim.InterfaceTemplate](../models/dcim/interfacetemplate.md)
* [dcim.InventoryItemTemplate](../models/dcim/inventoryitemtemplate.md)
* [dcim.ModuleBayTemplate](../models/dcim/modulebaytemplate.md)
* [dcim.PowerOutletTemplate](../models/dcim/poweroutlettemplate.md)
* [dcim.PowerPortTemplate](../models/dcim/powerporttemplate.md)
* [dcim.RearPortTemplate](../models/dcim/rearporttemplate.md)

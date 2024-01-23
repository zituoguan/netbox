# 发布说明

NetBox的版本分为主要版本、次要版本和补丁版本。例如，版本3.1.0是一个次要版本，而v3.1.5是一个补丁版本。简要地描述如下：

* **主要版本** - 引入或删除整个API或其他核心功能
* **次要版本** - 实施重要的新功能，但可能对API消费者或其他集成产生破坏性变化
* **补丁版本** - 修复错误并可能引入向后兼容的增强功能的维护版本

次要版本每年的四月、八月和十二月发布。补丁版本根据需要发布，以解决错误并满足次要功能请求，通常每一到两周发布一次。

此页面包含了自NetBox v2.0以来的所有主要和次要版本的历史记录。有关特定补丁版本的更多详细信息，请查看该特定次要版本的发布说明页面。

#### [版本3.7](./version-3.7.md)（2023年12月）

* VPN隧道 ([#9816](https://github.com/netbox-community/netbox/issues/9816))
* 事件规则 ([#14132](https://github.com/netbox-community/netbox/issues/14132))
* 虚拟机磁盘 ([#8356](https://github.com/netbox-community/netbox/issues/8356))
* 对象保护规则 ([#10244](https://github.com/netbox-community/netbox/issues/10244))
* 改进的自定义字段可见性控制 ([#13299](https://github.com/netbox-community/netbox/issues/13299))
* 改进的全局搜索结果 ([#14134](https://github.com/netbox-community/netbox/issues/14134))
* 插件的表格列注册 ([#14173](https://github.com/netbox-community/netbox/issues/14173))
* 插件的数据后端注册 ([#13381](https://github.com/netbox-community/netbox/issues/13381))

#### [版本3.6](./version-3.6.md)（2023年8月）

* 重新定位的管理界面视图 ([#12589](https://github.com/netbox-community/netbox/issues/12589), [#12590](https://github.com/netbox-community/netbox/issues/12590), [#12591](https://github.com/netbox-community/netbox/issues/12591), [#13044](https://github.com/netbox-community/netbox/issues/13044))
* 可配置的默认权限 ([#13038](https://github.com/netbox-community/netbox/issues/13038))
* 用户书签 ([#8248](https://github.com/netbox-community/netbox/issues/8248))
* 自定义字段选择集 ([#12988](https://github.com/netbox-community/netbox/issues/12988))
* 自定义字段的预定义位置选择 ([#12194](https://github.com/netbox-community/netbox/issues/12194))
* 通过对象类型限制标签使用 ([#11541](https://github.com/netbox-community/netbox/issues/11541))

#### [版本3.5](./version-3.5.md)（2023年4月）

* 可定制的仪表板 ([#9416](https://github.com/netbox-community/netbox/issues/9416))
* 远程数据源 ([#11558](https://github.com/netbox-community/netbox/issues/11558))
* 配置模板渲染 ([#11559](https://github.com/netbox-community/netbox/issues/11559))
* NAPALM集成插件 ([#10520](https://github.com/netbox-community/netbox/issues/10520))
* ASN范围 ([#8550](https://github.com/netbox-community/netbox/issues/8550))
* 提供商帐户 ([#9047](https://github.com/netbox-community/netbox/issues/9047))
* 作业触发的Webhooks  ([#8958](https://github.com/netbox-community/netbox/issues/8958))

#### [版本3.4](./version-3.4.md)（2022年12月）

* 新的全局搜索 ([#10560](https://github.com/netbox-community/netbox/issues/10560))
* 虚拟设备上下文 ([#7854](https://github.com/netbox-community/netbox/issues/7854))
* 保存的过滤器 ([#9623](https://github.com/netbox-community/netbox/issues/9623))
* JSON/YAML批量导入 ([#4347](https://github.com/netbox-community/netbox/issues/4347))
* 通过批量导入更新现有对象 ([#7961](https://github.com/netbox-community/netbox/issues/7961))
* 计划报告和脚本 ([#8366](https://github.com/netbox-community/netbox/issues/8366))
* 用于插件的暂存更改的API ([#10851](https://github.com/netbox-community/netbox/issues/10851))

#### [版本3.3](./version-3.3.md)（2022年8月）

* 多对象电缆终端 ([#9102](https://github.com/netbox-community/netbox/issues/9102))
* L2VPN建模 ([#8157](https://github.com/netbox-community/netbox/issues/8157))
* PoE接口属性 ([#1099](https://github.com/netbox-community/netbox/issues/1099))
* 半高机架单元 ([#51](https://github.com/netbox-community/netbox/issues/51))
* 通过客户端IP限制API令牌 ([#8233](https://github.com/netbox-community/netbox/issues/8233))
* 在权限约束中引用用户 ([#9074](https://github.com/netbox-community/netbox/issues/9074))
* 自定义字段分组 ([#8495](https://github.com/netbox-community/netbox/issues/8495))
* 切换自定义字段可见性 ([#9166](https://github.com/netbox-community/netbox/issues/9166))

#### [版本3.2](./version-3.2.md)（2022年4月）

* 插件框架扩展 ([#8333](https://github.com/netbox-community/netbox/issues/8333))
* 模块和模块类型 ([#7844](https://github.com/netbox-community/netbox/issues/7844))
* 自定义对象字段 ([#7006](https://github.com/netbox-community/netbox/issues

/7006))
* 自定义状态选择项 ([#8054](https://github.com/netbox-community/netbox/issues/8054))
* 改进的用户首选项 ([#7759](https://github.com/netbox-community/netbox/issues/7759))
* 库存项目角色 ([#3087](https://github.com/netbox-community/netbox/issues/3087))
* 库存项目模板 ([#8118](https://github.com/netbox-community/netbox/issues/8118))
* 服务模板 ([#1591](https://github.com/netbox-community/netbox/issues/1591))
* 自动分配下一个可用的VLAN的API ([#2658](https://github.com/netbox-community/netbox/issues/2658))

#### [版本3.1](./version-3.1.md)（2021年12月）

* 联系对象 ([#1344](https://github.com/netbox-community/netbox/issues/1344))
* 无线网络 ([#3979](https://github.com/netbox-community/netbox/issues/3979))
* 动态配置更新 ([#5883](https://github.com/netbox-community/netbox/issues/5883))
* 第一跳冗余协议 (FHRP) 组 ([#6235](https://github.com/netbox-community/netbox/issues/6235))
* 条件Webhooks ([#6238](https://github.com/netbox-community/netbox/issues/6238))
* 接口桥接 ([#6346](https://github.com/netbox-community/netbox/issues/6346))
* 单个站点的多个ASN ([#6732](https://github.com/netbox-community/netbox/issues/6732))
* 单一登录（SSO）认证 ([#7649](https://github.com/netbox-community/netbox/issues/7649))

#### [版本3.0](./version-3.0.md)（2021年8月）

* 更新的用户界面 ([#5893](https://github.com/netbox-community/netbox/issues/5893))
* GraphQL API ([#2007](https://github.com/netbox-community/netbox/issues/2007))
* IP范围 ([#834](https://github.com/netbox-community/netbox/issues/834))
* 自定义模型验证 ([#5963](https://github.com/netbox-community/netbox/issues/5963))
* SVG电缆追踪 ([#6000](https://github.com/netbox-community/netbox/issues/6000))
* 以前在管理UI下的模型的新视图 ([#6466](https://github.com/netbox-community/netbox/issues/6466))
* REST API令牌提供 ([#5264](https://github.com/netbox-community/netbox/issues/5264))
* 新的清理命令 ([#6590](https://github.com/netbox-community/netbox/issues/6590))
* 用于插件的自定义队列支持 ([#6651](https://github.com/netbox-community/netbox/issues/6651))

#### [版本2.11](./version-2.11.md)（2021年4月）

* 日志支持 ([#151](https://github.com/netbox-community/netbox/issues/151))
* 父接口分配 ([#1519](https://github.com/netbox-community/netbox/issues/1519))
* Webhooks中的预更改和后更改快照 ([#3451](https://github.com/netbox-community/netbox/issues/3451))
* 没有电缆的情况下标记为连接 ([#3648](https://github.com/netbox-community/netbox/issues/3648))
* 允许将设备分配给位置 ([#4971](https://github.com/netbox-community/netbox/issues/4971))
* 动态对象导出 ([#4999](https://github.com/netbox-community/netbox/issues/4999))
* VLAN组的变量范围支持 ([#5284](https://github.com/netbox-community/netbox/issues/5284))
* 新的站点组模型 ([#5892](https://github.com/netbox-community/netbox/issues/5892))
* 改进的更改日志记录 ([#5913](https://github.com/netbox-community/netbox/issues/5913))
* 提供商网络建模 ([#5986](https://github.com/netbox-community/netbox/issues/5986))

#### [版本2.10](./version-2.10.md)（2020年12月）

* 路由目标 ([#259](https://github.com/netbox-community/netbox/issues/259))
* REST API批量删除 ([#3436](https://github.com/netbox-community/netbox/issues/3436))
* REST API批量更新 ([#4882](https://github.com/netbox-community/netbox/issues/4882))
* 自定义字段的重新实现 ([#4878](https://github.com/netbox-community/netbox/issues/4878))
* 电缆追踪性能改进 ([#4900](https://github.com/netbox-community/netbox/issues/4900))

#### [版本2.9](./version-2.9.md)（2020年8月）

* 基于对象的权限 ([#554](https://github.com/netbox-community/netbox/issues/554))
* 脚本和报告的后台执行 ([#2006](https://github.com/netbox-community/netbox/issues/2006))
* 命名的虚拟机箱 ([#2018](https://github.com/netbox-community/netbox/issues/2018))
* 标签创建的更改 ([#3703](https://github.com/netbox-community/netbox/issues/3703))
* VM接口的专用模型 ([#4721](https://github.com/netbox-community/netbox/issues/4721))
* 用户和组的REST API端点 ([#4877](https://github.com/netbox-community/netbox/issues/4877))

#### [版本2.8](./version-2.8.md)（2020年4月）

* 远程认证支持 ([#2328](https://github.com/netbox-community/netbox/issues/2328))
* 插件 ([#3351](https://github.com/netbox-community/netbox/issues/3351))

#### [版本2.7](./version-2.7.md)（2020年1月）

* 增强的设备类型导入 ([#451](https://github.com/netbox-community/netbox/issues/451))
* 设备组件的批量导入 ([#822](https://github.com/netbox-community/netbox/issues/822))
* 外部文件存储 ([#1814](https://github.com/netbox-community/netbox/issues/1814))
* 机架图通过SVG渲染 ([#2248](https://github.com/netbox-community/netbox/issues/2248))

#### [版本2.6](./version-2.6.md)（2019年6月）

* 电源面板和供电线路 ([#54](https://github.com/netbox-community/netbox/issues/54))
* 缓存 ([#2647](https://github.com/netbox-community/netbox/issues/2647))
* 视图权限 ([#323](https://github.com/netbox-community/netbox/issues/323))
* 自定义链接 ([#969](https://github.com/netbox-community/netbox/issues/969))
* Prometheus度量数据 ([#3104](https://github.com/netbox-community/netbox/issues/3104))

#### [版本2.5](./version-2.5.md)（2018年12月）

* 补丁面板和电缆 ([#20](https://github.com/netbox-community/netbox/issues/20))

#### [版本2.4](./version-2.4.md)（2018年8月）

* Webhooks ([#81](https://github.com/netbox-community/netbox/issues/81))
* 标签 ([#132](https://github.com/netbox-community/netbox/issues/132))
* 上下文配置数据 ([#1349](https://github.com/netbox-community/netbox/issues/1349))
* 变更日志 ([#1898](https://github.com/netbox-community/netbox/issues/1898))

#### [版本2.3](./version-2.3.md)（2018年2月）

* 虚拟机箱 ([#99](https://github.com/netbox-community/netbox/issues/99))
* 接口VLAN分配 ([#150](https://github.com/netbox-community/netbox/issues/150))
* 通过API批量创建对象 ([#1553](https://github.com/netbox-community/netbox/issues/1553))
* 自动分配下一个可用前缀 ([#1694](https://github.com/netbox-community/netbox/issues/1694))
* 设备/VM组件的批量重命名 ([#1781](https://github.com/netbox-community/netbox/issues/1781))

#### [版本2.2](./version-2.2.md)（2017年10月）

* 虚拟机和集群 ([#142](https://github.com/netbox-community/netbox/issues/142))
* 自定义验证报告 ([#1511](https://github.com/netbox-community/netbox/issues/1511))

#### [版本2.1](./version-2.1.md)（2017年7月）

* IP地址角色 ([#819](https://github.com/netbox-community/netbox/issues/819))
* 自动分配下一个可用IP地址 ([#1246](https://github.com/netbox-community/netbox/issues/1246))
* NAPALM集成 ([#1348](https://github.com/netbox-community/netbox/issues/1348))

#### [版本2.0](./version-2.0.md)（2017年5月）

* API 2.0 ([#113](https://github.com/netbox-community/netbox/issues/113))
* 图片附件 ([#152](https://github.com/netbox-community/netbox/issues/152))
* 全局搜索 ([#159](https://github.com/netbox-community/netbox/issues/159))
* 机架图视图 ([#951](https://github.com/netbox-community/netbox/issues/951))

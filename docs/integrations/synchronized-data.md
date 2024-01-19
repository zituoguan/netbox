# 同步数据

某些NetBox模型支持从远程[数据源](../models/core/datasource.md)自动同步特定属性，例如托管在GitHub或GitLab上的git仓库。来自权威远程源的数据在NetBox中作为[数据文件](../models/core/datafile.md)同步到本地。

!!! 注意 "权限"
    用户必须被分配`core.sync_datasource`权限，以便从远程数据源同步本地文件。这可以通过为“Core > 数据源”对象类型创建一个包含`sync`操作的权限并将其分配给所需的用户和/或组来实现。

以下功能支持使用同步数据：

* [配置模板](../features/configuration-rendering.md)
* [配置上下文数据](../features/context-data.md)
* [导出模板](../customization/export-templates.md)

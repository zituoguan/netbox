# 同步数据

NetBox中的几个模型支持从指定的远程源自动同步本地数据。例如，在NetBox中定义的[配置模板](./configuration-rendering.md)可以从存储在远程git存储库中的文本文件中获取其内容。这是通过使用核心[data source](../models/core/datasource.md)和[data file](../models/core/datafile.md)模型来实现的。

要启用远程数据同步，NetBox管理员首先指定一个或多个远程数据源。NetBox目前支持以下来源类型：

* Git存储库
* Amazon S3存储桶（或兼容的产品）
* 本地磁盘路径

（在这种情况下，本地磁盘路径被视为“远程”，因为它们存在于NetBox的数据库之外。这些路径也可以映射到外部网络共享。）

!!! info
    连接到外部源的数据后端通常需要安装一个或多个支持Python库。Git后端需要[`dulwich`](https://www.dulwich.io/)包，S3后端需要[`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)包。必须在NetBox的环境中安装这些后端才能启用它们。

每种远程源类型都有其自己的配置参数。例如，git源会要求用户指定分支和身份验证凭据。一旦创建了源，将运行同步作业，以自动复制远程文件到本地数据库中。

以下NetBox模型可以与复制的数据文件关联：

* 配置上下文
* 配置模板
* 导出模板

一旦将数据指定为本地实例，其数据将被替换为复制文件的内容。当将来更新复制文件（通过同步作业）时，本地实例将被标记为具有过时数据。然后，用户可以单独或批量同步这些对象以实现更新。这个两阶段的过程确保了自动同步任务不会立即影响生产数据。

!!! 注意 "权限"
    用户必须被分配`core.sync_datasource`权限，才能从远程数据源同步本地文件。
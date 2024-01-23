# 发布检查清单

此文档描述了打包和发布新的NetBox版本的流程。有三种类型的发布：

* 主要版本发布（例如，从v2.11到v3.0）
* 次要版本发布（例如，从v3.2到v3.3）
* 补丁版本发布（例如，从v3.3.0到v3.3.1）

尽管主要版本发布通常引入了一些对应用程序的非常重大的更改，但它们通常在发布打包的目的上与次要版本增量相同对待。

## 次要版本发布

### 处理受限制的依赖项

有时需要将依赖项限制到特定版本，例如，以解决较新版本中的错误或避免我们尚未适应的破坏性更改。 （另一个常见示例是限制上游的Django版本。）例如：

```
# https://github.com/encode/django-rest-framework/issues/6053
djangorestframework==3.8.1
```

这些版本约束被添加到`base_requirements.txt`，以确保在更新`requirements.txt`中的固定依赖项时不会安装更新的软件包（请参阅下面的[更新要求](#更新要求)部分）。在每个新的NetBox次要版本发布之前，应该尽可能解决所有这些对依赖包的约束。这可以防止随着时间的推移收集过时的约束。

### 关闭发布里程碑

在确保与之相关联的问题没有保留的情况下，在GitHub上关闭[发布里程碑](https://github.com/netbox-community/netbox/milestones)。

### 更新发布说明

检查新版本的发布说明链接是否在导航菜单中（在`mkdocs.yml`中定义），并确保已在`docs/index.md`中添加了所有主要新功能的摘要。

### 手动执行新安装

启动文档服务器，并导航到当前版本的安装文档：

```no-highlight
mkdocs serve
```

按照这些说明在临时环境中执行NetBox的新安装。此过程不得自动化：此步骤的目标是捕获文档中的任何错误或遗漏，并确保它针对每个发布保持最新。在继续发布之前，对文档进行任何必要的更改。

### 合并发布分支

提交拉取请求，将`feature`分支合并到`develop`分支，以准备发布。一旦合并完成，继续下面的补丁版本发布部分。

### 重建演示数据（发布后）

在发布新的次要版本之后，生成与新版本兼容的新演示数据快照。请参阅[`netbox-demo-data`](https://github.com/netbox-community/netbox-demo-data)存储库中的说明。

---

## 补丁版本发布

### 通知netbox-docker项目有关的更改

通知[`netbox-docker`](https://github.com/netbox-community/netbox-docker)的维护者（在**#netbox-docker**中），任何可能与其构建过程相关的更改，包括：

* 对`upgrade.sh`的重大更改
* 服务依赖项（PostgreSQL、Redis等）的最低版本的提高
* 对参考安装的任何更改

### 更新要求

在每次发布之前，将NetBox的每个Python依赖项更新到其最新稳定版本。这些依赖项在`requirements.txt`中定义，使用`pip`从`base_requirements.txt`中更新。要执行此操作，请执行以下步骤：

1. 升级环境中所有必需包的安装版本（`pip install -U -r base_requirements.txt`）。
2. 运行所有测试，并检查UI和API是否按预期运行。
3. 检查每个要求的发行说明，以查看是否有任何重大的破坏性或值得注意的更改。
4. 根据需要更新`requirements.txt`中的软件包版本。

在将依赖项升级到其最新版本会导致问题的情况下，应该在`base_requirements.txt`中将其限制为当前次要版本，并附带说明性注释，然后在下一个主要NetBox版本发布时重新审查（请参阅上面的[处理受限制的依赖项](#处理受限制的依赖项)部分）。

### 重建设备类型定义模式

运行以下命令以更新设备类型定义验证模式：

```nohighlight
./manage.py buildschema --write
```

这将自动更新`contrib/generated_schema.json`中的模式文件。

### 更新版本和更改日志

* 将`settings.py`中的`VERSION`常量更新为新的发布版本。
* 在`.github/ISSUE_TEMPLATES/`下的功能请求和错误报告模板中更新示例版本号。
* 用当前日期替换发布说明中的"FUTURE"占位符。

提交这些更改到`develop`分支，并将其推送到上游。

### 验证CI构建状态

确保`develop`分支上的持续集成测试已成功完成。如果失败，请采取措施纠正失败，然后继续发布。

### 提交拉取请求

提交一个拉取请求，标题为**"发布 vX.Y.Z"**，以将`develop`分支合并到`master`分支。将记录的发布说明复制到拉取请求的正文中。

一旦PR的CI完成，合并它。这将在`master`分支中发布一个新版本。

### 创建新发布

在GitHub上创建一个[新的发布](https://github.com/netbox-community/netbox/releases/new)，具有以下参数。

* **标签：** 当前版本（例如`v3.3.1`）
* **目标：** `master`
* **标题：** 版本和日期（例如`v3.3.1 - 2022-08-25`）
* **描述：** 从拉取请求正文复制

一旦创建，发布将可供用户安装。

### 更新开发版本

在`develop`分支上，将`settings.py`中的`VERSION`更新为下一个版本。例如，如果刚刚发布了v3.3.1，则设置为：

```
VERSION = 'v3.3.2-dev'
```

使用"PRVB"（代表_发布后版本提升_）的注释提交此更改，并将提交推送到上游。

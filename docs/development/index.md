# NetBox开发

感谢您对贡献NetBox的兴趣！本介绍将覆盖在您开始之前需要了解的一些重要事项。

## 代码

NetBox及其许多相关项目都在[GitHub](https://github.com/netbox-community/netbox)上维护。GitHub还是我们的主要讨论论坛之一。虽然所有代码和讨论都是公开可访问的，但您需要[注册一个免费的GitHub帐户](https://github.com/signup)以参与其中。大多数人通常会在自己的GitHub帐户下[fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) NetBox存储库以开始处理代码。

![GitHub](../media/development/github.png)

存储库中有三个永久分支：

- `master` - 当前稳定版本。个别更改永远不应直接推送到此分支，而应从`develop`合并。
- `develop` - 即将发布的补丁版本的活跃开发分支。拉取请求通常应基于此分支，除非它们引入必须推迟到下一个次要版本的破坏性更改。
- `feature` - 下一个次要版本中要引入的新功能工作（例如从v3.3到v3.4）。

NetBox组件被分成Django应用程序。每个应用程序包含与特定功能相关的模型、视图和其他资源：

- `circuits`：通信电路和供应商（不要与电力电路混淆）
- `dcim`：数据中心基础设施管理（站点、机架和设备）
- `extras`：不被视为核心数据模型的其他功能
- `ipam`：IP地址管理（VRF、前缀、IP地址和VLAN）
- `tenancy`：可以分配给NetBox对象的租户（例如客户）
- `users`：认证和用户首选项
- `utilities`：不面向用户的资源（可扩展的类等）
- `virtualization`：虚拟机和集群
- `wireless`：无线链接和局域网

所有核心功能都存储在`netbox/`子目录中。HTML模板存储在公共`templates/`目录中，具有特定于模型和视图的模板按应用程序排列。文档保存在`docs/`根目录中。

## 提出更改

所有对代码库进行的重大更改都使用[GitHub问题](https://docs.github.com/en/issues)进行跟踪。功能请求、错误报告和类似的提议都必须作为问题进行记录并经过维护人员批准，然后才能开始工作。这确保了对代码库的所有更改都得到了适当的文档记录以供将来参考。

要为NetBox提交新的功能请求或错误报告，请选择并完成适当的[问题模板](https://github.com/netbox-community/netbox/issues/new/choose)。一旦您的问题被批准，您就可以提交一个包含您提议更改的[拉取请求](https://docs.github.com/en/pull-requests)。

![打开新的GitHub问题](../media/development/github_new_issue.png)

查看我们的[问题接受政策](https://github.com/netbox-community/netbox/wiki/Issue-Intake-Policy)以了解问题分类和批准流程的概述。

!!! 提示
    请避免在提案被接受之前开始工作。并非所有提议的更改都会被接受，我们不希望您浪费时间在可能不会进入项目的代码上。

## 获取帮助

有两个主要的论坛可用于获取关于NetBox开发的帮助：

- [GitHub讨论](https://github.com/netbox-community/netbox/discussions) - 用于一般讨论和支持问题的首选论坛。在提交问题之前，理想的方式是先形成一个功能请求的形状。
- [NetDev社区Slack上的＃netbox](https://netdev.chat/) - 适用于快速聊天。避免任何可能需要稍后引用的讨论，因为聊天历史不会无限期保留。

!!! 注意
    不要使用GitHub问题寻求帮助：这些问题仅保留用于提出的代码更改。

## 治理

NetBox遵循[仁慈的独裁者](http://oss-watch.ac.uk/resources/benevolentdictatorgovernancemodel)治理模型，由[Jeremy Stretch](https://github.com/jeremystretch)负责对代码库进行的所有更改。虽然欢迎和鼓励社区的贡献，但首席维护人员的主要职责是确保项目的长期可维护性并继续专注于其主要功能。

## 许可证

整个NetBox项目都根据[Apache 2.0许可证](https://github.com/netbox-community/netbox/blob/master/LICENSE.txt)开源许可。这是一种非常宽松的许可证，允许在项目中无限制地重新分发所有代码。请注意，对项目的所有提交都受到相同的许可证的约束。

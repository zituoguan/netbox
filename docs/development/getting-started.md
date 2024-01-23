# 开始

## 设置开发环境

开始使用NetBox开发非常简单，并且对于有Django开发经验的人来说应该感到非常熟悉。您需要一些东西：

* 一个Linux系统或兼容的环境
* 一个PostgreSQL服务器，可以按照[文档](../installation/1-postgresql.md)在本地安装
* 一个Redis服务器，也可以[在本地安装](../installation/2-redis.md)
* Python 3.8或更高版本

### 1. Fork仓库

假设您将在自己的分支上工作，第一步是fork [官方git仓库](https://github.com/netbox-community/netbox)。 （如果您是将要直接与官方仓库一起工作的维护者，请跳过此步骤。）单击右上角的“fork”按钮（确保您已先登录GitHub）。

![GitHub fork按钮](../media/development/github_fork_button.png)

复制对话框中提供的URL。

![GitHub fork对话框](../media/development/github_fork_dialog.png)

然后，您可以将GitHub分支克隆到本地进行开发：

```no-highlight hl_lines="1 9"
$ git clone https://github.com/$username/netbox.git
Cloning into 'netbox'...
remote: Enumerating objects: 85949, done.
remote: Counting objects: 100% (4672/4672), done.
remote: Compressing objects: 100% (1224/1224), done.
remote: Total 85949 (delta 3538), reused 4332 (delta 3438), pack-reused 81277
Receiving objects: 100% (85949/85949), 55.16 MiB | 44.90 MiB/s, done.
Resolving deltas: 100% (68008/68008), done.
$ ls netbox/
base_requirements.txt  contrib          docs         mkdocs.yml  NOTICE     requirements.txt  upgrade.sh
CHANGELOG.md           CONTRIBUTING.md  LICENSE.txt  netbox      README.md  scripts
```

### 2. 创建新分支

NetBox项目使用三个持久性git分支来跟踪工作：

* `master` - 用作当前稳定版本的快照
* `develop` - 所有即将发布的稳定（补丁）版本的开发工作都在这里进行
* `feature` - 跟踪即将发布的次要版本的工作

通常情况下，您将基于`develop`分支创建拉取请求，或者如果要在新的主要版本上工作，则基于`feature`分支创建。例如，假设当前的NetBox版本是v3.3.5。应用到`develop`分支的工作将出现在v3.3.6中，而在`feature`分支下进行的工作将包含在下一个次要版本（v3.4.0）中。

!!! warning
    **绝不要**将拉取请求合并到`master`分支：此分支仅合并来自`develop`分支的拉取请求，以实现新版本发布。

要创建新分支，请首先确保您已经检出了所需的基础分支，然后运行：

```no-highlight
git checkout -B $branchname
```

在命名新的git分支时，强烈建议贡献者使用相关问题号后面跟一个非常简短的工作描述：

```no-highlight
$issue-$description
```

描述应该只是两到三个单词，以暗示正在执行的工作的重点。例如，修复TypeError异常的bug＃1234在创建设备时可能被命名为`1234-device-typerror`。这样确保分支总是按照某种逻辑顺序（例如，运行`git branch -a`时）并帮助其他开发人员快速识别每个分支的目的。

### 3. 启用Pre-Commit钩子

NetBox附带了一个[git pre-commit钩子](https://githooks.com/)脚本，它会在提交更改之前自动检查样式合规性和缺少的数据库迁移。这有助于避免提交错误，导致CI测试失败。建议您通过创建一个链接到`scripts/git-hooks/pre-commit`来启用它：

```no-highlight
cd .git/hooks/
ln -s ../../scripts/git-hooks/pre-commit
```
为了使pre-commit钩子工作，您还需要安装pycodestyle包：

```no-highlight
python -m pip install pycodestyle
```
...并按照[Web UI开发指南](web-ui.md)中显示的方式设置yarn包。

### 4. 创建Python虚拟环境

[虚拟环境](https://docs.python.org/3/tutorial/venv.html)（简称“venv”）类似于一组Python包的容器。这些允许您构建适合特定项目的环境，而不会干扰系统包或其他项目。在安装时，NetBox在生产中使用虚拟环境。

使用`venv` Python模块创建一个虚拟环境：

```no-highlight
mkdir ~/.venv
python3 -m venv ~/.venv/netbox
```

这将在您的主目录中创建一个名为`.venv/netbox/`的目录，其中包含Python可执行文件的虚拟副本及其相关的库和工具。在开发过程中运行NetBox时，将使用`~/.venv/netbox/bin/python`的Python二进制文件。

!!! tip "虚拟环境"
    将虚拟环境保留在`~/.venv/`中是一个常见的约定，但完全是可选的：虚拟环境可以几乎放在您喜欢的任何地方。还考虑使用[`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/en/stable/)来简化多个环境的管理。

创建虚拟环境后，请激活虚拟环境：

```no-highlight
source ~/.venv/netbox/bin/activate
```

请注意，控制台提示会更改以指示活动环境。这会更新必要的系统环境变量，以确保任何Python脚本都在虚拟环境内运行。

### 5. 安装所需的包

在激活虚拟环境后，使用`pip`模块安装项目所需的Python包。所需的包在`requirements.txt`中定义。该文件中的每一行都指定了所需包的名称和特定版本。

```no-highlight
python -m pip install -r requirements.txt
```

### 6. 配置NetBox

在`netbox/netbox/`目录中，将`configuration_example.py`复制到`configuration.py`并更新以下参数：

* `ALLOWED_HOSTS`：这可以设置为`['*']`以进行开发目的
* `DATABASE`：PostgreSQL数据库连接参数
* `REDIS`：Redis配置（如果与默认值不同）
* `SECRET_KEY`：设置为随机字符串（使用父目录中的`generate_secret_key.py`生成合适的密钥）
* `DEBUG`：设置为`True`
* `DEVELOPER`：设置为`True`（这将启用新的数据库迁移的创建）

### 7. 启动开发服务器

Django提供了一个轻量级的、自动更新的[HTTP/WSGI服务器](https://docs.djangoproject.com/en/stable/ref/django-admin/#runserver)用于开发使用。它使用`runserver`管理命令启动：

```no-highlight hl_lines="1"
$ ./manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
August 18, 2022 - 15:17:52
Django version 4.0.7, using settings 'netbox.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

这确保您的开发环境现在已经完整且可操作。开发服务器将监视开发环境并在进行任何更改时自动重新加载。

!!! tip "IDE集成"
    一些IDE，例如[PyCharm](https://www.jetbrains.com/pycharm/)（强烈推荐使用），将与Django的开发服务器集成在一起，并允许您在IDE内部直接运行它。这是非常方便的，因为它可以创建一个更加方便的开发环境。

## UI开发

对于UI开发，您需要查看[Web UI开发指南](web-ui.md)

## 填充演示数据

一旦您的开发环境正常运行，最好填充一些“虚拟”数据，以使与UI和API的交互更加方便。在GitHub上查看[netbox-demo-data](https://github.com/netbox-community/netbox-demo-data)仓库，该仓库包含可以轻松导入到任何新的NetBox部署中的示例数据集合。 （此示例数据用于填充<https://demo.netbox.dev>上的公共演示实例。）

演示数据以JSON格式提供，并使用Django的`loaddata`管理命令加载到空数据库中。有关如何填充数据的完整说明，请查阅演示数据仓库的`README`文件。

## 运行测试

在提交任何重大更改到代码库之前，请确保运行NetBox的测试套件以捕获潜在的错误。测试使用`test`管理命令运行，该命令使用Python的[`unittest`](https://docs.python.org/3/library/unittest.html#module-unittest)库。请确保在运行此命令之前激活Python虚拟环境。还要记住，这些命令是在`netbox/`目录中执行的，而不是存储库的根目录。

为了避免与本地配置文件可能出现的问题，请设置`NETBOX_CONFIGURATION`以指向打包的测试配置文件`netbox/configuration_testing.py`。这将处理诸如确保虚拟插件启用以进行全面测试等问题。

```no-highlight
export NETBOX_CONFIGURATION=netbox.configuration_testing
cd netbox/
python manage.py test
```

在您没有对数据库模式进行更改的情况下（这是典型情况），您可以在此命令后附加`--keepdb`参数，以便在运行之间重用测试数据库。这可以减少运行测试套件所需的时间，因为无需每次重新构建数据库。（请注意，如果您在上一次测试运行后修改了任何模型字段，此参数将导致错误。）

```no-highlight
python manage.py test --keepdb
```

您还可以通过使用`--parallel`标志启用并行测试执行来减少测试时间。 （默认情况下，这将运行与处理器数量相同的并行测试。为了避免运行缓慢，最好指定较低数量的并行测试。）此标志可以与`--keepdb`结合使用，尽管如果遇到任何奇怪的错误，请尝试禁用并行化后再次运行测试套件。

```no-highlight
python manage.py test --parallel <n>
```

最后，可以通过指定其Python路径来限制运行特定一组测试的运行。例如，仅运行IPAM和DCIM视图测试：

```no-highlight
python manage.py test dcim.tests.test_views ipam.tests.test_views
```

这对于只有少数测试失败并且您希望单独重新运行它们的情况非常方便。

!!! info
    NetBox使用[django-rich](https://github.com/adamchainz/django-rich)来增强Django的默认`test`管理命令。

## 提交拉取请求

一旦您满意您的工作并验证所有测试都通过，就可以提交您的更改并将其推送到您的分支。请始终提供描述性（但不要过于冗长）的提交消息。确保在提交消息前缀中使用单词“Fixes”或“Closes”以及相关的问题编号（带有井号）。这告诉GitHub在合并提交后自动关闭引用的问题。

```no-highlight
git commit -m "Closes #1234: Add IPv5 support"
git push origin
```

一旦您的分支具有新的提交，就可以提交[pull request](https://github.com/netbox-community/netbox/compare)到NetBox仓库以提出更改。请确保提供详细的更改说明以及进行更改的原因。

一旦提交，维护者将审查您的拉取请求并将其合并或请求更改。如果需要更改，您可以通过向您的分支提交新的提交来进行更改：拉取请求将自动更新。

!!! warning
    请记住，只有**已接受**的问题才允许拉取请求。如果您想要处理的问题尚未被维护者批准，最好避免冒险浪费时间和精力在可能不被接受的更改上。（唯一的例外是对文档或其他非关键资源的微不足道的更改。）

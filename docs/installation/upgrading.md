# 升级到新的NetBox版本

将NetBox升级到新版本通常很简单，但用户在开始升级前务必仔细查看发布说明并备份当前部署。

通常情况下，NetBox可以直接升级到任何更新版本，但唯一的例外是增加主版本号。只能从当前主版本的最新_次要_版本升级到新主版本。例如，NetBox v2.11.8可以按照下面的步骤升级到版本3.3.2。但是，NetBox v2.10.10或更早的版本必须首先升级到任何v2.11版本，然后再升级到任何v3.x版本。（这是为了适应由主版本更改引发的数据库模式迁移的合并）。

[![升级路径](../media/installation/upgrade_paths.png)](../media/installation/upgrade_paths.png)

!!! 警告 "执行备份操作"
在开始升级过程之前，请务必保存当前NetBox部署的备份。

## 1. 查看发布说明

在升级NetBox实例之前，务必仔细查看自当前版本发布以来已发布的所有[发布说明](../release-notes/index.md)。尽管升级过程通常不涉及其他工作，但某些版本可能引入了破坏性或不兼容的更改。这些在发布说明中在生效的版本下会有特别标明。

## 2. 更新依赖项到所需版本

NetBox需要以下依赖项：

| 依赖项     | 最低版本     |
|------------|--------------|
| Python     | 3.8           |
| PostgreSQL | 12           |
| Redis      | 4.0           |

## 3. 安装最新版本

与初始安装一样，您可以通过下载最新的发布包或克隆git存储库的`master`分支来升级NetBox。

!!! 警告
    使用与初始安装NetBox相同的方法

如果不确定NetBox是如何最初安装的，请使用以下命令检查：

```shell
ls -ld /opt/netbox /opt/netbox/.git
```

如果NetBox是从发布包安装的，那么`/opt/netbox`将是一个符号链接，指向当前版本，并且`/opt/netbox/.git`不存在。如果它是从git安装的，则`/opt/netbox`和`/opt/netbox/.git`都将存在作为正常的目录。

### 选项A：下载发布版

从GitHub下载[最新的稳定发布版](https://github.com/netbox-community/netbox/releases)作为tarball或ZIP归档文件。将其解压缩到所需路径。在此示例中，我们将使用`/opt/netbox`。

下载并提取最新版本：

```no-highlight
# 将$NEWVER设置为要安装的NetBox版本
NEWVER=3.5.0
wget https://github.com/netbox-community/netbox/archive/v$NEWVER.tar.gz
sudo tar -xzf v$NEWVER.tar.gz -C /opt
sudo ln -sfn /opt/netbox-$NEWVER/ /opt/netbox
```

从当前安装中复制`local_requirements.txt`，`configuration.py`和`ldap_config.py`（如果存在）到新版本：

```no-highlight
# 将$OLDVER设置为当前安装的NetBox版本
OLDVER=3.4.9
sudo cp /opt/netbox-$OLDVER/local_requirements.txt /opt/netbox/
sudo cp /opt/netbox-$OLDVER/netbox/netbox/configuration.py /opt/netbox/netbox/netbox/
sudo cp /opt/netbox-$OLDVER/netbox/netbox/ldap_config.py /opt/netbox/netbox/netbox/
```

确保复制您上传的媒体。 （确切的操作取决于您选择存储媒体的位置，但通常情况下，移动或复制媒体目录就足够了。）

```no-highlight
sudo cp -pr /opt/netbox-$OLDVER/netbox/media/ /opt/netbox/netbox/
```

还要确保复制或链接任何自定义脚本和报告。请注意，如果这些文件存储在项目根目录之外，您将不需要复制它们。（如果不确定，请检查上面的配置文件中的`SCRIPTS_ROOT`和`REPORTS_ROOT`参数。）

```no-highlight
sudo cp -r /opt/netbox-$OLDVER/netbox/scripts /opt/netbox/netbox/
sudo cp -r /opt/netbox-$OLDVER/netbox/reports /opt/netbox/netbox/
```

如果您按照原始安装指南设置了gunicorn，请确保复制其配置：

```no-highlight
sudo cp /opt/netbox-$OLDVER/gunicorn.py /opt/netbox/
```

### 选项B：克隆Git存储库

本指南假设NetBox安装在`/opt/netbox`。拉取`master`分支的最新迭代：

```no-highlight
cd /opt/netbox
sudo git checkout master
sudo git pull origin master
```

!!! 信息 "检出旧版本"
    如果需要升级到旧版本而不是当前的稳定版本，则可以检出任何有效的[git标签](https://github.com/netbox-community/netbox/tags)，每个标签都代表一个发布版本。例如，要检出NetBox v2.11.11的代码，请执行以下操作：

        sudo git checkout v2.11.11

## 4. 运行升级脚本

一旦新代码准备就绪，请验证您的部署所需的任何可选Python包（例如`django-auth-ldap`）是否在`local_requirements.txt`中列出。然后运行升级脚本：

```no-highlight
sudo ./upgrade.sh
```

!!! 警告
    如果默认版本的Python不至少为3.8，则需要在调用升级脚本时将支持的Python版本的路径作为环境变量传递。例如：

    ```no-highlight
    sudo PYTHON=/usr/bin/python3.8 ./upgrade.sh
    ```

此脚本执行以下操作：

* 销毁并重建Python虚拟环境
* 安装`requirements.txt`中列出的所有所需的Python包
* 安装`local_requirements.txt`中的任何附加包
* 应用包含在发布版中的任何数据库迁移
* 本地生成文档（供离线使用）
* 收集要由HTTP服务提供的所有静态文件
* 从数据库中删除陈旧的内容类型
* 从数据库中删除所有已过期的用户会话

!!! 注意
    如果升级脚本提示关于未反映的数据库迁移的警告，这表示对本地代码库进行了某些更改，应予调查。除非有意修改数据库模式，否则永远不要尝试创建新的迁移。

## 5. 重启NetBox服务

!!! 警告
    如果从不使用Python虚拟环境的安装升级（即v2.7.9之前的任何版本），则需要在重启服务之前更新systemd服务文件，以引用新的Python和gunicorn可执行文件。这些文件位于`/opt/netbox/venv/bin/`。有关参考信息，请参考`/opt/netbox/contrib/`中的示例服务文件。

最后，重新启动gunicorn和RQ服务：

```no-highlight
sudo systemctl restart netbox netbox-rq
```

## 6. 验证清理计划

如果从NetBox v3.0之前的版本升级，请检查是否已配置cron任务（或类似的计划进程）来运行NetBox的每晚清理命令。包含此命令的shell脚本位于`contrib/netbox-housekeeping.sh`中。它可以链接到系统的每日cron任务目录中，或直接包含在crontab中。（如果NetBox已安装在非标准路径中，请首先更新此脚本中的系统路径。）

```shell
sudo ln -s /opt/netbox/contrib/netbox-housekeeping.sh /etc/cron.daily/netbox-housekeeping
```

有关详细信息，请参阅[清理文档](../administration/housekeeping.md)。
# NetBox安装

本部分文档讨论安装和配置NetBox应用程序本身。

## 安装系统包

首先安装NetBox及其依赖的所有系统包。

!!! warning "需要Python 3.8或更高版本"
    NetBox需要Python 3.8、3.9、3.10或3.11。

=== "Ubuntu"

    ```no-highlight
    sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential libxml2-dev libxslt1-dev libffi-dev libpq-dev libssl-dev zlib1g-dev
    ```

=== "CentOS"

    ```no-highlight
    sudo yum install -y gcc libxml2-devel libxslt-devel libffi-devel libpq-devel openssl-devel redhat-rpm-config
    ```

在继续之前，请检查您安装的Python版本是否至少为3.8：

```no-highlight
python3 -V
```

## 下载NetBox

本文档提供两种安装NetBox的选项：从可下载的存档文件安装，或从Git存储库安装。从软件包安装（选项A）需要手动获取并解压存档文件，以进行每次更新，而通过Git安装（选项B）可以通过重新拉取`master`分支来实现无缝升级。

### 选项A：下载发行版存档

从GitHub下载[最新的稳定版本](https://github.com/netbox-community/netbox/releases)作为tarball或ZIP存档文件，并将其提取到所需的路径。在本示例中，我们将使用`/opt/netbox`作为NetBox根目录。

```no-highlight
sudo wget https://github.com/netbox-community/netbox/archive/refs/tags/vX.Y.Z.tar.gz
sudo tar -xzf vX.Y.Z.tar.gz -C /opt
sudo ln -s /opt/netbox-X.Y.Z/ /opt/netbox
```

!!! note
    建议将NetBox安装在以其版本号命名的目录中。例如，NetBox v3.0.0将安装在`/opt/netbox-3.0.0`中，并且从`/opt/netbox/`将指向此位置的符号链接。这允许将来的版本并行安装，而不会中断当前安装。在切换到新版本时，只需更新符号链接。

### 选项B：克隆Git存储库

创建NetBox安装的基本目录。在本指南中，我们将使用`/opt/netbox`。

```no-highlight
sudo mkdir -p /opt/netbox/
cd /opt/netbox/
```

如果尚未安装`git`，请安装它：

=== "Ubuntu"

    ```no-highlight
    sudo apt install -y git
    ```

=== "CentOS"

    ```no-highlight
    sudo yum install -y git
    ```

接下来，将NetBox GitHub存储库的**master**分支克隆到当前目录中。 （此分支始终包含当前的稳定发布版本。）

```no-highlight
sudo git clone -b master --depth 1 https://github.com/netbox-community/netbox.git .
```

!!! note
    上面的`git clone`命令使用“浅克隆”以获取最近的提交。如果需要下载整个历史记录，请省略`--depth 1`参数。

`git clone`命令应生成类似于以下内容的输出：

```
Cloning into '.'...
remote: Enumerating objects: 996, done.
remote: Counting objects: 100% (996/996), done.
remote: Compressing objects: 100% (935/935), done.
remote: Total 996 (delta 148), reused 386 (delta 34), pack-reused 0
Receiving objects: 100% (996/996), 4.26 MiB | 9.81 MiB/s, done.
Resolving deltas: 100% (148/148), done.
```

!!! note
    通过git安装还允许您轻松尝试不同版本的NetBox。要检出[特定的NetBox版本](https://github.com/netbox-community/netbox/releases)，请使用所需的发行标签运行`git checkout`命令。例如，`git checkout v3.0.8`。

## 创建NetBox系统用户

创建名为`netbox`的系统用户帐户。我们将配置WSGI和HTTP服务以在此帐户下运行。我们还将分配此用户对媒体目录的所有权。这确保了NetBox能够保存上传的文件。

=== "Ubuntu"

    ```
    sudo adduser --system --group netbox
    sudo chown --recursive netbox /opt/netbox/netbox/media/
    sudo chown --recursive netbox /opt/netbox/netbox/reports/
    sudo chown --recursive netbox /opt/netbox/netbox/scripts/
    ```

=== "CentOS"

    ```
    sudo groupadd --system netbox
    sudo adduser --system -g netbox netbox
    sudo chown --recursive netbox /opt/netbox/netbox/media/
    sudo chown --recursive netbox /opt/netbox/netbox/reports/
    sudo chown --recursive netbox /opt/netbox/netbox/scripts/
    ```

## 配置

进入NetBox配置目录，并复制`configuration_example.py`为`configuration.py`。此文件将保存所有本地配置参数。

```no-highlight
cd /opt/netbox/netbox/netbox/
sudo cp configuration_example.py configuration.py
```

使用您喜欢的编辑器打开`configuration.py`以开始配置NetBox。NetBox提供[许多配置参数](../configuration/index.md)，但只有以下四个对新安装是必需的：

* `ALLOWED_HOSTS`
* `DATABASE`
* `REDIS`
* `SECRET_KEY`

### ALLOWED_HOSTS

这是允许此服务器

通过的有效主机名和IP地址列表。您必须至少指定一个名称或IP地址。（请注意，这不会限制可以访问NetBox的位置：它仅用于[HTTP主机标头验证](https://docs.djangoproject.com/en/3.0/topics/security/#host-headers-virtual-hosting)。）

```python
ALLOWED_HOSTS = ['netbox.example.com', '192.0.2.123']
```

如果您尚未确定NetBox安装的域名和/或IP地址，可以将其设置为通配符（星号）以允许所有主机值：

```python
ALLOWED_HOSTS = ['*']
```

### DATABASE

此参数保存数据库配置详细信息。您必须定义在配置PostgreSQL时使用的用户名和密码。如果服务在远程主机上运行，请相应地更新`HOST`和`PORT`参数。有关单个参数的更多详细信息，请参阅[配置文档](../configuration/required-parameters.md#database)。

```python
DATABASE = {
    'NAME': 'netbox',               # 数据库名称
    'USER': 'netbox',               # PostgreSQL用户名
    'PASSWORD': 'J5brHrAXFLQSif0K', # PostgreSQL密码
    'HOST': 'localhost',            # 数据库服务器
    'PORT': '',                     # 数据库端口（留空使用默认值）
    'CONN_MAX_AGE': 300,            # 最大数据库连接时间（秒）
}
```

### REDIS

Redis是NetBox用于缓存和后台任务排队的内存中的键值存储。Redis通常需要最少的配置；下面的值应对大多数安装足够。有关各个参数的更多详细信息，请参阅[配置文档](../configuration/required-parameters.md#redis)。

请注意，NetBox需要指定两个单独的Redis数据库：`tasks`和`caching`。这两者都可以由同一个Redis服务提供，但是每个都应具有唯一的数字数据库ID。

```python
REDIS = {
    'tasks': {
        'HOST': 'localhost',      # Redis服务器
        'PORT': 6379,             # Redis端口
        'PASSWORD': '',           # Redis密码（可选）
        'DATABASE': 0,            # 数据库ID
        'SSL': False,             # 使用SSL（可选）
    },
    'caching': {
        'HOST': 'localhost',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 1,            # 第二个数据库的唯一ID
        'SSL': False,
    }
}
```

### SECRET_KEY

此参数必须分配一个随机生成的键，用作哈希和相关加密函数的盐（注意，它绝不直接用于加密秘密数据）。此密钥必须对此安装是唯一的，并建议至少50个字符长。不要在本地系统外共享它。

在父目录中提供了一个名为`generate_secret_key.py`的简单Python脚本，以帮助生成合适的密钥：

```no-highlight
python3 ../generate_secret_key.py
```

!!! warning "SECRET_KEY的值必须匹配"
    在具有多个Web服务器的高可用性安装中，`SECRET_KEY`必须在所有服务器上相同，以保持持久的用户会话状态。

完成修改配置后，请记得保存文件。

## 可选要求

NetBox所需的所有Python包都列在`requirements.txt`中，将自动安装。NetBox还支持一些可选的包。如果需要，这些包必须在NetBox根目录中的`local_requirements.txt`中列出。

### 远程文件存储

默认情况下，NetBox将使用本地文件系统来存储上传的文件。要使用远程文件系统，请安装[`django-storages`](https://django-storages.readthedocs.io/en/stable/)库，并在`configuration.py`中配置您的[所需存储后端](../configuration/system.md#storage_backend)。

```no-highlight
sudo sh -c "echo 'django-storages' >> /opt/netbox/local_requirements.txt"
```

### 远程数据源

NetBox支持通过可配置的后端与几个远程数据源集成。每个都需要安装一个或多个附加库。

* Amazon S3：[`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* Git：[`dulwich`](https://www.dulwich.io/)

例如，要启用Amazon S3后端，请将`boto3`添加到您的本地要求文件中：

```no-highlight
sudo sh -c "echo 'boto3' >> /opt/netbox/local_requirements.txt"
```

!!! info
    这些包在NetBox v3.5中以前是必需的，但现在是可选的。

### Sentry集成

NetBox可以配置为将错误报告发送到[Sentry](../administration/error-reporting.md)以进行分析。此集成需要安装`sentry-sdk` Python库。

```no-highlight
sudo sh -c "echo 'sentry-sdk' >> /opt/netbox/local_requirements.txt"
```

!!! info
    在NetBox v3.6中，默认情况下包括了Sentry集成，但现在是可选的。

## 运行升级脚本

一旦NetBox已配置完成，我们就可以继续进行实际的安装。我们将运行打包的升级脚本（`upgrade.sh`）来执行以下操作：

* 创建Python虚拟环境
* 安装所有必需的Python包
* 运行数据库模式迁移
* 本地构建文档（供离线使用）
* 在磁盘上汇总静态资源文件

!!! warning
    如果您仍然有来自前面安装步骤的Python虚拟环境，请现在通过运行`deactivate`命令将其禁用。这将避免在已配置为保留用户当前环境的系统上发生错误。

```no-highlight
sudo /opt/netbox/upgrade.sh
```

请注意，NetBox v3.2及更高版本需要**Python 3.8或更高版本**。如果服务器上的默认Python安装设置为较低版本，请将受支持的安装路径作为名为`PYTHON`的环境变量传递。（请注意，在`sudo`命令之后必须传递环境变量。）

```no-highlight
sudo PYTHON=/usr/bin/python3.8 /opt/netbox/upgrade.sh
```

!!! note
    完成后，升级脚本可能会警告未检测到现有的虚拟环境。由于这是一个新安装，可以安全地忽略此警告。

## 创建超级用户

NetBox没有预定义的用户帐户。您需要创建一个超级用户（管理帐户）以便能够登录NetBox。首先，进入由升级脚本创建的Python虚拟环境：

```no-highlight
source /opt/netbox/venv/bin/activate
```

一旦虚拟环境已激活，您应该会注意到在控制台提示之前添加了字符串`(venv)`。

接下来，我们将使用`createsuperuser` Django管理命令（通过`manage.py`）创建一个超级用户帐户。不需要为用户指定电子邮件地址，但请确保使用非常强的密码。

```no-highlight
cd /opt/netbox/netbox
python3 manage.py createsuperuser
```

## 配置定期任务

NetBox包括一个`housekeeping`管理命令，用于处理一些定期清理任务，例如清除旧会话和过期的更改记录。虽然可以手动运行此命令，但建议使用系统的`cron`守护程序或类似的实用程序配置定期任务。

可以在`contrib/netbox-housekeeping.sh`中找到调用此命令的shell脚本。可以将它复制到系统的每日cron任务目录中，或直接包含在crontab中。(如果将NetBox安装到非标准路径，请确保首先在此脚本中更新系统路径。)

```shell
sudo ln -s /opt/netbox/contrib/netbox-housekeeping.sh /etc/cron.daily/netbox-housekeeping
```

有关更多详细信息，请参阅[housekeeping文档](../administration/housekeeping.md)。

## 测试应用程序

此时，我们应该能够运行NetBox的开发服务器进行测试。我们可以通过在本地启动开发实例来检查。

!!! 提示
    在尝试运行服务器之前，请检查Python虚拟环境是否仍然处于活动状态。

```no-highlight
python3 manage.py runserver 0.0.0.0:8000 --insecure
```

如果成功，您应该会看到类似以下的输出：

```no-highlight
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 30, 2021 - 18:02:23
Django version 3.2.6, using settings 'netbox.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

接下来，连接到服务器的名称或IP地址（如`ALLOWED_HOSTS`中定义）的端口8000；例如，<http://127.0.0.1:8000/>。您应该会看到NetBox的首页。尝试使用创建超级用户时指定的用户名和密码登录。

!!! 注意
    默认情况下，基于RHEL的发行版可能会使用firewalld阻止您的测试尝试。可以使用`firewall-cmd`打开开发服务器端口（如果要使规则在服务器重启后保持生效，请添加`--permanent`）：

    ```no-highlight
    firewall-cmd --zone=public --add-port=8000/tcp
    ```

!!! 危险 "不适用于生产环境"
    开发服务器仅用于开发和测试目的。它既不足够高性能也不足够安全，不能用于生产环境。**不要在生产环境中使用它。**

!!! 警告
    如果测试服务未运行，或者无法访问NetBox首页，说明出现了问题。在修复安装之前，请不要继续阅读本指南的其余部分。

使用`Ctrl+c`停止开发服务器。
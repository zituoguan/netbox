# 系统维护

NetBox包括一个名为`housekeeping`的管理命令，应该每晚运行一次。该命令处理以下任务：

* 清除数据库中过期的认证会话
* 删除比配置的[保留时间](../configuration/miscellaneous.md#changelog_retention)更早的更改日志记录
* 删除比配置的[保留时间](../configuration/miscellaneous.md#job_retention)更早的作业结果记录
* 检查新的NetBox版本（如果设置了[`RELEASE_CHECK_URL`](../configuration/miscellaneous.md#release_check_url)）

可以直接调用此命令，也可以使用位于`/opt/netbox/contrib/netbox-housekeeping.sh`的提供的shell脚本。

## 调度

### 使用Cron

可以将此脚本链接到cron调度程序的每日作业目录中（例如`/etc/cron.daily`），或直接在cron配置文件中引用它。

```shell
sudo ln -s /opt/netbox/contrib/netbox-housekeeping.sh /etc/cron.daily/netbox-housekeeping
```

!!! note
    在基于Debian的系统上，请确保在从cron目录内部链接到脚本时省略`.sh`文件扩展名。否则，任务可能不会运行。

### 使用Systemd

首先，为systemd服务和计时器文件创建符号链接。从`/opt/netbox/contrib/`目录将现有的服务和计时器文件链接到`/etc/systemd/system/`目录中：

```bash
sudo ln -s /opt/netbox/contrib/netbox-housekeeping.service /etc/systemd/system/netbox-housekeeping.service
sudo ln -s /opt/netbox/contrib/netbox-housekeeping.timer /etc/systemd/system/netbox-housekeeping.timer
```

然后，重新加载systemd配置并启用计时器以在启动时自动启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now netbox-housekeeping.timer
```

通过运行以下命令来检查计时器的状态：

```bash
sudo systemctl list-timers --all
```

该命令将显示所有计时器的列表，包括您的`netbox-housekeeping.timer`。确保计时器处于活动状态并正确安排。

就是这样！现在已经配置了每天使用systemd运行的NetBox系统维护服务。

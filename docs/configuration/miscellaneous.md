# 其他参数

## 管理员

NetBox会将关于关键错误的详细信息通过电子邮件发送给此处列出的管理员。这应该是一个（姓名，电子邮件）元组的列表。例如：

```python
ADMINS = [
    ['Hank Hill', 'hhill@example.com'],
    ['Dale Gribble', 'dgribble@example.com'],
]
```

---

## BANNER_BOTTOM

!!! tip "动态配置参数"

设置用户界面底部横幅的内容。

---

## BANNER_LOGIN

!!! tip "动态配置参数"

这定义了要在登录页面上方登录表单之上显示的自定义内容。允许使用HTML。

---

## BANNER_MAINTENANCE

!!! tip "动态配置参数"

!!! note
    此参数在NetBox v3.5中添加。

在启用维护模式时，在每个页面的顶部添加横幅。允许使用HTML。

---

## BANNER_TOP

!!! tip "动态配置参数"

设置用户界面顶部横幅的内容。

!!! tip
    如果希望顶部和底部横幅相匹配，请设置以下内容：

    ```python
    BANNER_TOP = '您的横幅文本'
    BANNER_BOTTOM = BANNER_TOP
    ```

---

## CENSUS_REPORTING_ENABLED

默认值：True

启用匿名普查报告。要选择退出普查报告，请将其设置为False。

这些数据使项目维护人员能够估计存在多少NetBox部署，并跟踪随时间采用新版本的情况。每次启动工作进程时，普查报告都会产生一个HTTP请求。此功能仅报告NetBox版本、Python版本和伪随机唯一标识符。

---

## CHANGELOG_RETENTION

!!! tip "动态配置参数"

默认值：90

保留记录的更改的天数（对象的创建、更新和删除）。将其设置为`0`将无限期保留数据库中的更改。

!!! warning
    如果启用无限期的更改日志保留，建议定期删除旧条目。否则，数据库最终可能会超出容量。

---

## CHANGELOG_SKIP_EMPTY_CHANGES

默认值：True

如果启用，当对象在不更改其现有字段值的情况下更新时，将不会创建更改日志记录。

!!! note
    无论此参数如何设置，对象的`last_updated`字段始终会反映最近更新的时间。

---

## DATA_UPLOAD_MAX_MEMORY_SIZE

默认值：`2621440`（2.5 MB）

传入HTTP请求（即`GET`或`POST`数据）的最大大小（以字节为单位）。超过此大小的请求将引发`RequestDataTooBig`异常。

---

## ENFORCE_GLOBAL_UNIQUE

!!! tip "动态配置参数"

默认值：True

默认情况下，NetBox将防止在全局表中（即不分配给任何VRF的表）创建重复的前缀和IP地址。可以通过将`ENFORCE_GLOBAL_UNIQUE`设置为False来禁用此验证。

!!! info "在v3.7中更改"
    此参数的默认值已从False更改为True，从NetBox v3.7开始。

---

## FILE_UPLOAD_MAX_MEMORY_SIZE

默认值：`2621440`（2.5 MB）

在写入文件系统之前，内存中保存的上传数据的最大量（以字节为单位）。更改此设置可以用于例如能够上传大于2.5MB的文件到自定义脚本进行处理。

---

## GRAPHQL_ENABLED

!!! tip "动态配置参数"

默认值：True

将其设置为False将禁用GraphQL API。

---

## JOB_RETENTION

!!! tip "动态配置参数"

!!! note
    从NetBox v3.5起，将此参数的名称更改为`JOBRESULT_RETENTION`。

默认值：90

保留作业结果（脚本和报告）的天数。将其设置为`0`将无限期保留数据库中的作业结果。

!!! warning
    如果启用无限期的作业结果保留，建议定期删除旧条目。否则，数据库最终可能会超出容量。

---

## MAINTENANCE_MODE

!!! tip "动态配置参数"

默认值：False

将其设置为True将在每个页面的顶部显示“维护模式”横幅。此外，NetBox将不再在登录时更新用户的“上次活动”时间。这是为了允许在数据库处于只读状态时进行新的登录。当禁用维护模式时，将恢复记录登录时间。

---

## MAPS_URL

!!! tip "动态配置参数"

默认值：`https://maps.google.com/?q=`（Google Maps）

这指定了在通过街道地址或GPS坐标呈现物理位置的地图时要使用的URL。该URL必须接受一个自由格式的街道地址或附加到其后的一对逗号分隔的数字坐标。将其设置为`None`将禁用UI内的“地图”按钮。

---

## MAX_PAGE_SIZE

!!! tip "动态配置参数"

默认值：1000

Web用户或API消费者可以通过在URL上附加“limit”参数（例如`?limit=1000`）来请求任意数量的对象。此参数定义了最大可接受的限制。将其设置为`0`或`None`将允许客户端通过指定`?limit=0`来一次检索所有匹配的对象，没有限制。

---

## METRICS_ENABLED

默认值：False

切换可用于`/metrics`的Prometheus兼容指标。有关更多详细信息，请参阅[Prometheus指标](../integrations/prometheus-metrics.md)文档。

---

## PREFER_IPV4

!!! tip "动态配置参数"

默认值：False

在确定设备的主要IP地址时，默认情况下优先使用IPv6而不是IPv4。将其设置为True以优先使用IPv4。

---

## QUEUE_MAPPINGS

允许更改内部用于后台任务的队列。

```python
QUEUE_MAPPINGS = {
    'webhook': 'low',
    'report': 'high',
    'script': 'high',
}
```

如果未定义队列，将使用名为`default`的队列。

---

## RELEASE_CHECK_URL

默认值：None（禁用）

此参数定义将检查新的NetBox版本的存储库的URL。检测到新版本时，将在主页上向管理用户显示一条消息。可以将其设置为官方存储库（`'https://api.github.com/repos/netbox-community/netbox/releases'`）或自定义分支。将其设置为`None`以禁用自动更新检查。

!!! note
    提供的URL **必须** 与[GitHub REST API](https://docs.github.com/en/rest)兼容。

---

## RQ_DEFAULT_TIMEOUT

默认值：`300`

后台任务（例如运行自定义脚本）的最大执行时间（以秒为单位）。

---

## RQ_RETRY_INTERVAL

!!! note
    从NetBox v3.5起，添加了此参数。

默认值：`60`

此参数控制失败的作业重试的频率，最多可以由`RQ_RETRY_MAX`指定的次数。这必须是指定连续尝试之间等待的秒数的整数，或者是这些值的列表。例如，`[60, 300, 3600]`将在1分钟、5分钟和1小时后重试任务。

---

## RQ_RETRY_MAX

!!! note
    从NetBox v3.5起，添加了此参数。

默认值：`0`（禁用重试）

在作业失败被标记为失败之前，后台任务将被重试的最大次数。
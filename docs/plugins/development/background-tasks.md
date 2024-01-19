# 背景任务

NetBox 支持使用 [Python RQ](https://python-rq.org/) 库，将需要在后台执行的任务排队，与请求-响应周期解耦。默认情况下，定义了三个不同优先级的任务队列：

* 高优先级
* 默认优先级
* 低优先级

在检查默认队列之前，任何在“高优先级”队列中的任务都将被完成，并且在“默认”队列中的任务完成之前，将完成“低”队列中的任务。

插件还可以通过在 PluginConfig 类下设置 `queues` 属性来为其自己的需求添加自定义队列。下面包含一个示例：

```python
class MyPluginConfig(PluginConfig):
    name = 'myplugin'
    ...
    queues = [
        'foo',
        'bar',
    ]
```

上面的 PluginConfig 创建了两个具有以下名称的自定义队列 `my_plugin.foo` 和 `my_plugin.bar`。（插件的名称会在每个队列前面添加，以避免插件之间的冲突。）

!!! 警告 "配置 RQ 工作进程"
    默认情况下，NetBox 的 RQ 工作进程仅服务于高、默认和低队列。引入自定义队列的插件应该建议用户重新配置默认工作进程，或者运行一个专用工作进程，指定所需的队列。例如：
    
    ```
    python manage.py rqworker my_plugin.foo my_plugin.bar
    ```

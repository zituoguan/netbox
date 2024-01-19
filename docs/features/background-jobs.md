# 后台作业

NetBox 包含了执行某些功能作为后台任务的能力。这些包括：

* [报告](../customization/reports.md)执行
* [自定义脚本](../customization/custom-scripts.md)执行
* 同步[远程数据源](../integrations/synchronized-data.md)

此外，NetBox 插件可以将自己的后台任务加入队列。这是通过 [Job 模型](../models/core/job.md) 实现的。后台任务由 `rqworker` 进程执行。

## 计划任务

后台作业可以配置为立即运行，或在未来的设定时间运行。计划任务也可以配置为以设定间隔重复执行。
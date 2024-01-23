# 信号

除了[Django内置的信号](https://docs.djangoproject.com/en/stable/topics/signals/)之外，NetBox还定义了一些自己的信号，如下所示。

## post_clean

此信号由继承自`CustomValidationMixin`的模型在其`clean()`方法结束时发送。

### 接收器

* `extras.signals.run_custom_validators()`

## core.job_start

每当[后台作业](../features/background-jobs.md)启动时，都会发送此信号。

### 接收器

* `extras.signals.process_job_start_event_rules()`

## core.job_end

每当[后台作业](../features/background-jobs.md)终止时，都会发送此信号。

### 接收器

* `extras.signals.process_job_end_event_rules()`

## core.pre_sync

当调用[DataSource](../models/core/datasource.md)模型的`sync()`方法时，将发送此信号。

## core.post_sync

当[DataSource](../models/core/datasource.md)完成同步时，将发送此信号。

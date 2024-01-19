# Prometheus Metrics

NetBox支持选择性地从应用程序中暴露本机Prometheus度量指标。[Prometheus](https://prometheus.io/)是一种流行的用于监视的时间序列度量平台。

NetBox在`/metrics` HTTP端点上公开度量指标，例如`https://netbox.local/metrics`。度量指标的暴露可以通过`METRICS_ENABLED`配置设置来切换。默认情况下不会暴露度量指标。

## 度量指标类型

NetBox使用[django-prometheus](https://github.com/korfuri/django-prometheus)库导出多种不同类型的度量指标，包括：

- 每个模型的插入、更新和删除计数器
- 每个视图请求计数器
- 每个视图请求延迟直方图
- 请求体大小直方图
- 响应体大小直方图
- 响应代码计数器
- 数据库连接、执行和错误计数器
- 缓存命中、未命中和失效计数器
- Django中间件延迟直方图
- 其他与Django相关的元数据度量指标

有关公开的度量指标的详尽列表，请访问您的NetBox实例上的`/metrics`端点。

## 多进程注意事项

在以多进程方式部署NetBox（例如运行多个Gunicorn工作进程）时，Prometheus客户端库需要使用共享目录来从所有工作进程收集度量指标。要配置此目录，请首先创建或指定一个本地目录，其中工作进程具有读取和写入访问权限，然后配置您的WSGI服务（例如Gunicorn）将此路径定义为`prometheus_multiproc_dir`环境变量。

!!! 警告
    如果在多进程环境中获得准确的长期度量指标对于您的部署至关重要，则建议您使用`uwsgi`库而不是`gunicorn`。问题出在`gunicorn`跟踪工作进程的方式上（与`uwsgi`相比），后者有助于管理上述配置创建的度量指标文件。如果您在容器化环境中使用gunicorn以每个容器一个进程的方法使用NetBox，那么您可能不需要切换到`uwsgi`。更多详细信息请参见[问题#3779](https://github.com/netbox-community/netbox/issues/3779#issuecomment-590547562)。

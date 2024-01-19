# 错误报告

## Sentry

### 启用错误报告

NetBox支持与[Sentry](https://sentry.io/)的本机集成，用于自动错误报告。要启用此功能，请将`SENTRY_ENABLED`设置为True，并在`configuration.py`中定义您唯一的[数据源名称（DSN）](https://docs.sentry.io/product/sentry-basics/concepts/dsn-explainer/)。

```python
SENTRY_ENABLED = True
SENTRY_DSN = "https://examplePublicKey@o0.ingest.sentry.io/0"
```

将`SENTRY_ENABLED`设置为False将禁用Sentry集成。

### 分配标签

如果需要，您可以通过设置`SENTRY_TAGS`参数，将一个或多个任意标签附加到出站错误报告：

```python
SENTRY_TAGS = {
    "custom.foo": "123",
    "custom.bar": "abc",
}
```

!!! warning "保留的标签前缀"
    避免使用以`netbox.`开头的任何标签名称，因为此前缀由NetBox应用程序保留。

### 测试

保存配置后，重新启动NetBox服务。

要测试Sentry操作，尝试通过导航到无效的URL生成404（页面未找到）错误，例如`https://netbox/404-error-testing`。（确保已禁用调试模式。）在从NetBox服务器接收到404响应后，您应该很快在Sentry中看到此问题。

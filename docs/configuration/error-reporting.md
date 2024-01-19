# 错误报告设置

## Sentry数据源名称 (SENTRY_DSN)

默认值: 无

定义了一个Sentry数据源名称（DSN），用于自动错误报告。要使此参数生效，必须将`SENTRY_ENABLED`设置为True。例如：

```
SENTRY_DSN = "https://examplePublicKey@o0.ingest.sentry.io/0"
```

---

## 启用Sentry (SENTRY_ENABLED)

默认值: False

设置为True以通过[Sentry](https://sentry.io/)启用自动错误报告。

!!! 注意
    启用Sentry集成需要安装`sentry-sdk` Python包。

---

## 错误采样率 (SENTRY_SAMPLE_RATE)

默认值: 1.0 (全部)

用于错误报告的采样率。必须是介于0（禁用）和1.0（报告所有错误）之间的值。

---

## Sentry标签 (SENTRY_TAGS)

一个可选的标签名称和值字典，用于应用于Sentry错误报告。例如：

```
SENTRY_TAGS = {
    "custom.foo": "123",
    "custom.bar": "abc",
}
```

!!! 警告 "保留的标签前缀"
    避免使用以`netbox.`开头的任何标签名称，因为此前缀被NetBox应用程序保留。

---

## 事务采样率 (SENTRY_TRACES_SAMPLE_RATE)

默认值: 0 (禁用)

用于事务的采样率。必须是介于0（禁用）和1.0（报告所有事务）之间的值。

!!! 警告 "考虑性能影响"
    对事务的高采样率可能导致显着的性能损失。如果需要事务报告，建议使用相对较低的采样率，例如10%到20%（0.1到0.2）。
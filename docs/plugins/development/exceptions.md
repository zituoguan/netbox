# 异常

以下列出的异常类可由插件引发，以在各种情况下更改 NetBox 的默认行为。

## `终止请求`

NetBox 提供了几个通用视图和 REST API 视图集，这些视图有助于单独或批量创建、修改和删除对象。在某些情况下，插件可能希望中断这些操作并干净地中止请求，向最终用户或 API 消费者报告错误消息。

例如，插件可以通过将接收器连接到 Site 模型的 Django `pre_save` 信号来禁止创建具有禁止名称的站点：

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from dcim.models import Site
from utilities.exceptions import AbortRequest

PROHIBITED_NAMES = ('foo', 'bar', 'baz')

@receiver(pre_save, sender=Site)
def test_abort_request(instance, **kwargs):
    if instance.name.lower() in PROHIBITED_NAMES:
        raise AbortRequest(f"Site name can't be {instance.name}!")
```

在引发 `AbortRequest` 时必须提供错误消息。这将传达给用户，并应清楚地解释请求被中止的原因，以及可能的解决方法。

!!! 提示 "考虑自定义验证规则"
    此异常旨在用于处理复杂的评估逻辑，并应谨慎使用。对于简单的对象验证（例如上面的虚构示例），请考虑使用[自定义验证规则](../../customization/custom-validation.md)。

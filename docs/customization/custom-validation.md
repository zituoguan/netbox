# 自定义验证

NetBox 在将对象写入数据库之前会对其进行验证，以确保数据的完整性。这种验证包括检查是否有正确的格式以及相关对象的引用是否有效。但是，您可能希望使用一些自己的规则来补充此验证。例如，您可能要求每个站点的名称符合特定模式。这可以通过使用自定义验证规则来实现。

## 自定义验证规则

自定义验证规则表示为模型属性到该属性必须符合的一组规则的映射。例如：

```json
{
  "name": {
    "min_length": 5,
    "max_length": 30
  }
}
```

这定义了一个自定义验证器，该验证器检查对象的 `name` 属性的长度至少为五个字符，且不超过三十个字符。此验证在 NetBox 执行其自身内部验证之后执行。

`CustomValidator` 类支持多种验证类型：

- `min`：最小值
- `max`：最大值
- `min_length`：最小字符串长度
- `max_length`：最大字符串长度
- `regex`：应用[正则表达式](https://en.wikipedia.org/wiki/Regular_expression)
- `required`：必须指定一个值
- `prohibited`：不得指定值
- `eq`：值必须等于指定值
- `neq`：值不能等于指定值

`min` 和 `max` 类型应该为数值，而 `min_length`、`max_length` 和 `regex` 适用于字符串（文本值）。`required` 和 `prohibited` 验证器可以用于任何字段，并且应传递一个值 `True`。

!!! warning
    请注意，这些验证器仅是 NetBox 自身验证的补充，不会覆盖它。例如，如果 NetBox 要求某个模型字段必填，那么为该字段设置 `{'prohibited': True}` 的验证器将不起作用。

### 自定义验证逻辑

可能会出现所提供的验证类型不足的情况。NetBox 提供了一个 `CustomValidator` 类，可以通过覆盖其 `validate()` 方法来强制执行任意验证逻辑，并在检测到不满意的条件时调用 `fail()`。

```python
from extras.validators import CustomValidator

class MyValidator(CustomValidator):

    def validate(self, instance):
        if instance.status == 'active' and not instance.description:
            self.fail("Active sites must have a description set!", field='status')
```

`fail()` 方法可以可选地指定一个字段，以关联提供的错误消息。如果指定了字段，错误消息将显示给用户，并与此字段关联。如果省略，错误消息将不与任何字段关联。

## 分配自定义验证器

自定义验证器与特定的 NetBox 模型相关联，位于 [CUSTOM_VALIDATORS](../configuration/data-validation.md#custom_validators) 配置参数下。可以通过以下三种方式定义自定义验证规则：

1. 普通 JSON 映射（无自定义逻辑）
2. 自定义验证器类的点路径
3. 直接引用自定义验证器类

### 普通数据

对于不需要自定义逻辑的情况，将验证规则传递为普通的 JSON 兼容对象就足够了。这种方法通常对配置的可移植性来说是最好的。例如：

```python
CUSTOM_VALIDATORS = {
    "dcim.site": [
        {
            "name": {
                "min_length": 5,
                "max_length": 30,
            }
        }
    ],
    "dcim.device": [
        {
            "platform": {
                "required": True,
            }
        }
    ]
}
```

### 点路径

在需要自定义验证器类的情况下，可以使用其 Python 路径（相对于 NetBox 的工作目录）来引用它：

```python
CUSTOM_VALIDATORS = {
    'dcim.site': (
        'my_validators.Validator1',
        'my_validators.Validator2',
    ),
    'dcim.device': (
        'my_validators.Validator3',
    )
}
```

### 直接类引用

这种方法要求每个要实例化的类都必须在 Python 配置文件中直接导入。

```python
from my_validators import Validator1, Validator2, Validator3

CUSTOM_VALIDATORS = {
    'dcim.site': (
        Validator1(),
        Validator2(),
    ),
    'dcim.device': (
        Validator3(),
    )
}
```

!!! note
    即使只定义了一个验证器，也必须将其传递为可迭代对象。
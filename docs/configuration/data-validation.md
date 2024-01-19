# 数据与验证参数

## CUSTOM_VALIDATORS

!!! 提示 "动态配置参数"

这是一个将模型映射到本地定义的[自定义验证器](../customization/custom-validation.md)以执行自定义验证逻辑的映射。下面提供了一个示例：

```python
CUSTOM_VALIDATORS = {
    "dcim.site": [
        {
            "name": {
                "min_length": 5,
                "max_length": 30
            }
        },
        "my_plugin.validators.Validator1"
    ],
    "dim.device": [
        "my_plugin.validators.Validator1"
    ]
}
```

---

## FIELD_CHOICES

某些模型上的静态选择字段可以配置自定义值。这可以通过将`FIELD_CHOICES`定义为将模型字段映射到其选择的字典来完成。列表中的每个选择必须具有数据库值和友好的标签，并且可以可选地指定颜色（下面提供了可用颜色的列表）。

提供的选择可以替换NetBox提供的默认选择，也可以追加到默认选择中。要 _替换_ 可用的选择，请指定由点分隔的应用程序、模型和字段名称。例如，站点模型可以引用为`dcim.Site.status`。要 _扩展_ 可用的选择，请在该字符串末尾附加加号（例如`dcim.Site.status+`）。

例如，以下配置将使用选项Foo、Bar和Baz替换默认站点状态选择：

```python
FIELD_CHOICES = {
    'dcim.Site.status': (
        ('foo', 'Foo', 'red'),
        ('bar', 'Bar', 'green'),
        ('baz', 'Baz', 'blue'),
    )
}
```

在字段标识符末尾添加加号将 _添加_ 这些选择到已经提供的选择中：

```python
FIELD_CHOICES = {
    'dcim.Site.status+': (
        ...
    )
}
```

以下模型字段支持可配置的选择：

* `circuits.Circuit.status`
* `dcim.Device.status`
* `dcim.Location.status`
* `dcim.Module.status`
* `dcim.PowerFeed.status`
* `dcim.Rack.status`
* `dcim.Site.status`
* `dcim.VirtualDeviceContext.status`
* `extras.JournalEntry.kind`
* `ipam.IPAddress.status`
* `ipam.IPRange.status`
* `ipam.Prefix.status`
* `ipam.VLAN.status`
* `virtualization.Cluster.status`
* `virtualization.VirtualMachine.status`
* `wireless.WirelessLAN.status`

支持以下颜色：

* `blue`
* `indigo`
* `purple`
* `pink`
* `red`
* `orange`
* `yellow`
* `green`
* `teal`
* `cyan`
* `gray`
* `black`
* `white`

---

## PROTECTION_RULES

!!! 提示 "动态配置参数"

这是一个将模型映射到[自定义验证器](../customization/custom-validation.md)的映射，该验证器将在对象被删除之前立即评估该对象。如果验证失败，对象将不会被删除。下面提供了一个示例：

```python
PROTECTION_RULES = {
    "dcim.site": [
        {
            "status": {
                "eq": "decommissioning"
            }
        },
        "my_plugin.validators.Validator1",
    ]
}
```

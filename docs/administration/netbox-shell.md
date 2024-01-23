# The NetBox Python Shell

NetBox包含一个Python管理shell，您可以在其中直接查询、创建、修改和删除对象。要进入shell，请运行以下命令：

```
./manage.py nbshell
```

这将启动一个轻度定制的版本，[内置的Django shell](https://docs.djangoproject.com/en/stable/ref/django-admin/#shell)中预加载了所有相关的NetBox模型。（如果需要，还可以通过执行`./manage.py shell`来使用原始的Django shell。）

```
$ ./manage.py nbshell
### NetBox交互式shell（localhost）
### Python 3.7.10 | Django 3.2.5 | NetBox 3.0
### lsmodels()将显示可用的模型。使用help(<model>)获取更多信息。
```

函数`lsmodels()`将打印出所有可用的NetBox模型的列表：

```
>>> lsmodels()
DCIM:
  ConsolePort
  ConsolePortTemplate
  ConsoleServerPort
  ConsoleServerPortTemplate
  Device
  ...
```

!!! 警告
    NetBox shell允许以几乎没有验证的方式直接访问NetBox数据和功能。因此，务必确保只有经过授权的、有知识的用户才能访问它。在没有完全备份的情况下，永远不要在管理shell中执行任何操作。

## 查询对象

可以使用[Django查询集](https://docs.djangoproject.com/en/stable/topics/db/queries/#retrieving-objects)从数据库中检索对象。对象的基本查询集采用`<model>.objects.all()`的形式，它将返回该类型的所有对象的（截断的）列表。

```
>>> Device.objects.all()
<QuerySet [<Device: TestDevice1>, <Device: TestDevice2>, <Device: TestDevice3>,
<Device: TestDevice4>, <Device: TestDevice5>, '...(remaining elements truncated)...']>
```

使用`for`循环来遍历列表中的所有对象：

```
>>> for device in Device.objects.all():
...   print(device.name, device.device_type)
...
('TestDevice1', <DeviceType: PacketThingy 9000>)
('TestDevice2', <DeviceType: PacketThingy 9000>)
('TestDevice3', <DeviceType: PacketThingy 9000>)
('TestDevice4', <DeviceType: PacketThingy 9000>)
('TestDevice5', <DeviceType: PacketThingy 9000>)
...
```

要计算与查询匹配的所有对象的数量，请用`count()`替换`all()`：

```
>>> Device.objects.count()
1274
```

要检索特定对象（通常是根据其主键或其他唯一字段），请使用`get()`：

```
>>> Site.objects.get(pk=7)
<Site: Test Lab>
```

### 过滤查询集

在大多数情况下，您将只想检索特定子集的对象。要过滤查询集，请将`all()`替换为`filter()`，并传递一个或多个关键字参数。例如：

```
>>> Device.objects.filter(status="active")
<QuerySet [<Device: TestDevice1>, <Device: TestDevice2>, <Device: TestDevice3>,
<Device: TestDevice8>, <Device: TestDevice9>, '...(remaining elements truncated)...']>
```

查询集支持切片以返回特定范围的对象。

```
>>> Device.objects.filter(status="active")[:3]
<QuerySet [<Device: TestDevice1>, <Device: TestDevice2>, <Device: TestDevice3>]>
```

可以在查询集的末尾添加`count()`方法，以返回对象的数量而不是完整列表。

```
>>> Device.objects.filter(status="active").count()
982
```

可以通过将属性名与双下划线连接来穿越与其他模型的关系。例如，以下内容将返回分配给名称为“Pied Piper”的租户的所有设备。

```
>>> Device.objects.filter(tenant__name="Pied Piper")
```

这种方法可以跨越多级关系。例如，以下内容将返回位于北美的设备上分配的所有IP地址。

```
>>> IPAddress.objects.filter(interface__device__site__region__slug="north-america")
```

!!! 注意
    虽然上述查询是可行的，但效率不高。有优化这类请求的方法，但这些方法超出了本文档的范围。有关更多信息，请参阅[Django查询集方法参考](https://docs.djangoproject.com/en/stable/ref/models/querysets/)文档。

也可以穿越反向关系。例如，以下内容将查找所有带有名称为“em0”的接口的设备：

```
>>> Device.objects.filter(interfaces__name="em0")
```

可以使用`contains`或`icontains`字段查找来自字段查找（后者不区分大小写）对字符字段进行部分匹配。

```
>>> Device.objects.filter(name__icontains="testdevice")
```

类似地，可以使用小于、大于和/或等于给定值的值对数字字段进行筛选。

```
>>> VLAN.objects.filter(vid__gt=2000)
```

可以组合多个过滤器以进一步细化查询集。

```
>>> VLAN.objects.filter(vid__gt=2000, name__icontains="engineering")
```

要返回查询集的反向结果，请使用`exclude()`而不是`filter()`。

```
>>> Device.objects.count()
4479
>>> Device.objects.filter(status="active").count()
4133
>>> Device.objects.exclude(status="active").count()
346
```

!!! 信息
    上述示例仅旨在提供对查询集过滤的简要介绍。要查看可用过滤器的详尽列表，请参阅[Django查询集API文档](https://docs.djangoproject.com/en/stable/ref/models/querysets/)。

## 创建和更新对象

可以通过实例化所需的模型、为所有必需属性定义值并在实例上调用`save()`来创建新对象。例如，我们可以通过指定其数字ID、名称和分配的站点来创建一个新的VLAN：

```
>>> lab1 = Site.objects.get(pk=7)
>>> myvlan = VLAN(vid=123, name='MyNewVLAN', site=lab1)
>>> myvlan.full_clean()
>>> myvlan.save()
```

要修改现有对象，我们检索它，更新所需的字段，然后再次调用`save()`。

```
>>> vlan = VLAN.objects.get(pk=1280)
>>> vlan.name
'MyNewVLAN'
>>> vlan.name = 'BetterName'
>>> vlan.full_clean()
>>> vlan.save()
>>> VLAN.objects.get(pk=1280).name
'BetterName'
```

!!! 警告
    Django ORM提供了一次创建/编辑多个对象的方法，即`bulk_create()`和`update()`。在大多数情况下最好避免使用它们，因为它们绕过了模型的内置验证，如果不小心使用，很容易导致数据库损坏。

## 删除对象

要删除一个对象，只需在其实例上调用`delete()`。这将返回一个包含已删除的所有对象（包括相关对象）的字典。

```
>>> vlan
<VLAN: 123 (BetterName)>
>>> vlan.delete()
(1, {'ipam.VLAN': 1})
```

要一次删除多个对象，请在过滤后的查询集上调用`delete()`。在删除它们之前，总是检查所选对象的数量是个好主意。

```
>>> Device.objects.filter(name__icontains='test').count()
27
>>> Device.objects.filter(name__icontains='test').delete()
(35, {'dcim.DeviceBay': 0, 'dcim.InterfaceConnection': 4,
'extras.ImageAttachment': 0, 'dcim.Device': 27, 'dcim.Interface': 4,
'dcim.ConsolePort': 0, 'dcim.PowerPort': 0})
```

!!! 警告
    删除是立即且不可逆转的。在在实例或查询集上调用`delete()`之前，务必仔细考虑删除对象的影响。

# 自定义脚本

自定义脚本引入了一种在NetBox UI内执行自定义逻辑的方式。自定义脚本使用户能够直接并方便地以预定的方式操作NetBox数据。它们可用于执行各种任务，例如：

* 在准备新站点部署时自动填充新设备和电缆
* 创建一系列新的保留前缀或IP地址
* 从外部来源获取数据并导入到NetBox

自定义脚本是Python代码，存在于官方NetBox代码库之外，因此可以在不干扰核心NetBox安装的情况下进行更新和更改。并且由于它们完全是自定义的，因此没有脚本可以执行的固有限制。

## 编写自定义脚本

所有自定义脚本必须继承自`extras.scripts.Script`基类。此类提供了生成表单和记录活动所需的功能。

```python
from extras.scripts import Script

class MyScript(Script):
    ...
```

脚本由两个核心组件组成：一组变量和一个`run()`方法。变量允许您的脚本通过NetBox UI接受用户输入，但这是可选的：如果您的脚本不需要任何用户输入，那么不需要定义任何变量。

`run()`方法是您的脚本的执行逻辑所在之处（请注意，您的脚本可以拥有所需数量的方法：这仅仅是NetBox的调用点）。

```python
class MyScript(Script):
    var1 = StringVar(...)
    var2 = IntegerVar(...)
    var3 = ObjectVar(...)

    def run(self, data, commit):
        ...
```

`run()`方法应接受两个参数：

* `data` - 包含通过Web表单传递的所有变量数据的字典。
* `commit` - 一个布尔值，指示是否将提交数据库更改。

定义脚本变量是可选的：如果不需要用户输入，则可以创建仅包含`run()`方法的脚本。

脚本在执行过程中生成的任何输出都将显示在用户界面的“输出”选项卡下。

默认情况下，模块中的脚本按字母顺序在脚本列表页中排序。要按特定顺序返回脚本，您可以在模块的末尾定义script_order变量。script_order变量是一个包含每个脚本类的顺序的元组。未包含在此列表中的任何脚本将被列在最后。

```python
from extras.scripts import Script

class MyCustomScript(Script):
    ...

class AnotherCustomScript(Script):
    ...

script_order = (MyCustomScript, AnotherCustomScript)
```

## 模块属性

### `name`

您可以在脚本模块内（包含一个或多个脚本的Python文件）定义`name`以设置模块名称。如果未定义`name`，则将使用模块的文件名。

## 脚本属性

脚本属性在脚本内部的名为`Meta`的类下定义。这些是可选的，但是鼓励使用。

### `name`

这是您的脚本的友好名称。如果省略，将使用类名。

### `description`

脚本功能的人性化描述。

### `field_order`

默认情况下，脚本变量将按照它们在脚本中定义的顺序在表单中排序。`field_order`可以定义为字段名称的可迭代项，以确定在默认的“脚本数据”组内渲染变量的顺序。未包含在此可迭代项中的任何字段将在最后列出。如果定义了`fieldsets`，则将忽略`field_order`。默认情况下，用户界面中将添加一个名为“脚本执行参数”的字段集组。

### `fieldsets`

`fieldsets`可以定义为字段组和它们的字段名称的可迭代项，以确定分组和呈现变量的顺序。未包含在此可迭代项中的任何字段将不会显示在表单中。如果定义了`fieldsets`，则将忽略`field_order`。默认情况下，用户界面中将添加一个名为“脚本执行参数”的字段集组。

以下是一个示例字段集定义：

```python
class MyScript(Script):
    class Meta:
        fieldsets = (
            ('第一组', ('field1', 'field2', 'field3')),
            ('第二组', ('field4', 'field5')),
        )
```

### `commit_default`

执行脚本时提交数据库更改的复选框默认为选中状态。将`commit_default`设置为脚本的Meta类下的False，以使此选项默认未选中。

```python
commit_default = False
```

### `scheduling_enabled`

默认情况下，可以安排以后执行脚本。将`scheduling_enabled`设置为False将禁用此功能：只能进行即时执行。（这还会禁用设置重复执行间隔的功能。）

### `job_timeout`

设置脚本的最大允许运行时间。如果未设置，将使用`RQ_DEFAULT_TIMEOUT`。

## 访问请求数据

可以使用实例属性`self.request`访问当前HTTP请求的详细信息（用于执行脚本的请求）。这可用于推断执行脚本的用户以及客户端IP地址：

```python
username = self.request.user.username
ip_address = self.request.META.get('HTTP_X_FORWARDED_FOR') or \
    self.request.META.get('REMOTE_ADDR')
self.log_info(f"以用户{username}（IP：{ip_address}）身份运行...")
```

有关可用请求参数的完整列表，请参阅[Django文档](https://docs.djangoproject.com/en/stable/ref/request-response/)。

## 从文件中读取数据

Script类提供了两个方便的方法，用于从文件中读取数据：

* `load_yaml`
* `load_json`

这两种方法将分别从本地路径（即`SCRIPTS_ROOT`）内的文件中加载YAML或JSON格式的数据。

## 记录

Script对象提供了一组方便的函数，用于记录不同严重程度级别的消息：

* `log_debug`
* `log_success`
* `log_info`
* `log_warning`
* `log_failure`

在执行脚本时，日志消息将返回给用户。支持对日志消息进行Markdown渲染。

## 更改日志

要在编辑现有对象时生成正确的更改日志数据，必须在对对象进行任何更改之前拍摄对象的快照。

```python
if obj.pk and hasattr(obj, 'snapshot'):
    obj.snapshot()

obj.property = "新值"
obj.full_clean()
obj.save()
```

## 错误处理

有时候事情会出错，脚本可能会遇到`Exception`异常。如果发生这种情况，自定义脚本引发未捕获的异常，执行将中止并报告完整的堆栈跟踪。

虽然这对于调试很有帮助，但在某些情况下，可能需要干净地中止自定义脚本的执行（例如，因为输入数据无效），从而确保不对数据库执行任何更改。在这种情况下，脚本可以引发`AbortScript`异常，这将阻止报告堆栈跟踪，但仍终止脚本的执行并报告给定的错误消息。

```python
from utilities.exceptions import AbortScript

if some_error:
    raise AbortScript("一些有意义的错误消息")
```

## 变量参考

### 默认选项

所有自定义脚本变量支持以下默认选项：

* `default` - 字段的默认值
* `description` - 字段的简要用户友好描述
* `label` - 在渲染的表单中显示的字段名称
* `required` - 指示字段是否为必填项（所有字段默认为必填项）
* `widget` - 要使用的表单小部件的类（请参阅[Django文档](https://docs.djangoproject.com/en/stable/ref/forms/widgets/)）

### StringVar

存储一串字符（即文本）。选项包括：

* `min_length` - 字符的最小数量
* `max_length` - 字符的最大数量
* `regex` - 提供的值必须与之匹配的正则表达式

请注意，`min_length` 和 `max_length` 可以设置为相同的数字，以实现固定长度字段。

### TextVar

任意长度的文本。呈现为多行文本输入字段。

### IntegerVar

存储数字整数。选项包括：

* `min_value` - 最小值
* `max_value` - 最大值

### BooleanVar

一个真/假标志。此字段除了上面列出的默认选项外，没有其他选项。

### ChoiceVar

用户可以从中选择一个选项的一组选择。

* `choices` - 表示可用选项的`(value, label)`元组列表。例如：

```python
CHOICES = (
    ('n', '北'),
    ('s', '南'),
    ('e', '东'),
    ('w', '西')
)

direction = ChoiceVar(choices=CHOICES)
```

在上面的示例中，选择标记为"北"的选项将提交值`n`。

### MultiChoiceVar

类似于`ChoiceVar`，但允许选择多个选项。

### ObjectVar

NetBox中的特定对象。每个ObjectVar必须指定特定的模型，并允许用户选择可用实例之一。ObjectVar接受以下参数。

* `model` - 模型类
* `query_params` - 在检索可用选项时使用的查询参数字典（可选）
* `null_option` - 表示“null”或空选项的标签（可选）

要在列表中限制可用选择，可以将其他查询参数作为`query_params`字典传递。例如，仅显示具有“active”状态的设备：

```python
device = ObjectVar(
    model=Device,
    query_params={
        'status': 'active'
    }
)
```

可以通过将列表分配给字典键来指定多个值。还可以通过在变量名称前加上美元符号（`$`）引用表单中其他字段的值。

```python
region = ObjectVar(
    model=Region
)
site = ObjectVar(
    model=Site,
    query_params={
        'region_id': '$region'
    }
)
```

### MultiObjectVar

类似于`ObjectVar`，但允许选择多个对象。

### FileVar

已上传的文件。请注意，上传的文件仅在脚本执行期间存在于内存中：它们不会自动保存供将来使用。脚本负责在必要时将文件内容写入磁盘。

### IPAddressVar

IPv4或IPv6地址，不带掩码。返回一个`netaddr.IPAddress`对象。

### IPAddressWithMaskVar

带有掩码的IPv4或IPv6地址。返回包括掩码的`netaddr.IPNetwork`对象。

### IPNetworkVar

带有掩码的IPv4或IPv6网络。返回一个包括掩码的`netaddr.IPNetwork`对象。可以使用两个属性来验证提供的掩码：

* `min_prefix_length` - 掩码的最小长度
* `max_prefix_length` - 掩码的最大长度

## 运行自定义脚本

!!! 注意
    要运行自定义脚本，用户必须通过`Extras > Script`、`Extras > ScriptModule`和`Core > ManagedFile`对象的权限分配。他们还必须分配`extras.run_script`权限。这可以通过在Script对象上分配用户（或组）权限，并在管理UI中指定`run`操作来实现，如下所示。

    ![将“run”操作添加到权限](../media/admin_ui_run_permission.png)

### 通过Web UI

可以通过导航到脚本、填写任何必要的表单数据并单击“运行脚本”按钮来通过Web UI运行自定义脚本。可以计划在将来的指定时间执行脚本。可以通过删除关联的作业结果对象来取消计划的脚本。

### 通过API

要通过REST API运行脚本，请发出POST请求到脚本的端点，指定表单数据和提交。例如，要运行名为`example.MyReport`的脚本，我们可以进行以下请求：

```no-highlight
curl -X POST \
-H "Authorization: Token $TOKEN" \
-H "Content-Type: application/json" \
-H "Accept: application/json; indent=4" \
http://netbox/api/extras/scripts/example.MyReport/ \
--data '{"data": {"foo": "somevalue", "bar": 123}, "commit": true}'
```

还可以在表单数据中传递`schedule_at`，并附带日期时间字符串，以在指定的日期和时间计划脚本。

### 通过CLI

可以通过调用管理命令在CLI上运行脚本：

```
python3 manage.py runscript [--commit] [--loglevel {debug,info,warning,error,critical}] [--data "<data>"] <module>.<script>
```

所需的`<module>.<script>`参数是要运行的脚本，其中`<module>`是`scripts`目录中的Python文件的名称，不包括`.py`扩展名，`<script>`是要运行的`<module>`中的脚本类的名称。

可选的`--data "<data>"`参数是要发送到脚本的数据。

可选的`--loglevel`参数是要输出到控制台的所需日志级别。

可选的`--commit`参数将提交脚本中的任何更改到数据库。

## 示例

以下是一个示例脚本，用于为计划的站点创建新对象。用户需要输入三个变量：

* 新站点的名称
* 设备型号（已定义设备类型的筛选列表）
* 要创建的访问交换机数量

这些变量以Web表单的形式呈现给用户。一旦提交，将调用脚本的`run()`方法来创建适当的对象。

```python
from django.utils.text import slugify

from dcim.choices import DeviceStatusChoices, SiteStatusChoices
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from extras.scripts import *


class NewBranchScript(Script):

    class Meta:
        name = "新分支"
        description = "为新分支站点进行配置"
        field_order = ['site_name', 'switch_count', 'switch_model']

    site_name = StringVar(
        description="新站点的名称"
    )
    switch_count = IntegerVar(
        description="要创建的访问交换机数量"
    )
    manufacturer = ObjectVar(
        model=Manufacturer,
        required=False
    )
    switch_model = ObjectVar(
        description="访问交换机型号",
        model=DeviceType,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    def run(self, data, commit):

        # 创建新站点
        site = Site(
            name=data['site_name'],
            slug=slugify(data['site_name']),
            status=SiteStatusChoices.STATUS_PLANNED
        )
        site.full_clean()
        site.save()
        self.log_success(f"创建新站点：{site}")

        # 创建访问交换机
        switch_role = DeviceRole.objects.get(name='访问交换机')
        for i in range(1, data['switch_count'] + 1):
            switch = Device(
                device_type=data['switch_model'],
                name=f'{site.slug}-switch{i}',
                site=site,
                status=DeviceStatusChoices.STATUS_PLANNED,
                role=switch_role
            )
            switch.full_clean()
            switch.save()
            self.log_success(f"创建新交换机：{switch}")

        # 生成新设备的CSV表格
        output = [
            '名称,制造商,型号'
        ]
        for switch in Device.objects.filter(site=site):
            attrs = [
                switch.name,
                switch.device_type.manufacturer.name,
                switch.device_type.model
            ]
            output.append(','.join(attrs))

        return '\n'.join(output)
```

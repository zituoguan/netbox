# 仪表板小部件

每个 NetBox 用户都可以通过添加和删除小部件以及操作每个小部件的大小和位置来自定义自己的个人仪表板。插件可以注册自己的仪表板小部件，以补充已经本地可用的小部件。

## DashboardWidget 类

所有仪表板小部件都必须继承自 NetBox 的 `DashboardWidget` 基类。子类必须提供一个 `render()` 方法，并可以重写基类的默认特性。

需要用户配置的小部件还必须包括一个子类 `ConfigForm`，该子类继承自 `WidgetConfigForm`。此表单用于呈现小部件的用户配置选项。

::: extras.dashboard.widgets.DashboardWidget

## 小部件注册

要注册一个用于在 NetBox 中使用的仪表板小部件，请导入 `register_widget()` 装饰器并使用它来包装每个 `DashboardWidget` 子类：

```python
from extras.dashboard.widgets import DashboardWidget, register_widget

@register_widget
class MyWidget1(DashboardWidget):
    ...

@register_widget
class MyWidget2(DashboardWidget):
    ...
```

## 示例

```python
from django import forms
from extras.dashboard.utils import register_widget
from extras.dashboard.widgets import DashboardWidget, WidgetConfigForm


@register_widget
class ReminderWidget(DashboardWidget):
    default_title = 'Reminder'
    description = 'Add a virtual sticky note'

    class ConfigForm(WidgetConfigForm):
        content = forms.CharField(
            widget=forms.Textarea()
        )

    def render(self, request):
        return self.config.get('content')
```

## 初始化

要注册小部件，导入小部件模块变得非常必要。推荐的做法是在`PluginConfig`中的`ready`方法里完成这个操作：

```python
class FooBarConfig(PluginConfig):
    def ready(self):
        super().ready()
        from . import widgets  # 将此指向你创建的上述小部件模块
```

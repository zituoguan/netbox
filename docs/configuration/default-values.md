# 默认值参数

## DEFAULT_DASHBOARD

此参数控制用户默认仪表板的内容和布局。一旦创建了仪表板，用户可以自由地通过添加、删除和重新配置小部件来自定义它。

此参数必须指定一个字典的可迭代对象，每个字典表示一个独立的仪表板小部件及其配置。支持以下小部件属性：

* `widget`：Python类的点路径（必需）
* `width`：默认小部件宽度（介于1和12之间，包括1和12）
* `height`：默认小部件高度，以行为单位
* `title`：小部件标题
* `color`：小部件标题栏的颜色，以名称指定
* `config`：任何小部件配置参数的字典映射

下面提供了一个简要的示例配置。

```python
DEFAULT_DASHBOARD = [
    {
        'widget': 'extras.ObjectCountsWidget',
        'width': 4,
        'height': 3,
        'title': 'Organization',
        'config': {
            'models': [
                'dcim.site',
                'tenancy.tenant',
                'tenancy.contact',
            ]
        }
    },
    {
        'widget': 'extras.ObjectCountsWidget',
        'width': 4,
        'height': 3,
        'title': 'IPAM',
        'color': 'blue',
        'config': {
            'models': [
                'ipam.prefix',
                'ipam.iprange',
                'ipam.ipaddress',
            ]
        }
    },
]
```

## DEFAULT_USER_PREFERENCES

!!! tip "动态配置参数"

这是一个字典，定义了要为新创建的用户帐户设置的默认首选项。例如，要将所有用户的默认页面大小设置为100，请定义以下内容：

```python
DEFAULT_USER_PREFERENCES = {
    "pagination": {
        "per_page": 100
    }
}
```

有关可用首选项的完整列表，请登录到NetBox，并导航到`/user/preferences/`。首选项名称中的句点表示JSON数据中的嵌套级别。上面的示例映射到`pagination.per_page`。

---

## PAGINATE_COUNT

!!! tip "动态配置参数"

默认值：50

每个对象列表中默认显示的最大对象数。

---

## POWERFEED_DEFAULT_AMPERAGE

!!! tip "动态配置参数"

默认值：15

创建新的电源馈线时，`amperage`字段的默认值。

---

## POWERFEED_DEFAULT_MAX_UTILIZATION

!!! tip "动态配置参数"

默认值：80

创建新的电源馈线时，`max_utilization`字段的默认值（百分比）。

---

## POWERFEED_DEFAULT_VOLTAGE

!!! tip "动态配置参数"

默认值：120

创建新的电源馈线时，`voltage`字段的默认值。

---

## RACK_ELEVATION_DEFAULT_UNIT_HEIGHT

!!! tip "动态配置参数"

默认值：22

机架标高中单位的默认高度（以像素为单位）。为了获得最佳效果，此值应大约是`RACK_ELEVATION_DEFAULT_UNIT_WIDTH`的十分之一。

---

## RACK_ELEVATION_DEFAULT_UNIT_WIDTH

!!! tip "动态配置参数"

默认值：220

机架标高中单位的默认宽度（以像素为单位）。

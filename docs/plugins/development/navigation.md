# 导航

## 菜单

插件可以在NetBox的导航菜单中注册自己的子菜单。这可以通过在`navigation.py`中定义一个名为`menu`的变量，指向`PluginMenu`类的一个实例来完成。每个菜单必须定义一个标签和分组的菜单项（下面讨论），并可以选择指定一个图标。示例如下。

```python title="navigation.py"
from netbox.plugins import PluginMenu

menu = PluginMenu(
    label='My Plugin',
    groups=(
        ('Foo', (item1, item2, item3)),
        ('Bar', (item4, item5)),
    ),
    icon_class='mdi mdi-router'
)
```

请注意，每个组都是一个包含标签和菜单项迭代器的两元组。组的标签用作子菜单中的部分标题。即使只有一个组的项目，也需要一个组标签。

!!! 提示
    菜单类的路径可以通过在PluginConfig实例中设置`menu`来修改。

`PluginMenu`具有以下属性：

| 属性         | 必需     | 描述                                  |
|--------------|----------|--------------------------------------|
| `label`      | 是       | 菜单标题显示的文本                  |
| `groups`     | 是       | 包含菜单项的具名分组的可迭代对象    |
| `icon_class` | -        | 用于标题的图标的CSS名称              |

!!! 提示
    支持的图标可以在[Material Design Icons](https://materialdesignicons.com/)上找到。

### 默认菜单

如果您的插件只有少量菜单项，可能希望使用NetBox的共享“插件”菜单，而不是创建自己的菜单。要实现这一点，只需在`navigation.py`中声明`menu_items`为`PluginMenuItems`列表。列出的项目将出现在“插件”子菜单中以您插件的名称为标题的部分下。

```python title="navigation.py"
menu_items = (item1, item2, item3)
```

!!! 提示
    菜单项列表的路径可以通过在PluginConfig实例中设置`menu_items`来修改。

## 菜单项

每个菜单项表示一个链接和（可选）一组按钮，构成了NetBox导航菜单中的一个条目。菜单项被定义为PluginMenuItem实例。示例如下。

```python title="navigation.py"
from netbox.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

item1 = PluginMenuItem(
    link='plugins:myplugin:myview',
    link_text='Some text',
    buttons=(
        PluginMenuButton('home', 'Button A', 'fa fa-info', ButtonColorChoices.BLUE),
        PluginMenuButton('home', 'Button B', 'fa fa-warning', ButtonColorChoices.GREEN),
    )
)
```

`PluginMenuItem`具有以下属性：

| 属性         | 必需     | 描述                                                              |
|--------------|----------|------------------------------------------------------------------|
| `link`      | 是       | 链接到此菜单项的URL路径的名称。                                   |
| `link_text`   | 是       | 呈现给用户的文本。                                               |
| `permissions` | -        | 显示此链接所需的权限列表。                                      |
| `staff_only`  | -        | 仅显示`is_staff`设置为True的用户（还需要指定的权限）             |
| `buttons`     | -        | 包含在内的PluginMenuButton实例的可迭代对象，用于包括在内 |

!!! info "staff_only"属性在NetBox v3.6.1中引入。

## 菜单按钮

每个菜单项都可以包括一组按钮。这对于提供与菜单项相关的快捷方式非常有用。例如，NetBox的导航菜单中的大多数项目都包括用于创建和导入新对象的按钮。

`PluginMenuButton`具有以下属性：

| 属性         | 必需     | 描述                                        |
|--------------|----------|--------------------------------------------|
| `link`      | 是       | 此按钮链接到的URL路径的名称。                |
| `title`       | 是       | 提示文本（当鼠标悬停在按钮上时显示）。     |
| `icon_class`  | 是       | 按钮图标的CSS类。                            |
| `color`       | -        | `ButtonColorChoices`提供的选择之一。          |
| `permissions` | -        | 显示此按钮所需的权限列表。                  |

在菜单项中关联的任何按钮将仅在用户有权查看链接时显示，而不管按钮上设置了哪些权限。

!!! 提示
    支持的图标可以在[Material Design Icons](https://materialdesignicons.com/)上找到。

# 国际化

从NetBox v4.0开始，NetBox将利用[Django的自动翻译](https://docs.djangoproject.com/en/stable/topics/i18n/translation/)来支持除英语以外的语言。本页详细介绍了需要特别注意以确保翻译支持正常工作的项目部分。简要来说，这些项目包括：

* 每个模型的`verbose_name`和`verbose_name_plural`元属性
* 每个模型字段的`verbose_name`和（如果已定义）`help_text`
* 每个表单字段的`label`
* 每个表单类的`fieldsets`头部
* 每个表格列的`verbose_name`
* 模板中的所有可读字符串必须用`{% trans %}`或`{% blocktrans %}`包装起来

本文其余部分详细阐述了上述每一项。

## 一般指导

* 使用Django的`gettext()`或`gettext_lazy()`实用工具函数包装可读字符串，以启用自动翻译。通常，首选`gettext_lazy()`（有时必需）以推迟翻译，直到显示字符串。

* 根据约定，首选的翻译函数通常被导入为下划线（`_`），以最小化样板代码。因此，您通常会看到翻译如`_("Some text")`。仍然可以导入和使用替代翻译函数（例如`pgettext()`和`ngettext()`）根据需要正常使用。

* 在可能的情况下避免传递标记和其他非自然语言。通过翻译函数包装的所有内容都会导出到消息文件中，供人工翻译使用。

* 对于翻译的字符串的意图可能不明显的情况，使用`pgettext()`或`pgettext_lazy()`包含协助上下文以供翻译人员使用。例如：

    ```python
    # 上下文，字符串
    pgettext("月份名称", "五月")
    ```

* **格式字符串不支持翻译。** 对于必须支持翻译的消息，避免使用"f"字符串。而是使用`format()`来实现变量替换：

    ```python
    # 翻译不会起作用
    f"有{count}个对象"
    
    # 改用以下方式
    "有{count}个对象".format(count=count)
    ```

## 模型

1. 导入`gettext_lazy`为`_`。
2. 确保在模型的`Meta`类下定义`verbose_name`和`verbose_name_plural`并用`gettext_lazy()`快捷方式包装。
3. 确保每个模型字段指定用`gettext_lazy()`包装的`verbose_name`。
4. 确保在模型字段上的任何`help_text`属性也用`gettext_lazy()`包装。

```python
from django.utils.translation import gettext_lazy as _

class Circuit(PrimaryModel):
    commit_rate = models.PositiveIntegerField(
        ...
        verbose_name=_('commit rate (Kbps)'),
        help_text=_("Committed rate")
    )

    class Meta:
        verbose_name = _('circuit')
        verbose_name_plural = _('circuits')
```

## 表单

1. 导入`gettext_lazy`为`_`。
2. 所有表单字段必须指定用`gettext_lazy()`包装的`label`。
3. 在表单的`fieldsets`属性下的所有标题必须用`gettext_lazy()`包装。

```python
from django.utils.translation import gettext_lazy as _

class CircuitBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Description'),
        ...
    )

    fieldsets = (
        (_('Circuit'), ('provider', 'type', 'status', 'description')),
    )
```

## 表格

1. 导入`gettext_lazy`为`_`。
2. 所有表格列必须指定用`gettext_lazy()`包装的`verbose_name`。

```python
from django.utils.translation import gettext_lazy as _

class CircuitTable(TenancyColumnsMixin, ContactsColumnMixin, NetBoxTable):
    provider = tables.Column(
        verbose_name=_('Provider'),
        ...
    )
```

## 模板

1. 确保在模板顶部包含`{% load i18n %}`以启用翻译支持。
2. 使用[`{% trans %}`](https://docs.djangoproject.com/en/stable/topics/i18n/translation/#translate-template-tag)标签（简称为“translate”）包装短字符串。
3. 可以使用[`{% blocktrans %}`](https://docs.djangoproject.com/en/stable/topics/i18n/translation/#blocktranslate-template-tag)标签和`{% endblocktrans %}`标签包围较长的字符串，以提高可读性并启用变量替换。 （记得包括`trimmed`参数以在标签之间修剪空格。）
4. 在可能的情况下，避免在翻译字符串中传递HTML，因为这可能会增加翻译人员需要开发消息映射的工作量。

```
{% load i18n %}

{# 短字符串 #}
<h5 class="card-header">{% trans "Circuit List" %}</h5>

{# 带有上下文变量的较长字符串 #}
{% blocktrans trimmed with count=object.circuits.count %}
  有{count}个电路。您想继续吗？
{% endblocktrans %}
```

!!! 警告
    `{% blocktrans %}`标签仅支持**有限的变量替换**，与Python字符串上的`format()`方法相当。它不允许访问对象属性或在其中使用其他模板标签或过滤器。确保将任何必要的上下文作为简单变量传递。

!!! 信息
    `{% trans %}`和`{% blocktrans %}`支持使用`context`参数包括翻译者使用的上下文提示：

    ```nohighlight
    {% trans "May" context "month name" %}
    ```

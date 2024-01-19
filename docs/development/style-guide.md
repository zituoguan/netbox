# 风格指南

NetBox通常遵循[Django风格指南](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/)，这本身是基于[PEP 8](https://www.python.org/dev/peps/pep-0008/)的。[Pycodestyle](https://github.com/pycqa/pycodestyle)用于验证代码格式，忽略某些违规情况。

## 代码

### 一般指导

* 如果有疑虑，保持一致性：保持一致性不正确总是比不一致性正确要好。如果在无关的工作中注意到应该纠正的模式，请继续遵循当前的模式，并提交一个单独的错误报告，以便在以后的某个时间点评估整个代码库。

* 优先考虑可读性而不是简洁性。Python是一种非常灵活的语言，通常提供了多种表达给定逻辑的选项，但有些可能对读者更友好。 （列表理解特别容易被过度优化。）始终要考虑到未来的读者可能需要在没有您编写代码的上下文的情况下解释您的代码。

* 在每个文件的末尾包含一个换行符。

* 没有彩蛋。虽然它们可能很有趣，但NetBox必须被视为一种业务关键的工具。不必要代码引入错误的潜力（尽管很小），最好完全避免。

* 常量（不变的变量）应在每个应用的`constants.py`中声明。从文件进行通配符导入是可以接受的。

* 每个模型必须有[文档字符串](https://peps.python.org/pep-0257/)。每个自定义方法都应包含其功能的解释。

* 嵌套API序列化器生成对象的最小表示。这些存储在主要序列化器之外，以避免循环依赖。始终直接从其他应用程序导入嵌套的序列化器。例如，从DCIM应用程序中，您会编写`from ipam.api.nested_serializers import NestedIPAddressSerializer`。

### PEP 8的例外

NetBox忽略了某些PEP8断言。这些列在下面。

#### 通配符导入

通配符导入（例如，`from .constants import *`）在满足以下任何条件时都是可以接受的：

* 被导入的库仅包含常量声明（例如，`constants.py`）
* 被导入的库显式定义`__all__`

#### 最大行长度（E501）

NetBox不限制行的最大长度为79个字符。我们使用最大行长度为120个字符，但CI不强制执行此限制。最大长度不适用于HTML模板或自动生成的代码（例如，数据库迁移）。

#### 二元运算符后面的换行符（W504）

允许在二元运算符后面换行。

### 强制执行代码样式

CI过程使用[`pycodestyle`](https://pypi.org/project/pycodestyle/)工具（以前是`pep8`）来强制执行代码样式。NetBox附带了一个[pre-commit钩子](./getting-started.md#2-enable-pre-commit-hooks)，用于自动运行此操作。要手动调用`pycodestyle`，请运行：

```
pycodestyle --ignore=W504,E501 netbox/
```

### 引入新依赖项

最好避免引入新的依赖项，除非绝对必要。对于小功能，通常最好在NetBox代码库内部复制功能，而不是引入对外部项目的依赖。这减少了跟踪新版本和暴露于外部错误和供应链攻击的风险。

如果有充分的理由引入新的依赖项，它必须满足以下条件：

* 其完整的源代码必须已发布，并且可在无需注册的情况下免费访问。
* 其许可证必须有助于包含在开源项目中。
* 它必须得到积极维护，发布之间的时间不能超过一年。
* 它必须通过[Python包索引](https://pypi.org/)（PyPI）提供。

在添加新依赖项时，必须将该软件包的简短描述和其代码存储库的URL添加到`base_requirements.txt`中。此外，必须在`requirements.txt`中添加一行，指定将包名称固定到当前稳定版本。这确保NetBox仅安装已知的好版本。

## 文档

### 一般指导

* 书面材料必须始终符合合理的专业标准，具有正确的语法、拼写和标点符号。

* 段落之间使用两个换行符。

* 在句子之间只使用一个空格。

* 所有文档必须以[Markdown](../reference/markdown.md)编写，其中允许在需要时使用适度的HTML来克服技术限制。

### 品牌

* 在书写时，引用NetBox时，请使用正确的形式“NetBox”，其中N和B大写。小写形式“netbox”应用于代码、文件名等，但永远不要使用“Netbox”或其他任何偏差。

* NetBox的标志有一个SVG形式，位于[docs/netbox_logo.svg](../netbox_logo.svg)。最好为所有目的使用此标志，因为它可以在不损失分辨率的情况下缩放到任意大小。如果需要栅格图像，则应将SVG标志转换为规定大小的PNG图像。

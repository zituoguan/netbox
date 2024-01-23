# 暂存更改

!!! 危险 "实验性功能"
    此功能仍在积极开发中，被视为实验性质的功能。目前强烈不建议在生产环境中使用它。

NetBox提供了一种编程API，用于暂存对象的创建、修改和删除，而不实际将这些更改提交到活动数据库。这对于执行批量操作的“干跑”或准备一组更改以供管理审批等情况非常有用。

要开始暂存更改，首先创建一个[分支](../../models/extras/branch.md)：

```python
from extras.models import Branch

branch1 = Branch.objects.create(name='branch1')
```

然后，使用`checkout()`上下文管理器激活分支并开始进行更改。这会启动一个新的数据库事务。

```python
from extras.models import Branch
from netbox.staging import checkout

branch1 = Branch.objects.get(name='branch1')
with checkout(branch1):
    Site.objects.create(name='New Site', slug='new-site')
    # ...
```

退出上下文后，数据库事务将自动回滚，并记录您的更改为[暂存更改](../../models/extras/stagedchange.md)。重新进入分支将触发一个新的数据库事务，并自动应用与分支相关联的任何暂存更改。

要在分支内应用更改，请调用分支的`commit()`方法：

```python
from extras.models import Branch

branch1 = Branch.objects.get(name='branch1')
branch1.commit()
```

提交分支是一个全有或全无的操作：任何异常都会还原整套更改。成功提交分支后，所有与其关联的StagedChange对象都将自动删除（但分支本身将保留，可以重用）。

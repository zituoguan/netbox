# 站点

您在建模网络时如何使用站点可能会因您的组织性质而异，但通常一个站点将等同于一个建筑物或校园。例如，一家银行连锁公司可能会创建一个站点来代表其每个分支机构，为其总部创建一个站点，并为其在两个网络数据中心设施中的存在创建另外两个站点。

## 字段

### 名称

站点的唯一名称。

### Slug

唯一的URL友好标识符。（可以用于过滤）

### 状态

站点的运营状态。

!!! 提示
    通过在[`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices)配置参数下设置`Site.status`，可以定义其他状态。

### 区域

站点所属的父[区域](./region.md)，如果有的话。

### 设施

用于识别站点的数据中心或设施指定。

### AS号

每个站点可以分配多个[AS号](../ipam/asn.md)。

### 时区

站点的本地时区。（时区由[zoneinfo](https://docs.python.org/3/library/zoneinfo.html)库提供。）

### 物理地址

站点的物理地址，用于地图。

### 发货地址

用于寄往站点的交付的地址。

!!! 提示
    您还可以为每个站点指定[联系点](../../features/contacts.md)以提供额外的联系方式。

### 纬度和经度

站点的GPS坐标，用于地理定位。
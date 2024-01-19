# VLANs

虚拟局域网（VLAN）表示一个隔离的第二层域，由名称和数字ID（1-4094）标识，如[IEEE 802.1Q](https://en.wikipedia.org/wiki/IEEE_802.1Q)中定义。VLAN被安排到[VLAN组](./vlangroup.md)中以定义范围并强制唯一性。

## 字段

### ID

VLAN的12位数字ID，范围为1-4094（包括）。

### 名称

配置的VLAN名称。

### 状态

VLAN的运行状态。

!!! tip
    可以通过在[`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices)配置参数下设置`VLAN.status`来定义其他状态。

### 角色

分配给VLAN的用户定义的功能[角色](./role.md)。

### VLAN组或站点

VLAN分配到的[VLAN组](./vlangroup.md)或[站点](../dcim/site.md)。

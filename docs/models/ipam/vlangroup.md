# VLAN组

VLAN组可用于组织NetBox中的[VLAN](./vlan.md)。每个VLAN组可以范围到特定的[区域](../dcim/region.md)、[站点组](../dcim/sitegroup.md)、[站点](../dcim/sitegroup.md)、[位置](../dcim/location.md)、[机架](../dcim/rack.md)、[集群组](../virtualization/clustergroup.md)或[集群](../virtualization/cluster.md)。成员VLAN将可用于分配给指定范围内的设备和/或虚拟机。

组还可以用于强制唯一性：组中的每个VLAN必须具有唯一的ID和名称。未分配给组的VLAN可以具有重叠的名称和ID（包括属于共同站点的VLAN）。例如，可以创建两个具有ID 123的VLAN，但它们不能都分配给同一个组。

## 字段

### 名称

唯一的人类友好名称。

### Slug

唯一的URL友好标识符。（此值可用于过滤。）

### 最小和最大VLAN ID

必须为每个组设置一个最小和最大的子VLAN ID。（这些默认分别为1和4094。）在组内创建的VLAN必须具有落在这些值之间的VID（包括在内）。

### 范围

VLAN组覆盖的域，定义为受支持的对象类型之一。这传达了VLAN组适用的上下文。

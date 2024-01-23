# 集群

集群是物理资源的逻辑分组，用于其中运行[虚拟机](./virtualmachine.md)。物理[设备](../dcim/device.md)可以与集群关联为主机。这允许用户跟踪特定虚拟机可能驻留在哪台主机上。

## 字段

### 名称

集群的人类友好名称。必须在分配的组和站点内唯一。

### 类型

分配给该集群的[集群类型](./clustertype.md)。

### 组

该集群所属的[集群组](./clustergroup.md)。

### 状态

集群的运行状态。

!!! tip
    可以通过设置 [`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices) 配置参数下的 `Cluster.status` 来定义附加的状态。

### 站点

集群关联的[站点](../dcim/site.md)。
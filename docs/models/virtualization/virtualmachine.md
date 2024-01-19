# 虚拟机

虚拟机（VM）代表托管在[集群](./cluster.md)内的虚拟计算实例。每个虚拟机必须分配到一个[站点](../dcim/site.md)和/或集群，并可以选择分配给集群内的特定主机[设备](../dcim/device.md)。

虚拟机可以分配虚拟[接口](./vminterface.md)，但不支持任何物理组件。当虚拟机具有一个或多个分配了IP地址的接口时，可以为设备指定IPv4和IPv6的主要IP。

## 字段

### 名称

虚拟机的配置名称。必须对分配给的集群和租户唯一。

### 角色

分配给虚拟机的功能[角色](../dcim/devicerole.md)。

### 状态

虚拟机的运行状态。

!!! tip
    通过在[`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices)配置参数下设置`VirtualMachine.status`，可以定义附加状态。

### 站点和集群

分配给虚拟机的[站点](../dcim/site.md)和/或[集群](./cluster.md)。

### 设备

分配给虚拟机的所在站点/集群内的物理主机[设备](../dcim/device.md)。

### 平台

虚拟机可以与特定[平台](../dcim/platform.md)关联，表示其操作系统。

### 主要IPv4和IPv6地址

每个虚拟机可以为管理目的指定一个主要的IPv4地址和/或一个主要的IPv6地址。

!!! tip
    NetBox默认情况下会优先使用IPv6地址而不是IPv4地址。可以通过设置`PREFER_IPV4`配置参数来更改这一点。

### vCPU

分配的虚拟CPU数。可以分配部分vCPU计数（例如1.5个vCPU）。

### 内存

分配的运行内存量，以兆字节为单位。

### 磁盘

分配的磁盘存储量，以千兆字节为单位。

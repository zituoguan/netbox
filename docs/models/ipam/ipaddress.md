# IP地址

NetBox中的IP地址对象包括一个单一的主机地址（IPv4或IPv6）及其子网掩码，表示配置在网络接口上的IP地址。IP地址可以分配给[设备](../dcim/device.md)和[虚拟机](../virtualization/virtualmachine.md)接口，以及[FHRP组](./fhrpgroup.md)。此外，每个设备和虚拟机可以为每个地址族（IPv4和IPv6各一个）中的一个接口IP指定为其主IP。

!!! tip
    当为IPv4和IPv6分别设置主IP时，NetBox将首选IPv6。可以通过设置`PREFER_IPV4`配置参数来更改这个设置。

## 网络地址转换（NAT）

一个IP地址可以被指定为另一个IP地址的网络地址转换（NAT）内部IP地址，这对于表示公网和私网IP地址之间的转换非常有用。这种关系在两个方向上都适用：例如，如果将10.0.0.1分配为192.0.2.1的内部IP，那么10.0.0.1将显示为192.0.2.1的外部IP。

!!! note
    NetBox目前不支持跟踪应用级NAT关系（也称为_端口地址转换_或PAT）。这种类型的策略需要额外的逻辑来建模，不能仅通过IP地址来完全表示。

## 字段

### 地址

IPv4或IPv6地址和掩码，使用CIDR表示法（例如`192.0.2.0/24`）。

### 状态

IP地址的操作状态。

!!! tip
    通过设置`ipam.IPAddress.status`在[`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices)配置参数下，可以定义其他状态。

### 角色

此IP地址所履行的功能角色。选项包括：

* **环回：** 配置在回环接口上
* **次要：** 配置在接口上的多个IP地址之一
* **任播：** 用于任播服务
* **VIP：** 通用虚拟IP地址
* **VRRP：** 使用VRRP协议管理的虚拟IP地址
* **HSRP：** 使用HSRP协议管理的虚拟IP地址
* **GLBP：** 使用GLBP协议管理的虚拟IP地址
* **CARP：** 使用CARP协议管理的虚拟IP地址

!!! tip
    虚拟IP地址应分配给[FHRP组](./fhrpgroup.md)，而不是分配给实际接口，以准确地建模它们的共享性质。

### VRF

此IP地址存在的[虚拟路由和转发](./vrf.md)实例。

!!! note
    VRF分配是可选的。未分配VRF的IP地址被认为存在于“全局”表中。

### DNS名称

与此IP地址关联的DNS A/AAAA记录值。

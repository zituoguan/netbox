# IP地址范围

这个模型表示一段任意的IPv4或IPv6地址范围，包括其起始和结束地址。例如，范围从192.0.2.10到192.0.2.20有11个成员。（总成员数可以作为IPRange实例的`size`属性获得。）与[前缀](./prefix.md)和[IP地址](./ipaddress.md)一样，每个IP范围都可以选择分配到一个[VRF](./vrf.md)。

## 字段

### VRF

此IP范围存在的[虚拟路由和转发](./vrf.md)实例。

!!! note
    VRF分配是可选的。未分配VRF的IP范围被认为存在于“全局”表中。

### 起始和结束地址

定义范围边界的起始和结束IP地址（包括在内）。两个IP地址都必须指定正确的掩码。

!!! note
    IP范围的最大支持大小是2^32 - 1。

### 角色

分配给IP范围的用户定义功能[角色](./role.md)。

### 状态

IP范围的操作状态。请注意，范围的状态不会影响其成员IP地址，这些地址可以独立定义其状态。

!!! tip
    通过设置`IPRange.status`在[`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices)配置参数下，可以定义其他状态。

### 标记为已利用

如果启用，IP范围将被视为100%利用，而不管其中定义了多少个IP地址。这对于记录DHCP范围等情况非常有用。

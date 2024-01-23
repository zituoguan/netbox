# L2VPN

NetBox中的L2VPN对象是对层2桥接技术的表示，例如VXLAN、VPLS或EPL。每个L2VPN可以通过名称以及可选的唯一标识符（例如VNI）来识别。创建后，L2VPN可以终止到[接口](../dcim/interface.md)和[VLAN](../ipam/vlan.md)。

## 字段

### 名称

唯一的人性化名称。

### Slug

唯一的URL友好标识符。（可用于过滤的值。）

### 类型

用于形成和操作L2VPN的技术。选择包括：

* VPLS
* VPWS
* EPL
* EVPL
* EP-LAN
* EVP-LAN
* EP-TREE
* EVP-TREE
* VXLAN
* VXLAN-EVPN
* MPLS-EVPN
* PBB-EVPN

!!! 注意
    将类型指定为VPWS、EPL、EP-LAN、EP-TREE将限制L2VPN实例的终止到两个点。

### 标识符

可选的数字标识符。这可用于跟踪伪线ID，例如。

### 导入和导出目标

与此L2VPN相关联的[路由目标](../ipam/routetarget.md)，用于控制转发信息的导入和导出。

# FHRP组

第一跳冗余协议（FHRP）使多个物理接口以冗余的方式呈现虚拟[IP地址](./ipaddress.md)（VIP）。此类协议的示例包括：

* [热备份路由器协议](https://en.wikipedia.org/wiki/Hot_Standby_Router_Protocol)（HSRP）
* [虚拟路由器冗余协议](https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol)（VRRP）
* [通用地址冗余协议](https://en.wikipedia.org/wiki/Common_Address_Redundancy_Protocol)（CARP）
* [网关负载均衡协议](https://en.wikipedia.org/wiki/Gateway_Load_Balancing_Protocol)（GLBP）

在创建新的FHRP组时，用户可以选择创建一个VIP。此IP地址将自动分配给新组。（虚拟IP地址也可以在创建组后分配。）

## 字段

### 协议

协作服务器用于维护组的虚拟[IP地址（S）](./ipaddress.md)的传输协议。

### 组ID

组的数字标识符。

### 名称

FHRP组的可选名称。

### 认证类型

组节点使用的认证类型，如果有的话。

### 认证密钥

组认证使用的共享密钥，如果有的话。

!!! 警告
    认证密钥值以明文存储在NetBox的数据库中。如果您需要对共享密钥进行静态加密，请不要使用此字段。

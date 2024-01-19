# 隧道

隧道表示通过使用协议封装在共享基础设施之间建立的两个或多个端点之间的私有虚拟连接。常见的封装技术包括[通用路由封装（GRE）](https://en.wikipedia.org/wiki/Generic_Routing_Encapsulation)、[IP-in-IP](https://en.wikipedia.org/wiki/IP_in_IP)和[IPSec](https://en.wikipedia.org/wiki/IPsec)。NetBox支持建模点对点和集线器与分支的隧道拓扑。

通过创建[隧道终止](./tunneltermination.md)，可以将设备和虚拟机接口与隧道关联。

## 字段

### 名称

用于标识隧道的唯一名称。

### 状态

隧道的操作状态。默认情况下，以下状态是可用的：

* 已计划
* 活动
* 禁用

!!! tip "自定义隧道状态"
    可以通过在[`FIELD_CHOICES`](../../configuration/data-validation.md#field_choices)配置参数下设置`Tunnel.status`来定义其他隧道状态。

### 组

将此隧道分配给的[管理组](./tunnelgroup.md)（可选）。

### 封装

用于建立隧道的封装协议或技术。NetBox支持GRE、IP-in-IP和IPSec封装。

### 隧道ID

隧道的可选数值标识符。

### IPSec配置文件

对于IPSec隧道，这是用于协商安全关联的[IPSec配置文件](./ipsecprofile.md)。

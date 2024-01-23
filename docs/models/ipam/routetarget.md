# 路由目标

路由目标是一种特殊类型的[扩展BGP社区](https://tools.ietf.org/html/rfc4360#section-4)，用于控制网络中VRF表之间的路由重新分发。在NetBox中，可以将路由目标分配给单个VRF，用作导入目标、导出目标（或两者都是），以在L3VPN中模拟此交换。每个路由目标都必须具有唯一的名称，该名称应按照[第4364号RFC](https://tools.ietf.org/html/rfc4364#section-4.2)中规定的格式，类似于VR路由区分器。

## 字段

### 名称

符合[第4360号RFC](https://tools.ietf.org/html/rfc4360#section-4)的路由目标标识符。

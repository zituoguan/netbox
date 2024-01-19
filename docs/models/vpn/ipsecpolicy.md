# IPSec策略

[IPSec](https://en.wikipedia.org/wiki/IPsec)策略定义了在形成IPSec隧道时要使用的一组[提议](./ikeproposal.md)。还可以选择性地定义完美前向保密性（PFS）组。这些策略被[IPSec配置文件](./ipsecprofile.md)引用。

## 字段

### 名称

策略的唯一用户分配的名称。

### 提议

策略支持使用的一个或多个[IPSec提议](./ipsecproposal.md)。

### PFS组

策略支持的[完美前向保密性（PFS）](https://en.wikipedia.org/wiki/Forward_secrecy)组（可选）。

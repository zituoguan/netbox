# ASNs

自治系统号（ASN）是用于BGP协议的数值标识符，用于识别特定前缀是从哪个[自治系统](https://en.wikipedia.org/wiki/Autonomous_system_%28Internet%29)发起并通过的。NetBox支持32位和64位ASN。

ASN在NetBox内必须是全局唯一的，并可以从[定义的范围](./asnrange.md)分配。每个ASN可以分配给多个[站点](../dcim/site.md)。

## 字段

### AS号码

32位或64位的AS号码。

### RIR

负责分配此特定ASN的[区域互联网注册管理机构](./rir.md)或类似机构。

### 站点

分配给此ASN的[站点](../dcim/site.md)。

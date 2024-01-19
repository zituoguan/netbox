# IKE策略

[IKE（Internet Key Exchange）](https://en.wikipedia.org/wiki/Internet_Key_Exchange)策略定义了在IKE协商中要使用的IKE版本、模式和一组[提议](./ikeproposal.md)。这些策略由[IPSec配置文件](./ipsecprofile.md)引用。

## 字段

### 名称

策略的唯一用户分配的名称。

### 版本

使用的IKE版本（v1或v2）。

### 模式

使用的IKE模式（主要或积极）。

### 提议

支持此策略使用的一个或多个[IKE提议](./ikeproposal.md)。

### 预共享密钥

与此策略关联的预共享秘密密钥（可选）。

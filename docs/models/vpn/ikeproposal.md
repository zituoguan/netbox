# IKE提议

[IKE（Internet Key Exchange）](https://en.wikipedia.org/wiki/Internet_Key_Exchange)提议定义了用于在不受信任的介质（如互联网）上建立安全的双向连接的一组参数。NetBox中定义的IKE提议可以被[IKE策略](./ikepolicy.md)引用，而这些策略则被[IKE配置文件](./ipsecprofile.md)使用。

!!! 注意
    一些平台将IKE提议称为[ISAKMP](https://en.wikipedia.org/wiki/Internet_Security_Association_and_Key_Management_Protocol)，这是一种用于认证和密钥交换的框架，它使用了IKE。

## 字段

### 名称

提议的唯一用户分配的名称。

### 认证方法

用于对IKE对等体进行身份验证的策略。下面列出了可用的选项。

| 名称               |
|------------------|
| 预共享密钥         |
| 证书               |
| RSA签名            |
| DSA签名            |

### 加密算法

用于数据加密的协议。选项包括DES、3DES和各种AES变种。

### 认证算法

用于确保数据完整性的机制。选项包括MD5和SHA HMAC实现。指定认证算法是可选的，因为某些加密算法（例如AES-GCM）在本地提供了认证。

### 组

提议支持的[Diffie-Hellman组](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)。组ID由[IANA](https://www.iana.org/assignments/ikev2-parameters/ikev2-parameters.xhtml#ikev2-parameters-8)管理。

### SA寿命

IKE安全关联（SA）的最大寿命，以秒为单位。

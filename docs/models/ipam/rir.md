# 区域互联网注册管理机构（RIRs）

[区域互联网注册管理机构](https://en.wikipedia.org/wiki/Regional_Internet_registry)负责分配全球可路由的地址空间。五个RIR分别是ARIN、RIPE、APNIC、LACNIC和AFRINIC。但是，一些地址空间已经被保留供内部使用，例如RFC 1918和RFC 6598中定义的地址。NetBox将这些RFC视为一种RIR，即拥有某些地址空间的权威机构。还存在为特定地理区域提供服务的下层注册机构。

用户可以创建任何他们喜欢的RIR，但是每个[聚合](./aggregate.md)必须分配给一个RIR。例如，假设您的组织已经被ARIN分配了104.131.0.0/16。它还在内部使用RFC 1918的地址。您首先会创建名为"ARIN"和"RFC 1918"的RIR，然后为这些顶级前缀创建一个聚合，将其分配给相应的RIR。

## 字段

### 名称

唯一的用户友好名称。

### Slug

唯一的URL友好标识符。（此值可用于过滤。）

### 私有

将此RIR标记为仅适用于私有/本地IP空间的权威机构（例如RFC）。

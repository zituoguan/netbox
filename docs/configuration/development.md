#

## 调试 (DEBUG)

默认值: False

此设置启用调试功能。应仅在开发或故障排除期间启用调试。请注意，只有从被识别为[内部IP地址](#internal_ips)的客户端才会在用户界面中看到调试工具。

!!! 警告
    永远不要在生产系统上启用调试，因为它可能会将敏感数据暴露给未经身份验证的用户并且会对性能造成重大影响。

---

## 开发者模式 (DEVELOPER)

默认值: False

此参数用作防止某些潜在危险行为的保护措施，例如生成新的数据库模式迁移。此外，启用此设置会禁用用户界面中的调试警告横幅。仅在积极开发NetBox代码库时将其设置为`True`。请注意，这两个参数有助于在不同环境中管理NetBox的行为。 DEBUG参数用于启用或禁用调试，而DEVELOPER参数用于控制开发相关的选项。在生产环境中，它们通常都应设置为`False`以确保安全性和性能。
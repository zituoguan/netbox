# 导出模板

导出模板用于从一组NetBox对象中呈现任意数据。例如，您可能希望从设备对象列表自动生成网络监控服务配置。有关更多信息，请参阅[导出模板文档](../../customization/export-templates.md)。

## 字段

### 名称

导出模板的名称。这将显示在NetBox UI中的“导出”下拉列表中。

### 内容类型

导出模板适用的NetBox对象类型。

### 数据文件

模板代码可以选择从远程[数据文件](../core/datafile.md)中获取，该文件是从远程数据源同步的。在指定数据文件时，无需指定模板的本地内容：它将自动从数据文件填充。

### 模板代码

用于呈现导出数据的Jinja2模板代码。

### MIME类型

在呈现导出模板时在响应中指示的MIME类型（可选）。默认为`text/plain`。

### 文件扩展名

在响应中附加到文件名的文件扩展名（可选）。

### 作为附件

如果选择，呈现的内容将作为文件附件返回，而不是直接在支持的浏览器中显示。

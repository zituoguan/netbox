# 模块类型

模块类型表示一种特定的硬件组件型号，可以安装在设备的[模块插槽](./modulebay.md)中，并具有其自己的子组件。例如，考虑一个带有多个可更换线卡的机箱式交换机或路由器。每个线卡都有自己的型号，并包括一定数量的组件，例如接口。每个模块类型可以分配制造商、型号号和零件号。

与[设备类型](./devicetype.md)类似，每个模块类型可以关联以下任何组件模板：

* 接口
* 控制台端口
* 控制台服务器端口
* 电源端口
* 电源插座
* 正面通行端口
* 后通行端口

请注意，设备插槽和模块插槽不能添加到模块中。

## 自动组件重命名

在将组件模板添加到模块类型时，可以使用字符串“{module}”来引用将模块类型的实例安装到其中的模块插槽的“position”字段。

例如，您可以创建一个带有接口模板的模块类型，命名为“Gi{module}/0/[1-48]”。当将此类型的新模块“安装”到位置为“3”的模块插槽时，NetBox将自动将这些接口命名为“Gi3/0/[1-48]”。

自动重命名支持所有模块化组件类型（列出如上）。

## 字段

### 制造商

生产此类型模块的[制造商](./manufacturer.md)。

### 型号

制造商分配给此模块类型的型号号。必须对制造商是唯一的。

### 零件号

用于唯一标识模块类型的备用零件号。

### 重量

模块的数字重量，包括单位标识（例如，3千克或1磅）。

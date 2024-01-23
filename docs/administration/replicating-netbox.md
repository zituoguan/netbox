# 复制NetBox

## 复制数据库

NetBox使用[PostgreSQL](https://www.postgresql.org/)数据库，因此在这里适用通用的PostgreSQL最佳实践。可以使用`pg_dump`和`psql`工具将数据库写入文件并进行恢复。

!!! 注意
    下面的示例假设您的数据库命名为`netbox`。

### 导出数据库

使用`pg_dump`工具将整个数据库导出到文件中：

```no-highlight
pg_dump --username netbox --password --host localhost netbox > netbox.sql
```

!!! 注意
    您可能需要更改上述命令中的用户名、主机和/或数据库以匹配您的安装。

在将生产数据库复制到开发目的地时，您可能会发现将changelog数据排除在外是方便的，因为它很容易占据数据库大小的大部分。为此，可以在导出中排除`extras_objectchange`表数据。该表仍然会包含在输出文件中，但不会填充任何数据。

```no-highlight
pg_dump ... --exclude-table-data=extras_objectchange netbox > netbox.sql
```

### 加载导出的数据库

在从文件中还原数据库时，建议首先删除任何现有数据库，以避免潜在的冲突。

!!! 警告
    以下操作将销毁并替换现有数据库实例。

```no-highlight
psql -c 'drop database netbox'
psql -c 'create database netbox'
psql netbox < netbox.sql
```

请注意，PostgreSQL用户帐户和权限未包含在导出中：如果要完全复制原始数据库，您将需要手动创建这些帐户（请参阅[安装文档](../installation/1-postgresql.md)）。在设置NetBox的开发实例时，强烈建议使用不同的凭据。

### 导出数据库架构

如果只想导出数据库架构而不是数据本身（例如，供开发参考），请执行以下操作：

```no-highlight
pg_dump --username netbox --password --host localhost -s netbox > netbox_schema.sql
```

---

## 复制上传的媒体

默认情况下，NetBox将上传的文件（如图像附件）存储在其媒体目录中。要完全复制NetBox的实例，您需要复制数据库和媒体文件。

!!! 注意
    如果您的安装正在使用[远程存储后端](../configuration/system.md#storage_backend)，则不需要执行这些操作。

### 存档媒体目录

从NetBox安装路径的根目录（通常为`/opt/netbox`）执行以下命令：

```no-highlight
tar -czf netbox_media.tar.gz netbox/media/
```

### 恢复媒体目录

要将保存的存档提取到新安装中，请从安装根目录运行以下命令：

```no-highlight
tar -xf netbox_media.tar.gz
```

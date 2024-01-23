# 用户偏好设置

`users.UserConfig` 模型以 JSON 数据的形式保存每个用户的个人偏好设置。本页作为 NetBox 中所有已识别的用户偏好设置的清单。

## 可用偏好设置

| 名称                     | 描述                                                   |
|--------------------------|-------------------------------------------------------|
| data_format              | 渲染原始数据时的首选格式（JSON 或 YAML）              |
| pagination.per_page      | 每个分页表格页面显示的项目数量                      |
| pagination.placement     | 相对于表格显示分页控件的位置                        |
| tables.${table}.columns  | 查看表格时要显示的列的有序列表                      |
| tables.${table}.ordering | 表格应按列名排序的列的列表                           |
| ui.colormode             | 用户界面中的明亮或暗模式                              |

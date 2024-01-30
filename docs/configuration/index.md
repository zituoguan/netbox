# NetBox配置

## 配置文件

NetBox的配置文件包含了控制NetBox功能的所有重要参数：数据库设置、安全控制、用户首选项等等。尽管默认配置对于大多数用例都足够，但在安装过程中必须定义一些[必需的参数](./required-parameters.md)。

默认情况下，配置文件从`$INSTALL_ROOT/netbox/netbox/configuration.py`加载。示例配置位于`configuration_example.py`中，您可以复制它并用作默认配置。请注意，必须定义一个配置文件；没有配置文件，NetBox将无法运行。

!!! info "自定义配置模块"
    可以通过设置`NETBOX_CONFIGURATION`环境变量来指定自定义配置模块。这必须是指向所需Python模块的点分路径。例如，与`settings.py`位于同一目录中的名为`my_config.py`的文件可以引用为`netbox.my_config`。

    为简单起见，NetBox文档简单地将配置文件称为`configuration.py`。

在文档中适用的情况下，某些配置参数可以在`configuration.py`中定义，也可以在用户界面的管理部分内定义。在配置文件中“硬编码”的设置优先于通过UI定义的设置。

## 动态配置参数

一些配置参数主要通过NetBox的管理界面（在Admin > Extras > Configuration Revisions下）进行控制。在文档中适用的地方进行了相应的注释。这些设置也可以在`configuration.py`中进行覆盖，以防止通过UI进行修改。以下是支持的参数的完整列表：

* [`ALLOWED_URL_SCHEMES`](./security.md#allowed_url_schemes)
* [`BANNER_BOTTOM`](./miscellaneous.md#banner_bottom)
* [`BANNER_LOGIN`](./miscellaneous.md#banner_login)
* [`BANNER_TOP`](./miscellaneous.md#banner_top)
* [`CHANGELOG_RETENTION`](./miscellaneous.md#changelog_retention)
* [`CUSTOM_VALIDATORS`](./data-validation.md#custom_validators)
* [`DEFAULT_USER_PREFERENCES`](./default-values.md#default_user_preferences)
* [`ENFORCE_GLOBAL_UNIQUE`](./miscellaneous.md#enforce_global_unique)
* [`GRAPHQL_ENABLED`](./miscellaneous.md#graphql_enabled)
* [`JOB_RETENTION`](./miscellaneous.md#job_retention)
* [`MAINTENANCE_MODE`](./miscellaneous.md#maintenance_mode)
* [`MAPS_URL`](./miscellaneous.md#maps_url)
* [`MAX_PAGE_SIZE`](./miscellaneous.md#max_page_size)
* [`PAGINATE_COUNT`](./default-values.md#paginate_count)
* [`POWERFEED_DEFAULT_AMPERAGE`](./default-values.md#powerfeed_default_amperage)
* [`POWERFEED_DEFAULT_MAX_UTILIZATION`](./default-values.md#powerfeed_default_max_utilization)
* [`POWERFEED_DEFAULT_VOLTAGE`](./default-values.md#powerfeed_default_voltage)
* [`PREFER_IPV4`](./miscellaneous.md#prefer_ipv4)
* [`RACK_ELEVATION_DEFAULT_UNIT_HEIGHT`](./default-values.md#rack_elevation_default_unit_height)
* [`RACK_ELEVATION_DEFAULT_UNIT_WIDTH`](./default-values.md#rack_elevation_default_unit_width)

## 修改配置

可以随时修改配置文件。但是，在这些更改生效之前，必须重新启动WSGI服务（例如Gunicorn）：

```no-highlight
$ sudo systemctl restart netbox
```

可以通过用户界面修改的动态配置参数会立即生效。

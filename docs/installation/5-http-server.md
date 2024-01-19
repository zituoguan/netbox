# HTTP服务器设置

此文档提供了针对[nginx](https://www.nginx.com/resources/wiki/)和[Apache](https://httpd.apache.org/docs/current/)的示例配置，但任何支持WSGI的HTTP服务器都应该兼容。

!!! info
    为了简洁起见，这里仅提供了Ubuntu 20.04的说明。这些任务与NetBox无关，应该在其他发行版上进行最小的更改。如果需要帮助，请查阅您的发行版文档。

## 获取SSL证书

要启用对NetBox的HTTPS访问，您需要一个有效的SSL证书。您可以从受信任的商业提供商购买一个，从[Let's Encrypt](https://letsencrypt.org/getting-started/)免费获取一个，或者生成自己的证书（尽管自签名证书通常不受信任）。公共证书和私钥文件都需要安装在您的NetBox服务器上，以供`netbox`用户读取。

以下命令可用于生成用于测试目的的自签名证书，但强烈建议在生产中使用来自受信任机构的证书。将创建两个文件：公共证书（`netbox.crt`）和私钥（`netbox.key`）。证书是向世界发布的，而私钥必须始终保密。

```no-highlight
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout /etc/ssl/private/netbox.key \
-out /etc/ssl/certs/netbox.crt
```

上述命令将提示您提供证书的其他详细信息；所有这些信息都是可选的。

## 安装HTTP服务器

### 选项A：nginx

首先安装nginx：

```no-highlight
sudo apt install -y nginx
```

安装nginx后，将NetBox提供的nginx配置文件复制到`/etc/nginx/sites-available/netbox`。确保将`netbox.example.com`替换为您的安装的域名或IP地址（这应该与`configuration.py`中配置的`ALLOWED_HOSTS`的值匹配）。

```no-highlight
sudo cp /opt/netbox/contrib/nginx.conf /etc/nginx/sites-available/netbox
```

然后，删除`/etc/nginx/sites-enabled/default`并在`sites-enabled`目录中创建一个到刚刚创建的配置文件的符号链接。

```no-highlight
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/netbox /etc/nginx/sites-enabled/netbox
```

最后，重新启动`nginx`服务以使用新的配置。

```no-highlight
sudo systemctl restart nginx
```

### 选项B：Apache

首先安装Apache：

```no-highlight
sudo apt install -y apache2
```

接下来，将默认配置文件复制到`/etc/apache2/sites-available/`。确保适当修改`ServerName`参数。

```no-highlight
sudo cp /opt/netbox/contrib/apache.conf /etc/apache2/sites-available/netbox.conf
```

最后，确保启用了所需的Apache模块，启用`netbox`站点并重新加载Apache：

```no-highlight
sudo a2enmod ssl proxy proxy_http headers rewrite
sudo a2ensite netbox
sudo systemctl restart apache2
```

## 确认连接

此时，您应该能够连接到您提供的服务器名称或IP地址的HTTPS服务。

!!! info
    请记住，这里提供的配置是为了使NetBox能够运行所需的最低限度。您可能希望进行调整，以更好地适应您的生产环境。

!!! warning
    NetBox的某些组件（例如机架高度图的显示）依赖于嵌入式对象的使用。确保您的HTTP服务器配置不会覆盖NetBox设置的`X-Frame-Options`响应头。

## 故障排除

如果无法连接到HTTP服务器，请检查以下内容：

* Nginx/Apache正在运行并配置为侦听正确的端口。
* 访问没有被沿途的防火墙阻止。（尝试从服务器本身本地连接。）

如果能够连接但收到502（坏的网关）错误，请检查以下内容：

* WSGI工作进程（gunicorn）正在运行（`systemctl status netbox`应显示“active (running)”状态）。
* Nginx/Apache已配置为连接到gunicorn正在侦听的端口（默认为8001）。
* SELinux没有阻止反向代理连接。您可能需要使用命令`setsebool -P httpd_can_network_connect 1`允许HTTP网络连接。
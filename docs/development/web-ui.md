# Web UI开发

## 前端技术

NetBox UI 基于以下语言和框架构建：

### 样式和HTML元素

#### [Bootstrap](https://getbootstrap.com/) 5

NetBox UI 的大部分由标准 Bootstrap 组件组成，根据需要添加一些样式修改和自定义组件。Bootstrap 使用 [Sass](https://sass-lang.com/)，NetBox 扩展了 Bootstrap 的核心 Sass 文件以进行主题和自定义。

### 客户端脚本

#### [TypeScript](https://www.typescriptlang.org/)

所有客户端脚本都从 TypeScript 转译为 JavaScript，并由 Django 提供服务。在开发中，TypeScript 是一种非常有效的工具，用于准确描述和检查代码，这导致错误大大减少，开发体验更好，代码更可预测和可读。

作为 [捆绑](#捆绑) 过程的一部分，引入并捆绑了 Bootstrap 的 JavaScript 插件，与 NetBox 的前端代码一起使用。

!!! 危险 "NetBox不使用jQuery"
    随着Bootstrap 5团队在Bootstrap 5中废弃了jQuery，NetBox也不再在前端代码中使用jQuery。

## 指南

NetBox通常遵循以下前端代码的准则：

- 可以使用Bootstrap的实用类来解决临时问题或实现单一组件，只要类列表不超过4-5个类。如果元素需要超过5个实用类，应添加包含所需样式属性的自定义SCSS类。
- 必须对自定义类进行注释，解释类的一般目的以及它在哪里使用。
- 在可能的情况下重复使用SCSS变量。几乎不应硬编码CSS值。
- 所有TypeScript函数必须至少具有基本的 [JSDoc](https://jsdoc.app/) 描述，说明函数的用途和用途。如果可能，通过 [`@param` JSDoc 块标签](https://jsdoc.app/tags-param.html) 文档化所有函数参数。
- 在NetBox的 [依赖策略](style-guide.md#introducing-new-dependencies) 的基础上，应尽量避免引入新的前端依赖项，除非绝对必要。每个新的前端依赖项都会增加客户端必须加载的CSS/JavaScript文件大小，应尽量减小这一大小。如果不可避免地添加新的依赖项，请使用像 [Bundlephobia](https://bundlephobia.com/) 这样的工具，以确保使用最小的可能库。
- 所有UI元素必须在所有常见屏幕尺寸上可用，包括移动设备。确保在尽可能多的屏幕尺寸和设备类型上测试新实现的解决方案（包括JavaScript）。
- NetBox与Bootstrap的 [支持的浏览器和设备](https://getbootstrap.com/docs/5.1/getting-started/browsers-devices/) 列表保持一致。

## UI开发

要为NetBox UI做出贡献，您需要查看主要的 [入门指南](getting-started.md)，以设置基本环境。

### 工具

一旦您拥有可用的NetBox开发环境，您将需要安装一些工具来使用NetBox UI：

- [NodeJS](https://nodejs.org/en/download/)（LTS版本应该足够）
- [Yarn](https://yarnpkg.com/getting-started/install)（版本1）

在您的系统上安装Node和Yarn后，您需要安装所有NetBox UI依赖项：

```console
$ cd netbox/project-static
$ yarn
```

!!! 警告 "检查工作目录"
    您需要位于 `netbox/project-static` 目录中才能运行下面的 `yarn` 命令。

### 捆绑

为了使TypeScript和Sass（SCSS）源文件能够被浏览器使用，它们必须首先进行转译（TypeScript → JavaScript，Sass → CSS）、捆绑和最小化。在更改TypeScript或Sass源文件后，运行 `yarn bundle`。

`yarn bundle` 是以下子命令的包装器，可以单独运行其中任何一个：

| 命令               | 操作                                           |
| :-------------------- | :---------------------------------------------- |
| `yarn bundle`         | 捆绑TypeScript和Sass（SCSS）源文件。 |
| `yarn bundle:styles`  | 仅捆绑Sass（SCSS）源文件。           |
| `yarn bundle:scripts` | 仅捆绑TypeScript源文件。            |

所有输出文件将被写入 `netbox/project-static/dist`，当运行 `manage.py collectstatic` 时，Django 将获取它们。

!!! 信息 "记住重新运行 `manage.py collectstatic`"
    如果您正在运行开发Web服务器 — `manage.py runserver` — 您需要运行 `manage.py collectstatic` 以查看您的更改。

### 代码检查、格式化和类型检查

在提交任何更改到TypeScript文件之前，以及在开发过程中定期运行 `yarn validate` 以捕获格式、代码质量或类型错误。

!!! 提示 "IDE集成"
    如果您使用的是IDE，强烈建议安装 [ESLint](https://eslint.org/docs/user-guide/integrations)、[TypeScript](https://github.com/Microsoft/TypeScript/wiki/TypeScript-Editor-Support) 和 [Prettier](https://prettier.io/docs/en/editors.html) 集成，如果可用的话。大多数IDE将在您开发时自动检查和/或纠正代码中的问题，这可以显着提高您作为贡献者的生产力。

`yarn validate` 是以下子命令的包装器，可以单独运行其中任何一个：

| 命令               | 操作                                           |
| :-------------------- | :---------------------------------------------- |
| `yarn validate`                    | 运行所有验证。                                              |
| `yarn validate:lint`               | 仅通过 [ESLint](https://eslint.org/) 验证 TypeScript 代码。 |
| `yarn validate:types`              | 仅验证 TypeScript 代码编译。                       |
| `yarn validate:formatting`         | 验证 JavaScript 和 Sass/SCSS 文件的代码格式。       |
| `yarn validate:formatting:styles`  | 仅验证 Sass/SCSS 代码格式。                         |
| `yarn validate:formatting:scripts` | 仅验证 TypeScript 代码格式。                      |

您还可以运行以下命令来自动修复格式问题：

| 命令               | 操作                                          |
| :-------------------- | :---------------------------------------------- |
| `yarn format`         | 格式化 TypeScript 和 Sass (SCSS) 源文件。 |
| `yarn format:styles`  | 仅格式化 Sass (SCSS) 源文件。           |
| `yarn format:scripts` | 仅格式化 TypeScript 源文件。            |


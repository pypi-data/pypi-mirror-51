# goss
Github Object Storage System 使用 Github 构建类似 oss 的对象储存工具，本工具可以很方便的管理 github 数据，可以很方便的搭建图床

***暂不支持 windows 系统***

**创建仓库**

![goss1](https://raw.githubusercontent.com/wxnacy/image/master/blog/goss1.gif)

**上传本地图片**

![goss2](https://raw.githubusercontent.com/wxnacy/image/master/blog/goss3.gif)

## 安装

使用 pip 安装非常方便

```bash
$ pip install goss
```

**更新**

```bash
$ pip install --upgrade goss
```

## 快速开始

goss 的命令格式基本遵守了 RESTful 风格

### 登录

```bash
$ goss-cli login
```

**配置**

```bash
$ goss-cli config repo.name <repo-name> # 配置默认仓库名
$ goss-cli config repo.path <path>      # 配置上传文件时默认的地址或目录，默认为根目录
```

### 上传文件

```bash
$ goss <filepath|url>                   # 上传文件到默认的仓库和地址
$ goss <filepath|url> -r <repo-name>    # 指定一个仓库
$ goss <filepath|url> -p <path>         # 指定一个地址或目录
```

### 仓库管理

```bash
$ goss-cli repo                           # 查看仓库列表
$ goss-cli repo <repo-name>               # 查看指定仓库
$ goss-cli repo <repo-name> -m post       # 创建仓库
$ goss-cli repo <repo-name> -m delete     # 删除仓库
```

### 文件管理

```bash
$ goss-cli file                     # 查看默认仓库根目录下所有文件
$ goss-cli file <path>              # 查看指定文件详情或指定目录下文件列表
$ goss-cli file -r <repo-name>      # 查看指定仓库
$ goss-cli file <path> -m delete    # 删除指定文件
```

更多使用请使用帮助命令 `goss-cli --help` 或者 `goss-cli <cmd> --help`

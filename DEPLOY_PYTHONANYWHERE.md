# 部署到 PythonAnywhere 指南

本指南将帮助您将 TapNote 部署到 PythonAnywhere 平台。

## 1. 准备工作

确保您的代码已经推送到 GitHub（我们刚刚已经完成了）。

## 2. 注册并登录 PythonAnywhere

访问 [www.pythonanywhere.com](https://www.pythonanywhere.com/) 并注册一个账号。

## 3. 快速部署（使用脚本）

我们提供了一个自动化脚本来处理大部分工作。

1. 登录 PythonAnywhere，点击 **Consoles** -> **Bash**。
2. 在终端中运行以下命令（这将下载并运行脚本）：

```bash
# 下载脚本并运行
curl -O https://raw.githubusercontent.com/zoidberg-xgd/tapnote/master/deploy_pa.sh
chmod +x deploy_pa.sh
source deploy_pa.sh
```

> 注意：您可以先克隆仓库，然后直接运行仓库里的 `source deploy_pa.sh`。

脚本运行完成后，它会提示您在 **Web** 选项卡中需要手动配置的最后几步（因为这些无法通过脚本在免费账户中自动完成）。

请直接跳到 **第 7 步：配置 Web 应用** 继续操作。

---

## 4. 手动部署（如果不使用脚本）

如果您更喜欢手动操作，请按照以下步骤进行。

### 拉取代码

1. 登录后，点击右上角的 **Consoles** 选项卡。
2. 点击 **Bash** 启动一个命令行终端。
3. 在终端中输入以下命令来克隆您的仓库：

```bash
git clone https://github.com/zoidberg-xgd/tapnote.git
cd tapnote
```

### 设置虚拟环境

在同一个 Bash 终端中，执行以下命令来创建虚拟环境并安装依赖：

```bash
# 创建虚拟环境
mkvirtualenv --python=/usr/bin/python3.10 tapnote-venv

# 激活虚拟环境（通常会自动激活）
workon tapnote-venv

# 安装依赖
pip install -r requirements.txt
```

> 注意：如果 `mkvirtualenv` 命令不存在，尝试运行 `python3.10 -m venv venv` 然后 `source venv/bin/activate`，但在 PythonAnywhere 上推荐使用 `mkvirtualenv`（它是 virtualenvwrapper 的一部分）。

## 5. 配置环境变量

在项目根目录（`~/tapnote`）创建一个 `.env` 文件：

```bash
nano .env
```

粘贴以下内容（请修改 SECRET_KEY）：

```env
DEBUG=False
SECRET_KEY=change-this-to-a-long-random-string
ALLOWED_HOSTS=.pythonanywhere.com
# 如果您想使用 SQLite（最简单）：
DATABASE_URL=sqlite:////home/<your-username>/tapnote/db.sqlite3
```

按 `Ctrl+X`，然后按 `Y`，再按 `Enter` 保存并退出。

## 6. 收集静态文件和迁移数据库

继续在 Bash 终端中执行：

```bash
# 收集静态文件
python manage.py collectstatic

# 迁移数据库
python manage.py migrate
```

## 7. 配置 Web 应用

1. 点击页面顶部的 **Web** 选项卡。
2. 点击 **Add a new web app**。
3. 点击 **Next**。
4. 选择 **Manual configuration**（手动配置） -> 选择 **Python 3.10** -> 点击 **Next**。
5. 创建完成后，向下滚动到 **Virtualenv** 部分：
   - 输入您的虚拟环境路径，例如：`/home/<your-username>/.virtualenvs/tapnote-venv`
   - (如果您使用的是 `venv` 目录，则是 `/home/<your-username>/tapnote/venv`)
   - 点击勾选确认。

## 8. 配置 WSGI 文件

1. 在 **Web** 选项卡中，找到 **Code** 部分。
2. 点击 **WSGI configuration file** 旁边的链接（通常是 `/var/www/<username>_pythonanywhere_com_wsgi.py`）。
3. 删除文件中的所有内容，替换为以下内容：

```python
import os
import sys
from dotenv import load_dotenv

# 假设您的用户名是 'yourusername'，请替换它
# 或者使用 os.path 动态获取，但硬编码路径最不容易出错
path = '/home/<your-username>/tapnote'
if path not in sys.path:
    sys.path.append(path)

# 加载 .env 文件
project_folder = os.path.expanduser(path)
load_dotenv(os.path.join(project_folder, '.env'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'prototype.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

> **重要**：请务必将 `<your-username>` 替换为您真实的 PythonAnywhere 用户名。

4. 点击 **Save** 保存文件。

## 9. 配置静态文件 (Static Files)

回到 **Web** 选项卡，向下滚动到 **Static files** 部分：

1. 点击 **Enter URL**，输入 `/static/`
2. 点击 **Enter path**，输入 `/home/<your-username>/tapnote/staticfiles`
   (注意：我们在 settings.py 中设置的是 `staticfiles` 目录)

## 10. 完成！

回到页面顶部，点击绿色的 **Reload** 按钮。

点击顶部的应用链接（例如 `https://<your-username>.pythonanywhere.com`），您的 TapNote 应该就可以访问了！

## 常见问题

- **如果是 500 错误**：查看 **Web** 选项卡底部的 **Error log**。通常是 WSGI 文件路径不对、依赖没装好或者 .env 文件没读取到。
- **CSS 不显示**：检查 **Static files** 的路径是否正确，是否执行了 `collectstatic`。

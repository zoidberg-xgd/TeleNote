# Deployment Guide / 部署指南

[English](#english) | [中文](#中文)

---

## English

This guide covers deploying TeleNote to various platforms.

### Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/zoidberg-xgd/TeleNote.git
   cd tapnote
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Access the app** at `http://localhost:9009`

### Manual Installation

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `example.env` to `.env` and configure
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver 0.0.0.0:9009`

### PythonAnywhere

#### Quick Deploy (Script)

1. Log in to PythonAnywhere, go to **Consoles** → **Bash**
2. Run:
   ```bash
   curl -O https://raw.githubusercontent.com/zoidberg-xgd/TeleNote/master/deploy_pa.sh
   chmod +x deploy_pa.sh
   source deploy_pa.sh
   ```
3. Follow the prompts to complete Web app configuration

#### Manual Deploy

1. Clone the repo:
   ```bash
   git clone https://github.com/zoidberg-xgd/TeleNote.git
   cd tapnote
   ```

2. Create virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 tapnote-venv
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```env
   DEBUG=False
   SECRET_KEY=change-this-to-a-long-random-string
   ALLOWED_HOSTS=.pythonanywhere.com
   DATABASE_URL=sqlite:////home/<username>/tapnote/db.sqlite3
   ```

4. Run migrations and collect static files:
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

5. Configure Web app in PythonAnywhere dashboard:
   - Add new web app → Manual configuration → Python 3.10
   - Set virtualenv path: `/home/<username>/.virtualenvs/tapnote-venv`
   - Add static files mapping: `/static/` → `/home/<username>/tapnote/staticfiles`

6. Configure WSGI file (click the **WSGI configuration file** link in Web tab):
   ```python
   import os
   import sys
   from dotenv import load_dotenv

   path = '/home/<username>/tapnote'
   if path not in sys.path:
       sys.path.append(path)

   load_dotenv(os.path.join(path, '.env'))
   os.environ['DJANGO_SETTINGS_MODULE'] = 'prototype.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
   > Replace `<username>` with your PythonAnywhere username

#### Updating PythonAnywhere

```bash
cd ~/tapnote
workon tapnote-venv
git pull
pip install -r requirements.txt  # if dependencies changed
python manage.py migrate         # if models changed
python manage.py collectstatic --noinput  # if static files changed
# Then click Reload in Web tab
```

#### Auto-Renewal (Free Accounts)

PythonAnywhere free accounts require periodic renewal. Use `scripts/renew_pa.py`:

**Local:**
```bash
export PA_USERNAME="your_username"
export PA_PASSWORD="your_password"
python scripts/renew_pa.py
```

**GitHub Actions:** Add `PA_USERNAME` and `PA_PASSWORD` as repository secrets. The workflow runs automatically on the 1st and 15th of each month.

> ⚠️ Auto-renewal may violate PythonAnywhere ToS. Use at your own risk.

### Troubleshooting

- **500 Error**: Check error logs, verify WSGI paths, ensure `.env` is loaded
- **CSS not loading**: Verify static files path, run `collectstatic`
- **Database errors**: Run `migrate`, check file permissions

---

## 中文

本指南介绍如何将 TeleNote 部署到各种平台。

### Docker（推荐）

1. **克隆仓库**
   ```bash
   git clone https://github.com/zoidberg-xgd/TeleNote.git
   cd tapnote
   ```

2. **运行设置脚本**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **访问应用**：`http://localhost:9009`

### 手动安装

1. 安装依赖：`pip install -r requirements.txt`
2. 复制 `example.env` 到 `.env` 并配置
3. 运行迁移：`python manage.py migrate`
4. 启动服务器：`python manage.py runserver 0.0.0.0:9009`

### PythonAnywhere

#### 快速部署（脚本）

1. 登录 PythonAnywhere，点击 **Consoles** → **Bash**
2. 运行：
   ```bash
   curl -O https://raw.githubusercontent.com/zoidberg-xgd/TeleNote/master/deploy_pa.sh
   chmod +x deploy_pa.sh
   source deploy_pa.sh
   ```
3. 按提示完成 Web 应用配置

#### 手动部署

1. 克隆仓库：
   ```bash
   git clone https://github.com/zoidberg-xgd/TeleNote.git
   cd tapnote
   ```

2. 创建虚拟环境：
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 tapnote-venv
   pip install -r requirements.txt
   ```

3. 创建 `.env` 文件：
   ```env
   DEBUG=False
   SECRET_KEY=修改为随机长字符串
   ALLOWED_HOSTS=.pythonanywhere.com
   DATABASE_URL=sqlite:////home/<用户名>/tapnote/db.sqlite3
   ```

4. 运行迁移和收集静态文件：
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

5. 在 PythonAnywhere 控制台配置 Web 应用：
   - 添加新 Web 应用 → 手动配置 → Python 3.10
   - 设置虚拟环境路径：`/home/<用户名>/.virtualenvs/tapnote-venv`
   - 添加静态文件映射：`/static/` → `/home/<用户名>/tapnote/staticfiles`

6. 配置 WSGI 文件（点击 Web 选项卡中的 WSGI configuration file 链接）：
   ```python
   import os
   import sys
   from dotenv import load_dotenv

   path = '/home/<用户名>/tapnote'
   if path not in sys.path:
       sys.path.append(path)

   load_dotenv(os.path.join(path, '.env'))
   os.environ['DJANGO_SETTINGS_MODULE'] = 'prototype.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
   > 请将 `<用户名>` 替换为您的 PythonAnywhere 用户名

#### 更新 PythonAnywhere

```bash
cd ~/tapnote
workon tapnote-venv
git pull
pip install -r requirements.txt  # 如果依赖有变化
python manage.py migrate         # 如果模型有变化
python manage.py collectstatic --noinput  # 如果静态文件有变化
# 然后在 Web 选项卡点击 Reload
```

#### 自动续期（免费账户）

PythonAnywhere 免费账户需要定期续期。使用 `scripts/renew_pa.py`：

**本地运行：**
```bash
export PA_USERNAME="your_username"
export PA_PASSWORD="your_password"
python scripts/renew_pa.py
```

**GitHub Actions：** 将 `PA_USERNAME` 和 `PA_PASSWORD` 添加为仓库密钥。工作流会在每月 1 日和 15 日自动运行。

> ⚠️ 自动续期可能违反 PythonAnywhere 服务条款，请自行承担风险。

### 故障排查

- **500 错误**：检查错误日志，验证 WSGI 路径，确保 `.env` 已加载
- **CSS 不显示**：验证静态文件路径，运行 `collectstatic`
- **数据库错误**：运行 `migrate`，检查文件权限

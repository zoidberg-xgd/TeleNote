# 更新 PythonAnywhere 部署指南

本指南说明如何将本地代码更新推送到 PythonAnywhere 服务器。

## 快速更新步骤

### 1. 确保代码已推送到 GitHub

在本地执行（已完成）：
```bash
git add -A
git commit -m "更新说明"
git push
```

### 2. 在 PythonAnywhere 上更新

#### 方法一：使用部署脚本（推荐）

1. 登录 PythonAnywhere，点击 **Consoles** -> **Bash**
2. 运行以下命令：

```bash
cd ~/tapnote
source deploy_pa.sh
```

脚本会自动：
- 拉取最新代码 (`git pull`)
- 更新依赖（如果需要）
- 运行数据库迁移 (`python manage.py migrate`)
- 收集静态文件 (`python manage.py collectstatic`)

#### 方法二：手动更新

在 PythonAnywhere 的 Bash 终端中执行：

```bash
# 1. 进入项目目录
cd ~/tapnote

# 2. 激活虚拟环境
workon tapnote-venv

# 3. 拉取最新代码
git pull

# 4. 安装/更新依赖（如果有新依赖）
pip install -r requirements.txt

# 5. 运行数据库迁移（如果有新的迁移文件）
python manage.py migrate

# 6. 收集静态文件（如果有新的静态文件）
python manage.py collectstatic --noinput
```

### 3. 重新加载 Web 应用

1. 点击页面顶部的 **Web** 选项卡
2. 点击绿色的 **Reload** 按钮

完成！您的更新应该已经生效。

## 常见更新场景

### 场景1：只更新了代码（无数据库变更）

```bash
cd ~/tapnote
workon tapnote-venv
git pull
# 然后去 Web 选项卡点击 Reload
```

### 场景2：添加了新的数据库模型（有迁移文件）

```bash
cd ~/tapnote
workon tapnote-venv
git pull
python manage.py migrate
python manage.py collectstatic --noinput
# 然后去 Web 选项卡点击 Reload
```

### 场景3：添加了新的静态文件（CSS/JS）

```bash
cd ~/tapnote
workon tapnote-venv
git pull
python manage.py collectstatic --noinput
# 然后去 Web 选项卡点击 Reload
```

### 场景4：添加了新的 Python 依赖

```bash
cd ~/tapnote
workon tapnote-venv
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# 然后去 Web 选项卡点击 Reload
```

## 故障排查

### 如果更新后出现错误

1. **查看错误日志**：
   - 在 **Web** 选项卡底部找到 **Error log**
   - 查看最新的错误信息

2. **常见问题**：
   - **500 错误**：检查是否运行了 `migrate`，检查依赖是否安装完整
   - **静态文件不显示**：确保运行了 `collectstatic`，检查 Web 选项卡中的静态文件路径配置
   - **数据库错误**：确保运行了 `migrate`，检查数据库文件权限

3. **回滚到上一个版本**（如果需要）：
   ```bash
   cd ~/tapnote
   git log  # 查看提交历史
   git checkout <previous-commit-hash>  # 回滚到指定提交
   # 然后重新加载 Web 应用
   ```

## 提示

- 建议每次更新前先查看 `git log` 确认要拉取的更改
- 如果更新涉及数据库变更，建议先在本地测试迁移是否正常
- 更新后访问网站测试功能是否正常


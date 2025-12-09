# TeleNote

[English](README.md) | [中文](README_CN.md) | [API 文档](API.md)

**TeleNote** 是一个极简的自托管发布平台，灵感来自 [Telegra.ph](https://telegra.ph)。它提供无干扰的写作体验，支持即时 Markdown 发布、段落级评论，并拥有功能完善的 API。

![Demo](media/demo.gif)

[**🔴 在线演示 (Live Demo)**](https://zoidbergxgd.pythonanywhere.com/)

## ✨ 核心功能

- **📝 极简编辑器**：干净、无干扰的 Markdown 编辑器。无需注册账号。
- **⚡ 即时发布**：几秒钟内发布匿名文章。
- **🔌 兼容 Telegraph API**：Telegra.ph 的直接替代品。兼容现有的 Telegraph 客户端和机器人。
- **💬 段落评论**：集成 [ParaNote](https://github.com/zoidberg-xgd/paranote)，提供 Medium 风格的段落级评论。
- **🖼️ 社交预览**：自动生成 Open Graph 标签，在 Telegram、Twitter/X 和微信上显示精美卡片。
- **🔗 智能链接**：优化后的 8 字符短链接。
- **📦 数据掌控**：完全自托管。支持导入/导出 JSON 数据。
- **🚀 轻松部署**：支持 Docker 和 PythonAnywhere 自动化脚本。

## 🚀 快速开始

### 使用 Docker (推荐)

1. **克隆仓库**
   ```bash
   git clone https://github.com/zoidberg-xgd/tapnote.git
   cd tapnote
   ```

2. **运行设置脚本**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **访问应用**
   在浏览器中打开 `http://localhost:9009`。

### 手动安装

1. 安装依赖：`pip install -r requirements.txt`
2. 设置环境变量（复制 `example.env` to `.env`）。
3. 运行迁移：`python manage.py migrate`
4. 启动服务器：`python manage.py runserver 0.0.0.0:9009`

## 🛠 API 使用

TeleNote 实现了一个完整的 **Telegraph API** 克隆。您可以通过编程方式创建页面、管理账户和获取浏览统计。

**基础 URL**: `https://your-instance.com/`

**示例：创建页面**

```bash
curl -X POST https://your-instance.com/createPage \
  -d access_token="your_token" \
  -d title="我的文章" \
  -d content='[{"tag":"p","children":["Hello World"]}]' \
  -d return_content=true
```

👉 **[阅读完整 API 文档](API.md)**

## 📦 命令行工具

您可以使用 **[TelePress](https://github.com/zoidberg-xgd/telepress)** (通过 pip 安装) 在命令行中直接发布内容。

1. 安装 TelePress：`pip install telepress`
2. 发布文件：

```bash
telepress my_article.md --api-url http://localhost:9009
```

支持功能：
- 长文章自动分页
- 图片上传
- Zip 文件相册

## ⚙️ 配置

通过 `.env` 文件进行配置。

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `DEBUG` | 启用调试模式 | `False` |
| `SECRET_KEY` | Django 密钥 | (必须) |
| `ALLOWED_HOSTS` | 允许的主机（逗号分隔） | `*` |
| `ENABLE_COMMENTS` | 启用评论系统 | `True` |

## 🧪 测试

TeleNote 附带了全面的测试套件，覆盖核心逻辑、API 端点和配置。

```bash
# 运行所有测试
./run_tests.sh

# 生成覆盖率报告
./run_tests.sh --coverage
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

基于 MIT 许可证分发。详见 `LICENSE` 文件。

## 🙏 致谢

- **Telegra.ph**：最初的灵感来源。
- **[vorniches/tapnote](https://github.com/vorniches/tapnote)**：项目的基础代码来源。
- **ParaNote**：提供评论系统支持。
- **Django & Tailwind**：坚实的基础框架。

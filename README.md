# TeleNote

[English](README.md) | [中文](README_CN.md) | [API Documentation](API.md)

**TeleNote** is a minimalist, self-hosted publishing platform inspired by [Telegra.ph](https://telegra.ph). It offers a distraction-free writing experience with instant Markdown publishing, paragraph-level comments, and a full-featured API.

![Demo](media/demo.gif)

[**🔴 Live Demo**](https://zoidbergxgd.pythonanywhere.com/)

## ✨ Key Features

- **📝 Minimalist Editor**: Clean, distraction-free Markdown editor. No account required.
- **⚡ Instant Publishing**: Publish anonymous articles in seconds.
- **🔌 Telegraph API Compatible**: Drop-in replacement for Telegra.ph. Compatible with existing Telegraph clients and bots.
- **💬 Paragraph Comments**: Integrated with [ParaNote](https://github.com/zoidberg-xgd/paranote) for Medium-style paragraph-level comments.
- **🖼️ Social Previews**: Automatic Open Graph tags for beautiful cards on Telegram, Twitter/X, and WeChat.
- **🔗 Smart Links**: Optimized 8-character short URLs.
- **📦 Data Ownership**: Self-hosted. Import/Export data as JSON.
- **🚀 Easy Deployment**: Docker support and automated scripts for PythonAnywhere.

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/zoidberg-xgd/tapnote.git
   cd tapnote
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Access the app**
   Open your browser to `http://localhost:9009`.

### Manual Installation

1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables (copy `example.env` to `.env`).
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver 0.0.0.0:9009`

## 🛠 API Usage

TeleNote implements a complete **Telegraph API** clone. You can use it to create pages, manage accounts, and get view statistics programmatically.

**Base URL**: `https://your-instance.com/`

**Example: Create a Page**

```bash
curl -X POST https://your-instance.com/createPage \
  -d access_token="your_token" \
  -d title="My Post" \
  -d content='[{"tag":"p","children":["Hello World"]}]' \
  -d return_content=true
```

👉 **[Read the full API Documentation](API.md)**

## 📦 CLI Tools

You can publish content directly using **[TelePress](https://github.com/zoidberg-xgd/telepress)** (installed via pip).

1. Install TelePress: `pip install telepress`
2. Publish a file:

```bash
telepress my_article.md --api-url http://localhost:9009
```

This supports:
- Automatic pagination for long articles
- Image uploading
- Zip file galleries

## ⚙️ Configuration

Configuration is managed via the `.env` file.

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Django secret key | (Required) |
| `ALLOWED_HOSTS` | Comma-separated hosts | `*` |
| `ENABLE_COMMENTS` | Enable comment system | `True` |

## 🧪 Testing

TeleNote comes with a comprehensive test suite covering the core logic, API endpoints, and configuration.

```bash
# Run all tests
./run_tests.sh

# Run with coverage report
./run_tests.sh --coverage
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- **Telegra.ph**: The original inspiration.
- **[vorniches/tapnote](https://github.com/vorniches/tapnote)**: The original project foundation.
- **ParaNote**: Powering the comment system.
- **Django & Tailwind**: The robust foundation.

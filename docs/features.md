# TeleNote Features Guide

This document provides a detailed overview of the features and capabilities of TeleNote.

## ✍️ Editor & Publishing

### Markdown Support
TeleNote uses a robust Markdown engine that supports:
- **Headers** (H1-H4)
- **Formatting**: Bold, Italic, Strikethrough, Code (inline and block)
- **Lists**: Ordered and Unordered
- **Quotes**: Blockquotes
- **Images**: Drag & drop or URL based
- **Links**: Standard markdown links

### Metadata
- **Title**: Mandatory field for every note.
- **Author Name**: Optional. Defaults to "Anonymous" if not provided.
- **Author URL**: Optional. Links the author name to a profile or website.

### Limitations
To ensure system stability and performance:
- **Content Length**: Max 200,000 characters per note.
- **Upload Size**: Max 2.5MB per request (for internal storage/processing).

## 📖 Reading Experience

### Social Previews
TeleNote automatically generates Open Graph (OG) tags for every page.
- **Title**: From note title.
- **Description**: First paragraph of the content.
- **Image**: First image in the content (if any).
- **Site Name**: TeleNote.

### Short URLs
URLs are generated using a custom base62 encoding (alphanumeric), resulting in short, 8-character identifiers (e.g., `AbCdEf12`). This is more user-friendly than standard UUIDs.

## 💬 Comment System

TeleNote integrates **ParaNote**, a paragraph-level commenting system.

- **Granularity**: Comments are attached to specific paragraphs.
- **Positioning**: Comments follow their paragraph even if the article is edited (using fuzzy matching and context fingerprints).
- **Likes**: Users can like individual comments.
- **Moderation**: Admin interface allows banning users (by IP/ID) and deleting comments.
- **Toggle**: Comments can be disabled globally via `ENABLE_COMMENTS=False` in `.env`.

## 🔌 API

TeleNote provides a **Telegraph-compatible API**.
See [api.md](api.md) for full documentation.

Supported methods:
- `createAccount`, `editAccountInfo`, `getAccountInfo`, `revokeAccessToken`
- `createPage`, `editPage`, `getPage`, `getPageList`, `getViews`

## 📦 Data Management

### Import / Export
- **Export**: Admin can export all notes to a single JSON file.
- **Import**: Restore notes from a JSON file. This is useful for backups or migrating between instances.
- **Format**: JSON structure containing all Note, Comment, and Account models.

## 🛠 Administration

### Django Admin
Built-in admin interface at `/admin/`.
- Manage **Notes** (view, delete).
- Manage **Comments** (view, delete).
- Manage **Banned Users**.
- Manage **Telegraph Accounts**.

### Automated Deployment
- **PythonAnywhere**: Scripts included for one-click deployment (`deploy_pa.sh`) and auto-renewal (`scripts/renew_pa.py`).
- **Docker**: `docker-compose.yml` provided for containerized deployment.

## 🧪 Security & Anti-Abuse

- **Rate Limiting**: Built-in protections against spam (configurable).
- **Content Sanitization**: Markdown is rendered safely to prevent XSS.
- **Timing Attack Protection**: Constant-time comparison for tokens.

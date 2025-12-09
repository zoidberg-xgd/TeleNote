# TeleNote API Documentation

TeleNote provides a strict subset of the [Telegra.ph API](https://telegra.ph/api), allowing it to be used as a drop-in replacement for existing Telegraph clients and tools. All endpoints communicate using JSON.

## Base URL

```
https://your-telenote-instance.com/
```

## Methods

### createAccount

Creates a new TeleNote account.

**POST** `/createAccount`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `short_name` | String | Yes | Account name, helps users with debugging. |
| `author_name` | String | No | Default author name used when creating new pages. |
| `author_url` | String | No | Default profile link for author. |

**Response (Account)**
```json
{
  "ok": true,
  "result": {
    "short_name": "Sandbox",
    "author_name": "Anonymous",
    "author_url": "",
    "access_token": "b968da509bb76866c35425099bc0989a5ec3b32997d55286c657e6994bbb",
    "auth_url": ""
  }
}
```

### createPage

Creates a new TeleNote page.

**POST** `/createPage`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `access_token` | String | Yes | Access token of the account. |
| `title` | String | Yes | Page title. |
| `content` | Array of Node | Yes | Content of the page. |
| `author_name` | String | No | Author name, displayed below the title. |
| `author_url` | String | No | Profile link, displayed below the title. |
| `return_content` | Boolean | No | If true, returns content in response. Default false. |

**Response (Page)**
```json
{
  "ok": true,
  "result": {
    "path": "Sample-Page-12-09",
    "url": "https://your-telenote-instance.com/Sample-Page-12-09",
    "title": "Sample Page",
    "description": "",
    "author_name": "Anonymous",
    "author_url": "",
    "image_url": "",
    "views": 0,
    "can_edit": true
  }
}
```

### editPage

Edits an existing TeleNote page.

**POST** `/editPage`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `access_token` | String | Yes | Access token of the account. |
| `path` | String | Yes | Path of the page. |
| `title` | String | Yes | Page title. |
| `content` | Array of Node | Yes | Content of the page. |
| `author_name` | String | No | Author name. |
| `author_url` | String | No | Author profile link. |
| `return_content` | Boolean | No | If true, returns content in response. |

**Response (Page)**

### getPage

Get a TeleNote page.

**GET/POST** `/getPage/{path}`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | String | Yes | Path of the page (e.g. `Sample-Page-12-09`). |
| `return_content` | Boolean | No | If true, returns content. Default false. |

**Response (Page)**

### getAccountInfo

Get information about a TeleNote account.

**POST** `/getAccountInfo`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `access_token` | String | Yes | Access token of the account. |
| `fields` | Array of String | No | List of fields to return (short_name, author_name, author_url, auth_url, page_count). |

**Response (Account)**

### revokeAccessToken

Revoke access token and generate a new one.

**POST** `/revokeAccessToken`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `access_token` | String | Yes | Access token of the account. |

**Response (Account)**

### getPageList

Get a list of pages belonging to a TeleNote account.

**POST** `/getPageList`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `access_token` | String | Yes | Access token of the account. |
| `offset` | Integer | No | Sequential number of the first page to return. |
| `limit` | Integer | No | Number of pages to return. |

**Response (PageList)**
```json
{
  "ok": true,
  "result": {
    "total_count": 142,
    "pages": [ ... ]
  }
}
```

### getViews

Get the number of views for a TeleNote page.

**POST** `/getViews`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | String | Yes | Path of the page. |
| `year` | Integer | No | Year. |
| `month` | Integer | No | Month. |
| `day` | Integer | No | Day. |
| `hour` | Integer | No | Hour. |

**Response (PageViews)**
```json
{
  "ok": true,
  "result": {
    "views": 42
  }
}
```

## Content Format

TeleNote uses a DOM-based format for content, identical to Telegraph.

### Node Element
A Node can be a **String** or an **Element**.

### Element
```json
{
  "tag": "p",
  "attrs": { "id": "hello" },
  "children": [ "Hello world" ]
}
```

Supported tags: `a`, `aside`, `b`, `blockquote`, `br`, `code`, `em`, `figcaption`, `figure`, `h3`, `h4`, `hr`, `i`, `iframe`, `img`, `li`, `ol`, `p`, `pre`, `s`, `strong`, `u`, `ul`, `video`.

## Differences from Telegraph

- **Self-Hosted**: You own the data.
- **Comments**: TeleNote pages support paragraph-level comments (via web UI).
- **Short URLs**: URLs are optimized for brevity (8 characters) but retain the slug format for API compatibility.
- **Images**: Images are hosted on your server (or external URLs).

# 🔌 API接口文档

> 局域网文件传输工具后端API参考

---

## 📋 基础信息

**Base URL:** `http://192.168.x.x:5000`  
**协议:** HTTP/HTTPS  
**数据格式:** JSON  

---

## 📡 接口列表

### 1. 获取历史记录

**接口：** `GET /api/history`

**说明：** 获取最近20条传输记录（用于自动刷新）

**响应：**
```json
{
    "success": true,
    "history": [
        {
            "type": "image",
            "type_name": "🖼️ 图片",
            "name": "photo.jpg",
            "filename": "20260427_103045_photo.jpg",
            "time": "2026-04-27 10:30:45",
            "content": "",
            "is_link": false
        }
    ],
    "count": 1
}
```

**字段说明：**
- `type`: 类型（image/file/text）
- `type_name`: 类型显示名称
- `name`: 显示名称
- `filename`: 实际文件名
- `time`: 传输时间
- `content`: 文本内容（仅text类型）
- `is_link`: 是否为链接

---

### 2. 上传文件

**接口：** `POST /api/upload/file`

**Content-Type:** `multipart/form-data`

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | ✅ | 要上传的文件 |

**请求示例：**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/api/upload/file', {
    method: 'POST',
    body: formData
});
```

**成功响应：**
```json
{
    "success": true,
    "filename": "20260427_103045_photo.jpg"
}
```

**失败响应：**
```json
{
    "success": false,
    "message": "不支持的文件类型"
}
```

**错误码：**
- `400`: 没有文件/文件名为空/不支持的类型
- `413`: 文件过大（>100MB）

---

### 3. 发送文本

**接口：** `POST /api/upload/text`

**Content-Type:** `application/json`

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | String | ✅ | 要发送的文本内容 |

**请求示例：**
```javascript
fetch('/api/upload/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
        text: "Hello World" 
    })
});
```

**成功响应：**
```json
{
    "success": true
}
```

**失败响应：**
```json
{
    "success": false,
    "message": "没有文本内容"
}
```

---

### 4. 下载文件

**接口：** `GET /api/download/<filename>`

**说明：** 
- 图片文件：浏览器预览（inline）
- 其他文件：强制下载（attachment）

**支持的文件类型：**

**图片（预览）：**
- PNG, JPG, JPEG, GIF, BMP, WebP

**文档（下载）：**
- PDF, DOC, DOCX, XLS, XLSX, TXT
- ZIP, RAR
- MP4, MP3, AVI, MOV

**请求示例：**
```html
<!-- HTML链接 -->
<a href="/api/download/photo.jpg" download>下载</a>

<!-- JavaScript -->
window.location.href = '/api/download/photo.jpg';
```

**响应头：**
```
Content-Type: image/jpeg
Content-Disposition: inline; filename="photo.jpg"
```

---

### 5. 删除记录

**接口：** `DELETE /api/history/delete/<filename>`

**说明：** 删除单个历史记录及对应文件

**请求示例：**
```javascript
fetch('/api/history/delete/20260427_103045_photo.jpg', {
    method: 'DELETE'
});
```

**成功响应：**
```json
{
    "success": true,
    "message": "已删除 1 条记录"
}
```

**失败响应：**
```json
{
    "success": false,
    "message": "记录不存在"
}
```

**错误码：**
- `404`: 记录不存在
- `500`: 服务器错误

---

### 6. 清空历史

**接口：** `POST /api/history/clear`

**说明：** 清空所有历史记录和文件

**请求示例：**
```javascript
fetch('/api/history/clear', {
    method: 'POST'
});
```

**成功响应：**
```json
{
    "success": true,
    "message": "已清空 5 条记录"
}
```

**警告：** ⚠️ 此操作不可恢复！

---

### 7. 列出文件

**接口：** `GET /api/files`

**说明：** 列出所有接收的文件（不包含元数据）

**响应：**
```json
{
    "success": true,
    "files": [
        {
            "filename": "20260427_103045_photo.jpg",
            "size": 102400,
            "created": "2026-04-27 10:30:45"
        }
    ]
}
```

---

### 8. 设备信息

**接口：** `GET /api/devices`

**说明：** 返回服务器信息

**响应：**
```json
{
    "success": true,
    "ip": "192.168.0.102",
    "port": 5000,
    "url": "http://192.168.0.102:5000",
    "device_name": "Windows PC",
    "status": "online"
}
```

---

## 🔐 安全说明

### CORS支持

所有接口都启用了CORS，允许跨域请求。

**响应头：**
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

### 文件大小限制

**最大上传：** 100MB

**超限响应：**
```json
{
    "success": false,
    "message": "文件过大"
}
```

**HTTP状态码：** 413 Payload Too Large

---

### 文件类型限制

**允许的扩展名：**
```python
ALLOWED_EXTENSIONS = {
    # 图片
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg',
    
    # 文档
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt',
    
    # 压缩
    'zip', 'rar',
    
    # 媒体
    'mp4', 'mp3', 'avi', 'mov'
}
```

---

## 💡 使用示例

### JavaScript完整示例

```javascript
class FileTransferAPI {
    constructor(baseUrl = 'http://192.168.0.102:5000') {
        this.baseUrl = baseUrl;
    }
    
    // 获取历史记录
    async getHistory() {
        const response = await fetch(`${this.baseUrl}/api/history`);
        return await response.json();
    }
    
    // 上传文件
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${this.baseUrl}/api/upload/file`, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    }
    
    // 发送文本
    async sendText(text) {
        const response = await fetch(`${this.baseUrl}/api/upload/text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        return await response.json();
    }
    
    // 删除记录
    async deleteRecord(filename) {
        const response = await fetch(
            `${this.baseUrl}/api/history/delete/${filename}`, 
            { method: 'DELETE' }
        );
        
        return await response.json();
    }
    
    // 清空历史
    async clearHistory() {
        const response = await fetch(`${this.baseUrl}/api/history/clear`, {
            method: 'POST'
        });
        
        return await response.json();
    }
}

// 使用示例
const api = new FileTransferAPI();

// 获取历史
api.getHistory().then(data => {
    console.log('历史记录:', data.history);
});

// 上传文件
const fileInput = document.getElementById('fileInput');
fileInput.addEventListener('change', (e) => {
    api.uploadFile(e.target.files[0]).then(result => {
        console.log('上传结果:', result);
    });
});

// 发送文本
document.getElementById('sendBtn').addEventListener('click', () => {
    const text = document.getElementById('textInput').value;
    api.sendText(text).then(result => {
        console.log('发送结果:', result);
    });
});
```

---

### Python示例

```python
import requests

BASE_URL = 'http://192.168.0.102:5000'

# 获取历史记录
response = requests.get(f'{BASE_URL}/api/history')
print(response.json())

# 上传文件
with open('photo.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(f'{BASE_URL}/api/upload/file', files=files)
    print(response.json())

# 发送文本
data = {'text': 'Hello World'}
response = requests.post(f'{BASE_URL}/api/upload/text', json=data)
print(response.json())

# 删除记录
response = requests.delete(f'{BASE_URL}/api/history/delete/photo.jpg')
print(response.json())

# 清空历史
response = requests.post(f'{BASE_URL}/api/history/clear')
print(response.json())
```

---

### cURL示例

```bash
# 获取历史记录
curl http://192.168.0.102:5000/api/history

# 上传文件
curl -X POST -F "file=@photo.jpg" http://192.168.0.102:5000/api/upload/file

# 发送文本
curl -X POST -H "Content-Type: application/json" \
     -d '{"text":"Hello"}' \
     http://192.168.0.102:5000/api/upload/text

# 删除记录
curl -X DELETE http://192.168.0.102:5000/api/history/delete/photo.jpg

# 清空历史
curl -X POST http://192.168.0.102:5000/api/history/clear
```

---

## 📊 响应状态码

| 状态码 | 说明 | 常见场景 |
|--------|------|----------|
| 200 | 成功 | 正常响应 |
| 400 | 请求错误 | 参数缺失/格式错误 |
| 404 | 未找到 | 文件/记录不存在 |
| 413 | 文件过大 | 超过100MB限制 |
| 500 | 服务器错误 | 内部异常 |

---

## 🔄 自动刷新机制

### 工作原理

前端每2秒调用一次 `/api/history` 接口，实现实时更新。

**JavaScript实现：**
```javascript
setInterval(async () => {
    const data = await fetch('/api/history').then(r => r.json());
    if (data.success) {
        updateHistoryList(data.history);
    }
}, 2000);
```

### 性能优化

- **请求频率：** 2秒/次
- **数据量：** <5KB/次
- **响应时间：** <200ms
- **CPU占用：** <5%

---

## ⚠️ 注意事项

### 1. 文件名处理

服务器会自动添加时间戳前缀避免重名：

```
原始文件名：photo.jpg
保存文件名：20260427_103045_photo.jpg
```

**API返回：** 同时返回原始文件名和实际文件名

---

### 2. 文本存储

文本内容会保存为 `.txt` 文件：

```
文件名格式：text_20260427_103045.txt
```

---

### 3. 并发限制

Flask开发服务器默认单线程，建议：

- 避免同时上传多个大文件
- 生产环境使用Gunicorn/uWSGI

---

### 4. 内存管理

历史记录存储在内存中：

```python
transfer_history = []  # 最多保留20条
```

重启服务器后历史记录清空。

---

## 📞 技术支持

遇到问题请检查：

1. **服务器状态：** 是否正常运行
2. **网络连接：** 是否在同一局域网
3. **防火墙：** 是否阻止5000端口
4. **浏览器Console：** 是否有JavaScript错误

---

<div align="center">

**完整的API文档，助力快速集成！** 🔌✨

</div>

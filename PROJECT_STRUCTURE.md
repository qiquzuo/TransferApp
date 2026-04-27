# 📂 项目结构说明

```
TransferApp/
│
├── 📄 README.md                    # 项目说明文档
├── 📄 TESTING.md                   # 测试指南
├── 📄 .gitignore                   # Git忽略配置
│
├── 🖥️ Windows服务器端
│   ├── server.py                   # Flask服务器主程序
│   ├── requirements.txt            # Python依赖包
│   ├── start_server.bat            # Windows启动脚本
│   └── received_files/             # 接收的文件存储目录（运行时自动创建）
│       ├── 20240101_120000_photo.jpg
│       ├── 20240101_120100_document.pdf
│       └── text_20240101_120200.txt
│
└── 📱 Android客户端
    └── android-app/
        ├── build.gradle            # 项目级Gradle配置
        ├── settings.gradle         # Gradle设置
        ├── gradle.properties       # Gradle属性
        │
        └── app/
            ├── build.gradle        # 应用级Gradle配置
            │
            └── src/
                └── main/
                    ├── AndroidManifest.xml          # 应用清单文件
                    │
                    ├── java/com/transferapp/filetransfer/
                    │   ├── MainActivity.kt          # 主Activity（核心逻辑）
                    │   │
                    │   ├── data/
                    │   │   └── Models.kt            # 数据模型
                    │   │
                    │   ├── network/
                    │   │   ├── ApiService.kt        # Retrofit API接口
                    │   │   └── RetrofitClient.kt    # Retrofit客户端配置
                    │   │
                    │   └── adapter/
                    │       └── HistoryAdapter.kt    # 历史记录适配器
                    │
                    └── res/
                        ├── layout/
                        │   ├── activity_main.xml    # 主界面布局
                        │   └── item_history.xml     # 历史列表项布局
                        │
                        ├── drawable/
                        │   ├── gradient_header.xml  # 渐变背景
                        │   ├── ic_server.xml        # 服务器图标
                        │   ├── ic_file.xml          # 文件图标
                        │   ├── ic_image.xml         # 图片图标
                        │   ├── ic_text.xml          # 文本图标
                        │   ├── ic_clipboard.xml     # 剪贴板图标
                        │   ├── ic_success.xml       # 成功图标
                        │   └── ic_error.xml         # 错误图标
                        │
                        ├── values/
                        │   ├── colors.xml           # 颜色定义
                        │   ├── strings.xml          # 字符串资源
                        │   └── themes.xml           # 主题样式
                        │
                        └── xml/
                            └── network_security_config.xml  # 网络安全配置
```

## 🔍 核心文件说明

### Windows端

#### `server.py` (625行)
**功能：** Flask HTTP服务器
**主要模块：**
- 自动获取局域网IP
- 生成二维码
- 文件上传接口 `/api/upload/file`
- 文本上传接口 `/api/upload/text`
- 文件下载接口 `/api/download/<filename>`
- 美观的Web界面（拖拽上传、进度条、历史记录）

**关键函数：**
- `get_local_ip()` - 获取本机IP
- `generate_qr_code()` - 生成二维码
- `upload_file()` - 处理文件上传
- `upload_text()` - 处理文本上传

#### `requirements.txt`
Python依赖包：
- flask==3.0.0 - Web框架
- flask-cors==4.0.0 - 跨域支持
- qrcode==7.4.2 - 二维码生成
- pillow==10.1.0 - 图像处理

#### `start_server.bat`
一键启动脚本，自动：
1. 检查Python是否安装
2. 安装依赖包
3. 启动服务器

### Android端

#### `MainActivity.kt` (420行)
**功能：** 主界面和业务逻辑
**主要功能：**
- 服务器连接管理
- 文件/图片选择器
- 文本输入对话框
- 系统分享意图处理
- 传输历史记录
- 权限管理

**关键方法：**
- `connectToServer()` - 连接服务器
- `uploadFile()` - 上传文件
- `uploadImage()` - 上传图片
- `sendText()` - 发送文本
- `handleShareIntent()` - 处理系统分享

#### `ApiService.kt`
Retrofit API接口定义：
- `getDeviceInfo()` - 获取设备信息
- `uploadFile()` - 上传文件（Multipart）
- `uploadText()` - 上传文本（JSON）
- `listFiles()` - 列出文件

#### `activity_main.xml`
主界面布局：
- Material Design风格
- 连接状态卡片
- 快速操作按钮网格
- 上传进度条
- 历史记录列表

#### `HistoryAdapter.kt`
RecyclerView适配器：
- 显示传输历史
- 不同类型图标
- 文件大小格式化
- 时间戳显示

## 🎨 UI设计特点

### 配色方案
- **主色调：** #667eea（紫色渐变）
- **辅助色：** #764ba2（深紫色）
- **成功色：** #48bb78（绿色）
- **错误色：** #f56565（红色）
- **背景色：** #f5f7fa（浅灰）

### 设计元素
- 圆角卡片（16dp radius）
- 渐变头部
- 阴影效果（elevation）
- Material Icons
- 流畅动画

## 🔄 数据流

### 文件上传流程
```
用户选择文件
    ↓
读取文件为字节数组
    ↓
创建MultipartBody
    ↓
Retrofit发送POST请求
    ↓
Flask接收并保存文件
    ↓
返回成功响应
    ↓
更新UI和历史记录
```

### 文本发送流程
```
用户输入文本
    ↓
检测是否为链接
    ↓
创建TextRequest对象
    ↓
Retrofit发送POST请求
    ↓
Flask保存为txt文件
    ↓
返回成功响应
    ↓
更新UI和历史记录
```

## 📊 技术架构

### 通信协议
- **HTTP/REST API**
- Content-Type: multipart/form-data（文件）
- Content-Type: application/json（文本）

### 数据存储
- **Windows端：** 文件系统（received_files文件夹）
- **Android端：** 内存列表（重启后清空）

### 异步处理
- **Android：** Kotlin Coroutines
- **Python：** Flask同步处理（可改为异步）

## 🔐 安全考虑

### 当前实现
- 仅限局域网访问
- 文件类型白名单验证
- 文件大小限制（100MB）
- 文件名安全处理（secure_filename）

### 可扩展的安全措施
- HTTPS加密传输
- 密码认证
- Token验证
- IP白名单
- 速率限制

## 🚀 性能优化建议

### 已实现的优化
- ✅ 合理的超时设置（30秒）
- ✅ 文件大小限制
- ✅ 异步网络请求
- ✅ RecyclerView复用

### 可进一步优化
- 文件分片上传（大文件）
- 图片压缩
- 缓存机制
- 断点续传
- WebSocket实时推送

## 📦 打包部署

### Windows EXE打包
```bash
pip install pyinstaller
pyinstaller --onefile --windowed server.py
```

### Android APK打包
```bash
# Debug版本
./gradlew assembleDebug

# Release版本（需要签名）
./gradlew assembleRelease
```

## 🔧 开发工具推荐

- **Python IDE：** VS Code, PyCharm
- **Android IDE：** Android Studio
- **API测试：** Postman, curl
- **网络调试：** Wireshark, Charles
- **UI设计：** Figma, Adobe XD

---

**祝开发愉快！** 💻✨

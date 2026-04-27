# 📱 局域网文件传输助手

一个轻量级的跨平台文件传输工具，支持在Windows电脑和Android手机之间快速传输文件、图片和文本。

## ✨ 功能特性

- 🚀 **快速传输**：同一WiFi/热点下直接传输，无需互联网
- 📁 **多格式支持**：图片、文档、视频、音频等各种文件类型
- 📝 **文本分享**：支持纯文本和链接快速传输
- 🎨 **美观界面**：Material Design设计，支持拖拽上传
- 📋 **剪贴板集成**：一键粘贴剪贴板内容
- 🔄 **系统分享**：支持从其他App直接分享内容到此应用
- 📊 **传输历史**：记录所有传输历史，方便查看

## 🖥️ Windows端使用

### 方法一：直接运行（推荐）

1. **安装Python**（如果未安装）
   - 访问 https://www.python.org/downloads/
   - 下载并安装Python 3.8或更高版本

2. **启动服务器**
   ```bash
   # 双击运行
   start_server.bat
   
   # 或命令行运行
   python server.py
   ```

3. **查看服务器地址**
   - 启动后会显示类似：`http://192.168.1.100:5000`
   - 同时会生成二维码，手机可扫描访问

4. **浏览器访问**（可选）
   - 在手机浏览器中输入显示的地址
   - 可直接通过网页上传文件，无需安装App

### 方法二：打包成exe（可选）

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包成exe
pyinstaller --onefile --windowed --name=FileTransferServer server.py

# 生成的exe在 dist 文件夹中
```

## 📱 Android端使用

### 方法一：使用Android Studio编译

1. **打开项目**
   - 用Android Studio打开 `android-app` 文件夹

2. **同步Gradle**
   - 等待Gradle同步完成
   - 确保网络连接正常

3. **连接手机**
   - 开启USB调试模式
   - 点击Run按钮安装到手机

4. **生成APK**
   - Build → Build Bundle(s) / APK(s) → Build APK(s)
   - APK位置：`app/build/outputs/apk/debug/app-debug.apk`

### 方法二：直接使用Web界面（无需安装App）

如果不想安装App，可以直接用手机浏览器访问Windows服务器提供的地址，功能完全相同！

## 🚀 快速开始

### 首次使用步骤

1. **确保设备在同一网络**
   - Windows电脑和Android手机连接同一个WiFi或热点

2. **启动Windows服务器**
   ```bash
   cd TransferApp
   start_server.bat
   ```

3. **查看IP地址**
   - 服务器启动后会显示IP地址，例如：`192.168.1.100`

4. **配置Android App**
   - 打开App
   - 输入显示的IP地址
   - 点击"连接服务器"

5. **开始传输**
   - 点击相应按钮发送文件、图片或文本
   - 或使用系统分享功能

## 📖 使用示例

### 发送图片

1. 点击"🖼️ 图片"按钮
2. 从相册选择图片
3. 自动上传到电脑

### 发送文件

1. 点击"📁 文件"按钮
2. 选择要发送的文件
3. 等待上传完成

### 发送文本/链接

**方式一：手动输入**
1. 点击"📝 文本"按钮
2. 输入文本或链接
3. 点击发送

**方式二：从剪贴板**
1. 复制任意文本
2. 点击"📋 粘贴"按钮
3. 自动发送剪贴板内容

**方式三：系统分享**
1. 在其他App中点击"分享"
2. 选择"文件传输助手"
3. 自动发送到电脑

### 电脑接收文件

- 所有接收的文件保存在 `received_files` 文件夹
- 可通过Web界面查看和下载历史记录

## 🔧 常见问题

### 1. 连接失败怎么办？

**检查清单：**
- ✅ 确认手机和电脑在同一WiFi网络
- ✅ 确认Windows防火墙允许Python访问网络
- ✅ 确认输入的IP地址正确
- ✅ 尝试关闭电脑防火墙后重试

**Windows防火墙设置：**
```
控制面板 → Windows Defender 防火墙 → 允许应用通过防火墙
→ 找到Python → 勾选专用和公用
```

### 2. 如何查看本机IP地址？

**Windows命令提示符：**
```cmd
ipconfig
```
查找 "无线局域网适配器 WLAN" 下的 "IPv4 地址"

### 3. 传输速度慢？

- 确保WiFi信号良好
- 避免传输超大文件（建议<100MB）
- 关闭其他占用网络的程序

### 4. 文件保存在哪里？

- 默认保存在程序目录下的 `received_files` 文件夹
- 可在代码中修改 `UPLOAD_FOLDER` 变量更改路径

### 5. 支持哪些文件类型？

**支持的格式：**
- 图片：png, jpg, jpeg, gif, bmp
- 文档：pdf, doc, docx, xls, xlsx, txt
- 压缩：zip, rar
- 媒体：mp4, mp3

可在 `server.py` 的 `ALLOWED_EXTENSIONS` 中添加更多类型。

## 🛠️ 技术栈

### Windows端
- **Python 3.8+**
- **Flask** - Web框架
- **Flask-CORS** - 跨域支持
- **QRCode** - 二维码生成
- **Pillow** - 图像处理

### Android端
- **Kotlin**
- **Material Design Components**
- **Retrofit** - HTTP客户端
- **Glide** - 图片加载
- **Coroutines** - 异步处理

## 📝 开发说明

### 修改服务器端口

编辑 `server.py` 最后一行：
```python
app.run(host='0.0.0.0', port=5000, debug=False)
# 修改 port=5000 为其他端口
```

### 修改文件大小限制

编辑 `server.py`：
```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
# 修改为需要的值
```

### 添加文件类型白名单

编辑 `server.py`：
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', ...}
# 添加新的扩展名
```

## 🔒 安全说明

⚠️ **注意事项：**
- 此工具仅适用于可信的局域网环境
- 不建议在公共WiFi中使用
- 如需增强安全性，可添加密码验证

## 📄 许可证

MIT License - 自由使用和修改

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题或建议，欢迎反馈！

---

**享受便捷的文件传输体验！** 🎉

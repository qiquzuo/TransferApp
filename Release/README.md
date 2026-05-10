# 📱 TransferApp - 局域网文件传输助手

<div align="center">

[![Stars](https://img.shields.io/github/stars/qiquzuo/TransferApp?style=for-the-badge&logo=github)]()
[![Forks](https://img.shields.io/github/forks/qiquzuo/TransferApp?style=for-the-badge&logo=github)]()
[![License](https://img.shields.io/github/license/qiquzuo/TransferApp?style=for-the-badge)]()
[![Release](https://img.shields.io/github/v/release/qiquzuo/TransferApp?style=for-the-badge&logo=github)]()
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Android-green?style=for-the-badge)]()

**跨平台局域网文件传输工具 | Windows ↔ Android | 无需互联网 | 开源免费**

[⬇️ 下载最新版](https://github.com/qiquzuo/TransferApp/releases/latest) · 
[📖 使用文档](#-快速开始) · 
[🐛 报告问题](https://github.com/qiquzuo/TransferApp/issues) · 
[💬 讨论交流](https://github.com/qiquzuo/TransferApp/discussions)

</div>

---

## ✨ 特性亮点

- 🚀 **极速传输** - 局域网直连，速度可达10MB/s+，无文件大小限制
- 📁 **全格式支持** - 图片、文档、视频、音频等任意文件类型
- 📝 **文本分享** - 支持纯文本和链接快速传输，Enter即可发送
- 🎨 **现代UI** - 玻璃拟态设计，美观易用，响应式布局
- ⚡ **实时同步** - 1秒自动刷新传输历史，新内容即时显示
- 🔑 **零安装** - 便携版解压即用，手机端浏览器访问
- 🔄 **双向传输** - 电脑→手机、手机→电脑随意传
- 📋 **智能粘贴** - 一键粘贴剪贴板内容，快捷高效
- 🖼️ **图片预览** - 直接在浏览器中预览图片，无需下载
- 🔒 **隐私保护** - 纯局域网传输，数据不经过云端

---

## 🎯 适用场景

✅ **办公室协作** - 同事间快速分享文件，告别微信压缩  
✅ **照片备份** - 手机照片批量传到电脑，保留原图质量  
✅ **文件查看** - 电脑文件发送到手机随时查看  
✅ **大文件传输** - GB级文件轻松传输，无大小限制  
✅ **隐私保护** - 敏感文件局域网传输，不经过第三方服务器  
✅ **临时分享** - 快速分享链接和文本，无需登录任何账号  

---

## 🚀 快速开始

### 方法一：便携版（推荐⭐⭐⭐⭐⭐）

**无需安装Python，开箱即用！**

1. **下载** [最新Release](https://github.com/qiquzuo/TransferApp/releases/latest)
2. **解压** ZIP文件到任意目录
3. **运行** 双击 `start_server.bat`
4. **访问** 浏览器打开显示的地址（如 `http://192.168.1.100:5000`）
5. **扫码** 手机扫描二维码或手动输入URL

**就这么简单！** 🎉

---

### 方法二：源码运行

适合开发者或需要自定义的用户。

```bash
# 1. 克隆仓库
git clone https://github.com/qiquzuo/TransferApp.git
cd TransferApp

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务器
python server.py

# 4. 浏览器访问显示的地址
```

---

### 方法三：Android App（可选）

如果更喜欢原生App体验：

1. 下载 `android-app/app/build/outputs/apk/release/app-release.apk`
2. 在Android手机上安装
3. 打开App，扫描电脑端二维码
4. 开始传输文件

---

## 📸 界面预览

### 💻 电脑端

![Desktop UI](screenshots/desktop.png)

*玻璃拟态设计，左右分栏布局，拖拽上传*

---

### 📱 手机端

![Mobile UI](screenshots/mobile.png)

*垂直流式布局，触摸友好，操作便捷*

---

### 🎬 功能演示

![Demo GIF](screenshots/demo.gif)

*文件传输、文本发送、实时同步*

> **注意：** 截图将在下次更新时添加。欢迎贡献精美截图！

---

## 💡 使用技巧

### ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Enter` | 快速发送文本 |
| `Shift + Enter` | 文本换行 |
| `Ctrl + V` | 粘贴剪贴板内容 |
| 拖拽文件 | 批量上传 |

---

### 🎯 最佳实践

1. **网络环境**
   - 确保电脑和手机在同一WiFi网络
   - 使用5GHz WiFi可获得更快速度
   - 大文件建议使用有线网络连接

2. **传输优化**
   - 批量文件可一次性拖拽上传
   - 文本内容支持多行输入（Shift+Enter换行）
   - 图片可直接在浏览器中预览

3. **管理建议**
   - 定期清理 `received_files` 目录
   - 使用删除按钮移除不需要的记录
   - 重要文件及时下载到本地

---

## 🔧 技术栈

### 后端
- **Flask** - 轻量级Web框架
- **PyInstaller** - Python打包工具
- **Flask-Limiter** - API速率限制
- **Pillow** - 图像处理
- **qrcode** - 二维码生成

### 前端
- **原生HTML/CSS/JavaScript** - 无框架依赖
- **响应式设计** - 自适应各种屏幕
- **AJAX** - 异步数据加载
- **Glassmorphism** - 玻璃拟态UI

### 移动端
- **Kotlin** - Android原生开发
- **Retrofit** - 网络请求库
- **Material Design** - 设计规范

---

## 📊 性能对比

| 特性 | TransferApp | 微信文件传输 | QQ文件传输 | 蓝牙传输 |
|------|-------------|--------------|------------|----------|
| **传输速度** | ⚡⚡⚡⚡⚡ 10MB/s+ | ⭐⭐ 1-2MB/s | ⭐⭐⭐ 2-3MB/s | ⭐ 0.5MB/s |
| **文件大小** | ❌ 无限制 | ✅ 最大1GB | ✅ 最大4GB | ✅ 有限制 |
| **图片质量** | ✅ 原图无损 | ❌ 自动压缩 | ❌ 自动压缩 | ✅ 原图 |
| **隐私保护** | ✅ 纯局域网 | ❌ 经过云端 | ❌ 经过云端 | ✅ 点对点 |
| **无需安装** | ✅ 是 | ❌ 需要微信 | ❌ 需要QQ | ✅ 是 |
| **跨平台** | ✅ Win+Android | ✅ 全平台 | ✅ 全平台 | ❌ 受限 |

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！让TransferApp变得更好。

### 如何贡献

1. **Fork** 本仓库
2. **创建** 特性分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **开启** Pull Request

### 贡献方向

- 🐛 修复Bug
- ✨ 新增功能
- 🎨 优化UI/UX
- 📝 完善文档
- 🌍 多语言支持
- 🧪 编写测试

### 开发环境设置

```bash
# 克隆你的Fork
git clone https://github.com/YOUR_USERNAME/TransferApp.git
cd TransferApp

# 安装依赖
pip install -r requirements.txt

# 运行服务器
python server.py
```

---

## 📄 许可证

本项目采用 **MIT 许可证** - 详见 [LICENSE](LICENSE) 文件

您可以自由使用、修改和分发本项目，只需保留原始版权声明。

---

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

特别感谢：
- Flask团队提供的优秀Web框架
- 所有提出建议和报告Bug的用户
- 每一位Star和Fork的支持者

---

## 📞 联系方式

- 📧 Email: [您的邮箱]
- 🐦 Twitter: [@您的Twitter]
- 💬 GitHub Discussions: [讨论区](https://github.com/qiquzuo/TransferApp/discussions)
- 🐛 Issues: [问题反馈](https://github.com/qiquzuo/TransferApp/issues)

---

## 🌟 支持项目

如果这个项目对你有帮助，请考虑：

1. ⭐ **Star** 这个仓库
2. 🔄 **Share** 分享给需要的朋友
3. 🐛 **Report** 发现的问题
4. 💡 **Suggest** 新功能建议
5. 💰 **Sponsor** [赞助开发者](https://github.com/sponsors/qiquzuo)

您的支持是我持续改进的动力！❤️

---

<div align="center">

**Made with ❤️ by [qiquzuo](https://github.com/qiquzuo)**

[⬆️ 回到顶部](#-transferapp---局域网文件传输助手)

**如果这个项目对您有帮助，请给个 ⭐ Star 吧！**

</div>

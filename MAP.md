# 🗺️ 项目导航地图

```
                    🎯 局域网文件传输助手
                         TransferApp
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
        🖥️ Windows        📱 Android       📚 文档
        服务器端           客户端           
            │                 │                 │
    ┌───────┴───────┐  ┌─────┴─────┐   ┌──────┴──────┐
    │               │  │           │   │             │
 server.py      启动脚本   app源码    资源文件   8个Markdown
 requirements.txt  .bat   (Kotlin)  (XML/图片)   文档
```

---

## 🚀 快速导航

### 👤 我是普通用户，想立即使用

```
开始
  ↓
📖 阅读 QUICKSTART.md（5分钟）
  ↓
🖥️ 运行 start_server.bat
  ↓
📱 手机浏览器访问显示的IP地址
  ↓
✅ 开始传输文件
  ↓
需要更多功能？ → 📖 阅读 README.md
```

---

### 👨‍💻 我是开发者，想理解代码

```
开始
  ↓
📖 阅读 INDEX.md（了解文档结构）
  ↓
📖 阅读 PROJECT_STRUCTURE.md（了解代码架构）
  ↓
🔍 查看核心文件：
  ├─ server.py（后端逻辑）
  ├─ MainActivity.kt（前端逻辑）
  ├─ ApiService.kt（API接口）
  └─ activity_main.xml（UI布局）
  ↓
📖 阅读 UI_DESIGN.md（了解设计规范）
  ↓
🔧 开始修改和扩展
```

---

### 🧪 我是测试人员，想全面测试

```
开始
  ↓
📖 阅读 QUICKSTART.md（了解基本操作）
  ↓
📖 阅读 TESTING.md（获取测试清单）
  ↓
✅ 执行功能测试
  ├─ 基础功能测试
  ├─ 兼容性测试
  └─ 性能测试
  ↓
📝 记录测试结果
  ↓
发现问题？ → 🐛 提交Issue
```

---

### 🎨 我是设计师，想优化界面

```
开始
  ↓
📖 阅读 UI_DESIGN.md（了解当前设计）
  ↓
🎨 查看配色方案和布局规范
  ↓
🔍 分析现有UI组件：
  ├─ Web界面（server.py中的HTML）
  └─ Android界面（res/layout/*.xml）
  ↓
✏️ 设计改进方案
  ↓
🔧 修改代码实现新设计
```

---

## 📂 文件关系图

```
TransferApp/
│
├── 🖥️ Windows服务器
│   ├── server.py ←── 核心服务器代码
│   │     ├── 自动获取IP
│   │     ├── 生成二维码
│   │     ├── API接口（5个）
│   │     └── Web界面（HTML/CSS/JS）
│   │
│   ├── requirements.txt ←── Python依赖
│   │     ├── flask
│   │     ├── flask-cors
│   │     ├── qrcode
│   │     └── pillow
│   │
│   └── start_server.bat ←── 一键启动
│         ├── 检查Python
│         ├── 安装依赖
│         └── 启动server.py
│
├── 📱 Android客户端
│   └── android-app/
│         ├── build.gradle ←── 项目配置
│         ├── settings.gradle
│         ├── gradle.properties
│         │
│         └── app/
│               ├── build.gradle ←── 应用配置
│               │
│               └── src/main/
│                     ├── AndroidManifest.xml ←── 权限和Activity声明
│                     │
│                     ├── java/com/transferapp/filetransfer/
│                     │     ├── MainActivity.kt ←── 主界面逻辑
│                     │     │     ├── 连接服务器
│                     │     │     ├── 上传文件/图片
│                     │     │     ├── 发送文本
│                     │     │     └── 处理系统分享
│                     │     │
│                     │     ├── data/
│                     │     │     └── Models.kt ←── 数据模型
│                     │     │
│                     │     ├── network/
│                     │     │     ├── ApiService.kt ←── API接口定义
│                     │     │     └── RetrofitClient.kt ←── 网络客户端
│                     │     │
│                     │     └── adapter/
│                     │           └── HistoryAdapter.kt ←── 列表适配器
│                     │
│                     └── res/
│                           ├── layout/
│                           │     ├── activity_main.xml ←── 主界面布局
│                           │     └── item_history.xml ←── 列表项布局
│                           │
│                           ├── drawable/ ←── 图标和背景
│                           │     ├── gradient_header.xml
│                           │     ├── ic_server.xml
│                           │     ├── ic_file.xml
│                           │     ├── ic_image.xml
│                           │     ├── ic_text.xml
│                           │     ├── ic_clipboard.xml
│                           │     ├── ic_success.xml
│                           │     └── ic_error.xml
│                           │
│                           ├── values/
│                           │     ├── colors.xml ←── 颜色定义
│                           │     ├── strings.xml ←── 字符串
│                           │     └── themes.xml ←── 主题样式
│                           │
│                           └── xml/
│                                 └── network_security_config.xml
│
└── 📚 文档
      ├── INDEX.md ←── 📑 文档索引（从这里开始）
      ├── QUICKSTART.md ←── ⚡ 5分钟快速上手
      ├── README.md ←── 📖 完整使用说明
      ├── TESTING.md ←── 🧪 测试指南
      ├── PROJECT_STRUCTURE.md ←── 📂 项目结构
      ├── UI_DESIGN.md ←── 🎨 界面设计
      ├── SUMMARY.md ←── 📊 项目总结
      ├── CHECKLIST.md ←── ✅ 完成清单
      └── .gitignore ←── Git配置
```

---

## 🔄 数据流图

### 文件上传流程

```
📱 Android App                    🖥️ Windows Server
      │                                  │
      │  1. 用户选择文件                  │
      │     ↓                            │
      │  2. 读取文件为字节数组             │
      │     ↓                            │
      │  3. 创建MultipartBody            │
      │     ↓                            │
      │  4. POST /api/upload/file ──────→│
      │                                  │  5. 接收文件
      │                                  │     ↓
      │                                  │  6. 验证文件类型和大小
      │                                  │     ↓
      │                                  │  7. 保存到received_files/
      │                                  │     ↓
      │  8. 返回成功响应 ←───────────────│
      │     ↓                            │
      │  9. 更新UI显示成功                │
      │     ↓                            │
      │  10. 添加到历史记录               │
```

### 文本发送流程

```
📱 Android App                    🖥️ Windows Server
      │                                  │
      │  1. 用户输入文本                  │
      │     ↓                            │
      │  2. 检测是否为链接                │
      │     ↓                            │
      │  3. POST /api/upload/text ──────→│
      │         {text: "..."}            │
      │                                  │  4. 接收JSON数据
      │                                  │     ↓
      │                                  │  5. 保存为.txt文件
      │                                  │     ↓
      │  6. 返回成功响应 ←───────────────│
      │     ↓                            │
      │  7. 更新UI和历史记录              │
```

### 系统分享流程

```
其他App（微信/QQ等）          📱 Android App           🖥️ Windows Server
        │                         │                          │
        │  1. 用户点击"分享"       │                          │
        │     ↓                    │                          │
        │  2. 选择"文件传输助手"    │                          │
        │     ↓                    │                          │
        │  3. Intent发送数据 ─────→│                          │
        │                          │  4. 解析Intent           │
        │                          │     ↓                    │
        │                          │  5. 调用上传方法         │
        │                          │     ↓                    │
        │                          │  6. POST请求 ──────────→│
        │                          │                          │  7. 保存文件
        │                          │  8. 显示成功 ←──────────│
        │                          │     ↓                    │
        │                          │  9. 通知用户             │
```

---

## 🎯 功能模块图

```
                    ┌─────────────────────┐
                    │   用户交互层          │
                    │  (Web界面 + App)     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   业务逻辑层          │
                    │  (MainActivity      │
                    │   + server.py)      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   网络通信层          │
                    │  (Retrofit          │
                    │   + Flask API)      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   数据存储层          │
                    │  (文件系统           │
                    │   received_files/)  │
                    └─────────────────────┘
```

---

## 📊 技术栈关系图

```
前端（Android）                  后端（Python）
┌──────────────┐               ┌──────────────┐
│   Kotlin     │               │    Flask     │
│   Material   │◄──HTTP/Retrofit─►│   Flask-CORS│
│   Design     │   JSON/Multipart│   QRCode   │
└──────────────┘               └──────────────┘
       │                               │
       │                               │
┌──────▼──────┐               ┌────────▼────────┐
│  Retrofit   │               │  File System    │
│  Glide      │               │  received_files │
└─────────────┘               └─────────────────┘
```

---

## 🗂️ 文档阅读路径

```
新用户：
INDEX.md → QUICKSTART.md → README.md → 开始使用
                                    ↓
                              遇到问题？
                                    ↓
                              TESTING.md

开发者：
INDEX.md → PROJECT_STRUCTURE.md → 阅读源码
                                    ↓
                              想修改UI？
                                    ↓
                              UI_DESIGN.md

                              想了解全貌？
                                    ↓
                              SUMMARY.md

测试者：
INDEX.md → TESTING.md → 执行测试 → 记录问题
```

---

## 🔍 常见问题定位

```
问题：无法连接服务器
  ↓
查看：TESTING.md → 常见问题1
  ↓
可能原因：
  ├─ 不在同一WiFi → 检查网络
  ├─ 防火墙阻止 → 设置防火墙
  ├─ IP地址错误 → 重新获取IP
  └─ 服务器未启动 → 运行start_server.bat

问题：上传失败
  ↓
查看：TESTING.md → 常见问题3
  ↓
可能原因：
  ├─ 文件太大 → 检查文件大小
  ├─ 格式不支持 → 查看白名单
  └─ 网络中断 → 检查连接

问题：如何修改界面颜色？
  ↓
查看：UI_DESIGN.md → 配色方案
  ↓
修改位置：
  ├─ Web界面 → server.py中的CSS
  └─ Android → res/values/colors.xml
```

---

## 🎓 学习路径建议

```
第1天：熟悉使用
  ├─ 阅读 QUICKSTART.md
  ├─ 实际操作一遍
  └─ 掌握基本功能

第2天：深入理解
  ├─ 阅读 README.md
  ├─ 阅读 PROJECT_STRUCTURE.md
  └─ 理解代码结构

第3天：定制修改
  ├─ 尝试修改UI颜色
  ├─ 添加新的文件类型
  └─ 调整功能参数

第4天+：扩展开发
  ├─ 添加新功能
  ├─ 优化性能
  └─ 打包发布
```

---

<div align="center">

## 🎯 从这里开始

**[⬆️ INDEX.md - 文档总索引](INDEX.md)**  
**[⚡ QUICKSTART.md - 5分钟上手](QUICKSTART.md)**  
**[📖 README.md - 完整说明](README.md)**

祝探索愉快！🚀

</div>

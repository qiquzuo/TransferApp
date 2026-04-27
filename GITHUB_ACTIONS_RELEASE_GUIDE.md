# 🚀 GitHub Actions 自动发布指南

**日期：** 2026-04-27  
**版本：** v1.0  
**状态：** ✅ 已配置

---

## 📋 概述

本项目已配置GitHub Actions工作流，可以自动将便携版ZIP文件上传到GitHub Releases。

---

## ⚙️ 触发方式

### 方式1：推送版本标签（推荐）⭐

```bash
# 1. 提交代码更改
git add .
git commit -m "更新说明"

# 2. 创建版本标签
git tag v1.0.0

# 3. 推送标签到GitHub
git push origin v1.0.0
```

**效果：**
- ✅ 自动触发构建
- ✅ 自动生成exe
- ✅ 自动打包ZIP
- ✅ 自动上传到Releases
- ✅ ZIP文件名：`FileTransferServer_Portable_v1.0.0.zip`

---

### 方式2：手动触发

1. 进入GitHub仓库页面
2. 点击 **Actions** 标签
3. 选择 **📦 Auto Release Portable Version**
4. 点击 **Run workflow** 按钮
5. 选择分支（通常选main/master）
6. 点击 **Run workflow**

**效果：**
- ✅ 立即触发构建
- ✅ ZIP文件名使用时间戳：`FileTransferServer_Portable_v20260427_120000.zip`

---

## 📁 工作流程详解

### 步骤1：检出代码
```yaml
uses: actions/checkout@v4
```
- 从GitHub拉取最新代码

---

### 步骤2：设置Python环境
```yaml
uses: actions/setup-python@v5
with:
  python-version: '3.10'
```
- 安装Python 3.10
- 配置pip

---

### 步骤3：安装依赖
```bash
pip install -r requirements.txt
pip install pyinstaller
```
- 安装Flask等依赖
- 安装PyInstaller打包工具

---

### 步骤4：构建exe
```bash
pyinstaller --onefile --windowed --name=FileTransferServer server.py
```
- 生成独立的exe文件
- 位于 `dist/FileTransferServer.exe`

---

### 步骤5：准备发布文件
```
release_package/
├── FileTransferServer.exe    # 主程序
├── start_server.bat          # 启动脚本
├── README.md                 # 使用说明
├── requirements.txt          # 依赖列表
└── received_files/           # 接收文件目录
```

---

### 步骤6：压缩为ZIP
```powershell
Compress-Archive -Path release_package\* -DestinationPath FileTransferServer_Portable_v1.0.0.zip
```

---

### 步骤7：上传到Releases
```yaml
uses: softprops/action-gh-release@v1
with:
  files: FileTransferServer_Portable_v1.0.0.zip
  name: "📦 TransferApp v1.0.0"
  body: |
    ## 🚀 局域网文件传输助手 - 便携版
    ...
```

---

## 🔧 自定义配置

### 修改版本号规则

编辑 `.github/workflows/auto-release.yml`：

```yaml
on:
  push:
    tags:
      - 'v*'        # 当前：匹配 v1.0.0, v2.1.0 等
      # 可改为：
      - 'release/*' # 匹配 release/1.0.0
      - '*.*.*'     # 匹配 1.0.0（无前缀）
```

---

### 修改Python版本

```yaml
uses: actions/setup-python@v5
with:
  python-version: '3.10'  # 可改为 3.8, 3.9, 3.11 等
```

---

### 添加更多文件到ZIP

```yaml
- name: 📋 Prepare Release Files
  run: |
    mkdir release_package
    Copy-Item dist\FileTransferServer.exe release_package\
    Copy-Item start_server.bat release_package\
    Copy-Item README.md release_package\
    # 添加新文件：
    Copy-Item CHANGELOG.md release_package\
    Copy-Item LICENSE release_package\
```

---

### 设置为预发布

```yaml
- name: 📤 Upload to GitHub Releases
  uses: softprops/action-gh-release@v1
  with:
    prerelease: true  # 改为true表示预发布
```

---

### 创建草稿版本

```yaml
- name: 📤 Upload to GitHub Releases
  uses: softprops/action-gh-release@v1
  with:
    draft: true  # 改为true表示草稿，需手动发布
```

---

## 📊 查看构建状态

### 方法1：GitHub网页

1. 访问：`https://github.com/你的用户名/TransferApp/actions`
2. 查看工作流运行状态
3. 点击具体运行查看详细日志

---

### 方法2：命令行

```bash
# 查看最近的workflow运行
gh run list

# 查看具体运行的日志
gh run view <run-id>
```

需要先安装GitHub CLI：
```bash
winget install GitHub.cli
```

---

## ⚠️ 常见问题

### Q1: 构建失败，提示找不到requirements.txt

**解决：**
确保项目根目录有 `requirements.txt` 文件

```txt
flask
flask-cors
pillow
qrcode
```

---

### Q2: ZIP文件太大

**原因：** PyInstaller打包包含所有依赖

**优化方案：**
```yaml
- name: 🔨 Build Executable
  run: |
    # 使用UPX压缩exe（减小体积）
    pip install pyinstaller
    pyinstaller --onefile --windowed --upx-dir=upx --name=FileTransferServer server.py
```

---

### Q3: 如何删除旧的Releases？

**方法1：网页操作**
1. 进入Releases页面
2. 点击要删除的版本
3. 点击 **Delete this release**

**方法2：命令行**
```bash
gh release delete v1.0.0
```

---

### Q4: 如何只上传已有的ZIP文件？

如果想上传本地已打包好的ZIP（如 `FileTransferServer_Portable_v2.0.zip`），创建单独的工作流：

```yaml
name: 📤 Upload Existing ZIP

on:
  workflow_dispatch:
    inputs:
      zip_file:
        description: 'ZIP文件名'
        required: true
        default: 'FileTransferServer_Portable_v2.0.zip'

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: 📤 Upload to Releases
        uses: softprops/action-gh-release@v1
        with:
          files: ${{ github.event.inputs.zip_file }}
          tag_name: ${{ github.event.inputs.zip_file }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🎯 最佳实践

### 1. 语义化版本控制

```bash
# 主版本号.次版本号.修订号
git tag v1.0.0    # 第一个稳定版
git tag v1.1.0    # 新增功能
git tag v1.1.1    # Bug修复
git tag v2.0.0    # 重大更新
```

---

### 2. 编写清晰的Release说明

在tag消息中包含更新内容：

```bash
git tag -a v1.0.0 -m "
🚀 首次正式发布

✨ 新功能：
- 支持文件传输
- 支持文本分享
- 美观的Web界面

🐛 Bug修复：
- 修复图片预览问题
- 修复自动刷新

📝 其他：
- 优化UI设计
- 提升性能
"
git push origin v1.0.0
```

---

### 3. 定期清理旧版本

保留最近5个版本，删除更早的：

```bash
# 列出所有releases
gh release list

# 删除旧版本
gh release delete v0.1.0
gh release delete v0.2.0
```

---

### 4. 使用CHANGELOG

在项目根目录创建 `CHANGELOG.md`：

```markdown
# 更新日志

## [1.0.0] - 2026-04-27

### Added
- 初始版本发布
- 支持文件传输
- 支持文本分享

### Changed
- 优化UI设计
- 提升性能

### Fixed
- 修复图片预览问题
```

并在workflows中复制到ZIP包。

---

## 📈 进阶用法

### 多平台构建

同时构建Windows、Linux、macOS版本：

```yaml
jobs:
  build-windows:
    runs-on: windows-latest
    # Windows构建步骤...
  
  build-linux:
    runs-on: ubuntu-latest
    # Linux构建步骤...
  
  build-macos:
    runs-on: macos-latest
    # macOS构建步骤...
```

---

### 自动递增版本号

使用工具自动管理版本：

```yaml
- name: 🏷️ Bump Version
  uses: anothrNick/github-tag-action@1.34.0
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    WITH_V: true
    DEFAULT_BUMP: patch
```

---

### 通知机制

构建完成后发送通知：

```yaml
- name: 📢 Notify Discord
  if: success()
  uses: Ilshidur/action-discord@master
  env:
    DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
  with:
    args: "✅ 新版本 ${{ env.ZIP_NAME }} 已发布！"
```

---

## 🔗 相关资源

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [softprops/action-gh-release](https://github.com/softprops/action-gh-release)
- [PyInstaller文档](https://pyinstaller.org/)
- [语义化版本控制](https://semver.org/)

---

## 🎊 总结

### 快速开始

```bash
# 1. 提交代码
git add .
git commit -m "更新说明"

# 2. 创建标签
git tag v1.0.0

# 3. 推送标签
git push origin v1.0.0

# 4. 等待构建完成（约2-3分钟）

# 5. 查看Releases
# https://github.com/你的用户名/TransferApp/releases
```

---

### 优势

✅ **自动化** - 无需手动打包  
✅ **一致性** - 每次构建环境相同  
✅ **可追溯** - 完整的构建日志  
✅ **便捷性** - 一键发布  

---

<div align="center">

**🚀 现在可以轻松发布新版本了！**

**只需推送tag，其余交给GitHub Actions！** ✨

</div>

# 👨‍💻 开发者指南

> 项目架构、开发规范和扩展指南

---

## 📐 项目架构

### 技术栈

**后端：**
- Python 3.8+
- Flask 3.0（Web框架）
- Flask-CORS（跨域支持）
- QRCode（二维码生成）
- Pillow（图像处理）

**前端：**
- HTML5/CSS3
- JavaScript (ES6+)
- Fetch API
- CSS Grid/Flexbox

**Android客户端（可选）：**
- Kotlin 1.9
- Material Design
- Retrofit 2.9
- Glide 4.16

---

## 🏗️ 代码结构

```
TransferApp/
├── server.py              # Flask主服务器（282行）
│   ├── 路由定义
│   ├── API接口
│   └── 设备检测逻辑
│
├── web_templates.py       # Web界面模板（1009行）
│   ├── get_desktop_html_template()  # 电脑端UI
│   └── get_mobile_html_template()   # 手机端UI
│
├── android-app/           # Android客户端
│   ├── app/src/main/java/ # Kotlin源码
│   └── app/src/main/res/  # 资源文件
│
├── received_files/        # 文件存储目录
├── requirements.txt       # Python依赖
└── docs/                  # 文档目录
```

---

## 🔑 核心模块

### 1. 设备检测

**位置：** `server.py` 第65-74行

```python
@app.route('/')
def index():
    # 检测设备类型
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(keyword in user_agent for keyword in [
        'mobile', 'android', 'iphone', 'ipad'
    ])
    
    if is_mobile:
        html_template = get_mobile_html_template()
    else:
        html_template = get_desktop_html_template()
    
    return render_template_string(html_template, ...)
```

**工作原理：**
- 分析User-Agent字符串
- 匹配移动设备关键词
- 返回对应的HTML模板

---

### 2. 自动刷新

**位置：** `web_templates.py` JavaScript部分

**核心函数：**
```javascript
// 启动自动刷新
function startAutoRefresh() {
    autoRefreshInterval = setInterval(() => {
        if (isAutoRefreshEnabled) {
            loadHistory();
        }
    }, REFRESH_INTERVAL); // 2000ms
}

// 加载历史记录
async function loadHistory() {
    const response = await fetch('/api/history');
    const data = await response.json();
    updateHistoryList(data.history);
}

// 智能更新DOM
function updateHistoryList(history) {
    // 检测新记录
    // 生成HTML
    // 添加高亮动画
}
```

---

### 3. 文件处理

**上传流程：**
```
用户选择文件
    ↓
POST /api/upload/file
    ↓
验证文件类型和大小
    ↓
添加时间戳前缀
    ↓
保存到 received_files/
    ↓
添加到 transfer_history
    ↓
返回成功响应
```

**关键代码：**
```python
@app.route('/api/upload/file', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    # 验证
    if not allowed_file(file.filename):
        return jsonify({'success': False}), 400
    
    # 保存
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_')
    filename = timestamp + secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # 记录历史
    transfer_history.append({...})
    
    return jsonify({'success': True})
```

---

## 🎨 UI设计系统

### 颜色方案

**主色调：**
```css
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
--success-gradient: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
```

**语义色：**
- 主要操作：紫色渐变
- 次要操作：粉色渐变
- 成功状态：绿色渐变
- 删除操作：红色渐变

---

### 布局系统

**电脑端：**
```css
.container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    max-width: 1400px;
}
```

**手机端：**
```css
.content {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.action-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}
```

---

### 组件规范

**按钮：**
- 最小高度：48px（电脑）/ 56px（手机）
- 圆角：12-25px
- 阴影：0 4px 12px rgba(...)
- 过渡：all 0.2s ease

**卡片：**
- 圆角：16px
- 内边距：20px
- 阴影：0 4px 12px rgba(0,0,0,0.08)
- 背景：白色

---

## 📝 开发规范

### Python代码规范

**命名：**
```python
# 函数：小写+下划线
def upload_file():
    pass

# 变量：小写+下划线
upload_folder = './received_files'

# 常量：大写+下划线
MAX_FILE_SIZE = 100 * 1024 * 1024

# 类：大驼峰
class FileTransferAPI:
    pass
```

**注释：**
```python
def get_local_ip():
    """获取本机局域网IP地址"""
    # 创建UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ...
```

---

### JavaScript代码规范

**命名：**
```javascript
// 函数：小驼峰
function loadHistory() {}

// 变量：小驼峰
let autoRefreshInterval = null;

// 常量：全大写
const REFRESH_INTERVAL = 2000;

// 类：大驼峰
class FileTransferAPI {}
```

**异步处理：**
```javascript
// 优先使用 async/await
async function sendText() {
    try {
        const response = await fetch(...);
        const data = await response.json();
        // 处理数据
    } catch (error) {
        console.error('错误:', error);
    }
}
```

---

### CSS代码规范

**命名：**
```css
/* BEM命名法 */
.history-item { }
.history-item__info { }
.history-item--active { }
```

**属性顺序：**
```css
.element {
    /* 1. 定位 */
    position: absolute;
    top: 0;
    
    /* 2. 盒模型 */
    display: flex;
    width: 100%;
    padding: 20px;
    
    /* 3. 排版 */
    font-size: 16px;
    color: #333;
    
    /* 4. 视觉 */
    background: white;
    border-radius: 12px;
    
    /* 5. 其他 */
    transition: all 0.2s;
}
```

---

## 🔌 API扩展

### 添加新接口

**步骤1：定义路由**
```python
@app.route('/api/new-feature', methods=['GET'])
def new_feature():
    """新功能描述"""
    try:
        # 业务逻辑
        result = do_something()
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
```

**步骤2：前端调用**
```javascript
async function callNewFeature() {
    const response = await fetch('/api/new-feature');
    const data = await response.json();
    
    if (data.success) {
        // 处理数据
    }
}
```

---

### 修改现有接口

**示例：增加分页支持**

```python
@app.route('/api/history', methods=['GET'])
def get_history():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    history_data = transfer_history[start:end]
    
    return jsonify({
        'success': True,
        'history': history_data,
        'count': len(history_data),
        'total': len(transfer_history)
    })
```

---

## 🎨 UI扩展

### 添加新页面

**步骤1：创建路由**
```python
@app.route('/settings')
def settings():
    return render_template_string(settings_html())
```

**步骤2：定义HTML模板**
```python
def settings_html():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>设置</title>
    </head>
    <body>
        <h1>设置页面</h1>
    </body>
    </html>
    '''
```

---

### 修改主题色

**全局替换：**
```bash
# 查找所有渐变色定义
grep -r "#667eea" web_templates.py
grep -r "#764ba2" web_templates.py

# 替换为新颜色
sed -i 's/#667eea/#ff6b6b/g' web_templates.py
sed -i 's/#764ba2/#ee5a6f/g' web_templates.py
```

---

## 🧪 测试指南

### 单元测试

**安装pytest：**
```bash
pip install pytest
```

**编写测试：**
```python
# test_server.py
import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_history(client):
    response = client.get('/api/history')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True

def test_upload_text(client):
    response = client.post('/api/upload/text', 
                          json={'text': 'test'})
    assert response.status_code == 200
```

**运行测试：**
```bash
pytest test_server.py -v
```

---

### 手动测试清单

**基础功能：**
- [ ] 服务器启动
- [ ] 设备检测
- [ ] 文件上传
- [ ] 文本发送
- [ ] 自动刷新
- [ ] 图片预览
- [ ] 下载功能
- [ ] 删除功能

**性能测试：**
- [ ] CPU占用 <5%
- [ ] 内存稳定
- [ ] 响应时间 <200ms
- [ ] 无内存泄漏

---

## 📦 打包部署

### PyInstaller打包

**配置文件：** `FileTransferServer.spec`

```python
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(['server.py'],
             pathex=[],
             binaries=[],
             datas=[('web_templates.py', '.'),
                    ('received_files', 'received_files')],
             hiddenimports=['flask', 'flask_cors', 'qrcode', 'PIL'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FileTransferServer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon=None)
```

**打包命令：**
```bash
pyinstaller FileTransferServer.spec
```

---

### Docker部署（未来）

**Dockerfile：**
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "server.py"]
```

**构建和运行：**
```bash
docker build -t file-transfer .
docker run -p 5000:5000 file-transfer
```

---

## 🔐 安全建议

### 生产环境配置

**1. 使用WSGI服务器**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

**2. 启用HTTPS**
```python
# 使用Let's Encrypt证书
app.run(ssl_context=('cert.pem', 'key.pem'))
```

**3. 添加认证**
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == 'admin' and password == 'secret'

@app.route('/api/upload/file', methods=['POST'])
@auth.login_required
def upload_file():
    ...
```

**4. 限制访问IP**
```python
from flask import abort

@app.before_request
def restrict_ip():
    allowed_ips = ['192.168.0.100', '192.168.0.101']
    if request.remote_addr not in allowed_ips:
        abort(403)
```

---

## 📊 性能优化

### 后端优化

**1. 启用缓存**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/history')
@cache.cached(timeout=1)
def get_history():
    ...
```

**2. 异步文件操作**
```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

def save_file_async(file, filepath):
    executor.submit(file.save, filepath)
```

---

### 前端优化

**1. 减少DOM操作**
```javascript
// ❌ 低效
history.forEach(item => {
    const div = document.createElement('div');
    historyList.appendChild(div);
});

// ✅ 高效
let html = '';
history.forEach(item => {
    html += generateHTML(item);
});
historyList.innerHTML = html;
```

**2. 防抖处理**
```javascript
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

const debouncedSearch = debounce(search, 300);
```

---

## 🚀 发布流程

### 版本管理

**版本号规范：** `v主版本.次版本.修订版本`

**示例：**
- v2.4.0 - 新增自动刷新功能
- v2.3.1 - 修复UI bug
- v2.3.0 - 新增双端UI

---

### 发布检查清单

**代码：**
- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 文档已更新

**打包：**
- [ ] 重新生成exe
- [ ] 测试便携版
- [ ] 验证文件大小

**文档：**
- [ ] 更新CHANGELOG
- [ ] 更新README
- [ ] 更新API文档

**发布：**
- [ ] 创建Git tag
- [ ] 上传到GitHub
- [ ] 发布公告

---

## 📞 贡献指南

### 提交PR

**分支命名：**
```
feature/新功能名称
bugfix/问题描述
hotfix/紧急修复
```

**Commit规范：**
```
feat: 添加自动刷新功能
fix: 修复图片预览bug
docs: 更新API文档
style: 代码格式化
refactor: 重构设备检测逻辑
test: 添加单元测试
```

---

<div align="center">

**Happy Coding!** 💻✨

</div>

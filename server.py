from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
import socket
import datetime
import qrcode
import io
import base64
import webbrowser
import threading
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = './received_files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'zip', 'rar', 'mp4', 'mp3', 'avi', 'mov'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 存储接收的记录
transfer_history = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def generate_qr_code(url):
    """生成二维码图片（base64编码）"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    """主页 - 美观的Web上传界面（单页应用）"""
    local_ip = get_local_ip()
    port = request.host.split(':')[-1] if ':' in request.host else '5000'
    server_url = f"http://{local_ip}:{port}"
    qr_code = generate_qr_code(server_url)
    
    html_template = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>局域网文件传输</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 1400px;
            width: 100%;
            padding: 30px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        /* 响应式：小屏幕垂直布局 */
        @media (max-width: 1024px) {
            .container {
                grid-template-columns: 1fr;
                max-width: 900px;
            }
        }
        
        .header {
            text-align: center;
            margin-bottom: 20px;
            grid-column: 1 / -1;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .left-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .right-panel {
            display: flex;
            flex-direction: column;
            gap: 20px;
            max-height: calc(100vh - 200px);
            overflow-y: auto;
        }
        
        /* 自定义滚动条 */
        .right-panel::-webkit-scrollbar {
            width: 8px;
        }
        
        .right-panel::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        .right-panel::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 10px;
        }
        
        .right-panel::-webkit-scrollbar-thumb:hover {
            background: #764ba2;
        }
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
        }
        
        .qr-code {
            width: 200px;
            height: 200px;
            margin: 15px auto;
            border: 3px solid #667eea;
            border-radius: 10px;
            padding: 10px;
            background: white;
        }
        
        .server-info {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        
        .server-info code {
            font-size: 1.1em;
            color: #1976d2;
            font-weight: bold;
        }
        
        .upload-zone {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 60px 20px;
            text-align: center;
            background: #f8f9ff;
            transition: all 0.3s ease;
            cursor: pointer;
            margin: 30px 0;
        }
        
        .upload-zone:hover {
            background: #eef0ff;
            border-color: #764ba2;
            transform: translateY(-2px);
        }
        
        .upload-zone.dragover {
            background: #e0e4ff;
            border-color: #764ba2;
        }
        
        .upload-icon {
            font-size: 4em;
            margin-bottom: 15px;
        }
        
        .upload-text {
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .upload-hint {
            color: #999;
            font-size: 0.9em;
        }
        
        .file-input {
            display: none;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .text-upload {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
        }
        
        .text-upload textarea {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1em;
            resize: vertical;
            font-family: inherit;
        }
        
        .text-upload textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .history {
            margin-top: 30px;
        }
        
        .history h2 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .history-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .history-header h2 {
            color: #667eea;
            margin: 0;
        }
        
        .btn-clear {
            background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        
        .btn-clear:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(245, 101, 101, 0.4);
        }
        
        .history-item {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 10px;
            margin: 8px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .history-item:hover {
            background: #eef0ff;
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        }
        
        .history-item .info {
            flex: 1;
        }
        
        .history-item .type {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            margin-right: 10px;
        }
        
        .type-file { background: #e3f2fd; color: #1976d2; }
        .type-text { background: #f3e5f5; color: #7b1fa2; }
        .type-image { background: #e8f5e9; color: #388e3c; }
        
        .history-item .time {
            color: #999;
            font-size: 0.85em;
        }
        
        .download-link {
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }
        
        .download-link:hover {
            text-decoration: underline;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
            display: none;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .status-message {
            padding: 12px;
            border-radius: 8px;
            margin: 10px 0;
            display: none;
        }
        
        .status-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        /* Toast 提示 */
        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 14px;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }
        
        .toast.show {
            opacity: 1;
        }
        
        /* 图片预览模态框 */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            max-width: 90%;
            max-height: 90%;
            position: relative;
        }
        
        .modal-img {
            max-width: 100%;
            max-height: 90vh;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
        
        .modal-close {
            position: absolute;
            top: -40px;
            right: 0;
            color: white;
            font-size: 32px;
            cursor: pointer;
            background: none;
            border: none;
            padding: 5px;
        }
        
        .thumbnail {
            width: 50px;
            height: 50px;
            object-fit: cover;
            border-radius: 8px;
            margin-right: 10px;
            cursor: pointer;
            border: 2px solid #667eea;
            transition: transform 0.2s;
            flex-shrink: 0;
        }
        
        .thumbnail:hover {
            transform: scale(1.1);
        }
        
        .action-buttons {
            display: flex;
            gap: 6px;
            margin-left: 8px;
            flex-shrink: 0;
        }
        
        .btn-delete {
            background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
            color: white;
        }
        
        .btn-delete:hover {
            transform: translateY(-2px);
            box-shadow: 0 3px 10px rgba(245, 101, 101, 0.4);
        }
        
        .btn-small {
            padding: 6px 12px;
            font-size: 12px;
            border-radius: 15px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: bold;
        }
        
        .btn-copy {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-copy:hover {
            transform: translateY(-2px);
            box-shadow: 0 3px 10px rgba(102, 126, 234, 0.4);
        }
        
        .btn-download {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }
        
        .btn-download:hover {
            transform: translateY(-2px);
            box-shadow: 0 3px 10px rgba(72, 187, 120, 0.4);
        }
        
        .text-content {
            background: white;
            padding: 10px;
            border-radius: 8px;
            margin-top: 8px;
            font-size: 14px;
            color: #333;
            max-height: 100px;
            overflow-y: auto;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 局域网文件传输</h1>
            <p>快速在手机和电脑之间传输文件、图片和文本</p>
        </div>
        
        <!-- 左侧面板 -->
        <div class="left-panel">
            <div class="qr-section">
                <h3>手机扫描二维码连接</h3>
                <img src="{{ qr_code }}" alt="QR Code" class="qr-code">
                <p style="color: #666; margin-top: 10px;">或手动访问下方地址</p>
            </div>
            
            <div class="server-info">
                <p>服务器地址：</p>
                <code>{{ server_url }} (本机地址)</code>
            </div>
            
            <div class="upload-zone" id="uploadZone">
                <div class="upload-icon">📁</div>
                <div class="upload-text">拖拽文件到此处或点击选择</div>
                <div class="upload-hint">支持图片、文档、视频等格式（最大100MB）</div>
                <input type="file" id="fileInput" class="file-input" multiple>
            </div>
            
            <div class="progress-bar" id="progressBar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            
            <div class="status-message" id="statusMessage"></div>
        </div>
        
        <!-- 右侧面板 -->
        <div class="right-panel">
            <div class="text-upload">
                <h3 style="margin-bottom: 15px; color: #667eea;">📝 发送文本</h3>
                <textarea id="textInput" placeholder="输入要发送的文本或链接..."></textarea>
                <div style="margin-top: 15px; text-align: center;">
                    <button class="btn" onclick="sendText()">发送文本</button>
                    <button class="btn" onclick="pasteFromClipboard()" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">📋 粘贴</button>
                </div>
            </div>
            
            <div class="history">
                <div class="history-header">
                    <h2>📋 传输历史</h2>
                    <button class="btn-clear" onclick="clearAllHistory()">🗑️ 清空全部</button>
                </div>
                <div id="historyList">
                {% for item in history %}
                <div class="history-item" data-type="{{ item.type }}" data-filename="{{ item.filename }}">
                    {% if item.type == 'image' %}
                    <img src="/api/download/{{ item.filename }}" class="thumbnail" onclick="previewImage('{{ item.filename | replace("'", "\\'") }}')" alt="预览">
                    {% endif %}
                    <div class="info">
                        <span class="type type-{{ item.type }}">{{ item.type_name }}</span>
                        <strong>{{ item.name }}</strong>
                        <div class="time">{{ item.time }}</div>
                        {% if item.type == 'text' and item.content %}
                        <div class="text-content">{{ item.content }}</div>
                        {% endif %}
                    </div>
                    <div class="action-buttons">
                        {% if item.type == 'text' %}
                        <button class="btn-small btn-copy" onclick="copyText(event, '{{ item.content | replace("'", "\\'") | replace('"', '\\"') }}')">📋 复制</button>
                        {% endif %}
                        {% if item.type == 'file' or item.type == 'image' %}
                        <a href="/api/download/{{ item.filename }}" class="btn-small btn-download" download="{{ item.name }}">⬇️ 下载</a>
                        {% endif %}
                        <button class="btn-small btn-delete" onclick="deleteItem(event, '{{ item.filename }}')">🗑️</button>
                    </div>
                </div>
                {% endfor %}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Toast 提示 -->
    <div id="toast" class="toast"></div>
    
    <!-- 图片预览模态框 -->
    <div id="imageModal" class="modal" onclick="closeModal()">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <img id="modalImg" class="modal-img" src="" alt="预览">
        </div>
    </div>
    
    <script>
        const uploadZone = document.getElementById('uploadZone');
        const fileInput = document.getElementById('fileInput');
        const progressBar = document.getElementById('progressBar');
        const progressFill = document.getElementById('progressFill');
        const statusMessage = document.getElementById('statusMessage');
        
        // 点击上传区域
        uploadZone.addEventListener('click', () => fileInput.click());
        
        // 文件选择
        fileInput.addEventListener('change', handleFiles);
        
        // 拖拽事件
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });
        
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });
        
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            uploadFiles(files);
        });
        
        function handleFiles(e) {
            const files = e.target.files;
            uploadFiles(files);
        }
        
        async function uploadFiles(files) {
            if (files.length === 0) return;
            
            showStatus('正在上传...', 'success');
            progressBar.style.display = 'block';
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/api/upload/file', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        updateProgress((i + 1) / files.length * 100);
                        showStatus(`✅ ${file.name} 上传成功！`, 'success');
                    } else {
                        showStatus(`❌ ${file.name} 上传失败：${result.message}`, 'error');
                    }
                } catch (error) {
                    showStatus(`❌ ${file.name} 上传错误：${error.message}`, 'error');
                }
            }
            
            setTimeout(() => {
                progressBar.style.display = 'none';
                location.reload();
            }, 1500);
        }
        
        async function sendText() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) {
                showStatus('请输入文本内容', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/upload/text', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showStatus('✅ 文本发送成功！', 'success');
                    document.getElementById('textInput').value = '';
                    setTimeout(() => location.reload(), 1000);
                } else {
                    showStatus('❌ 发送失败：' + result.message, 'error');
                }
            } catch (error) {
                showStatus('❌ 发送错误：' + error.message, 'error');
            }
        }
        
        async function pasteFromClipboard() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById('textInput').value = text;
                showStatus('✅ 已粘贴剪贴板内容', 'success');
            } catch (error) {
                showStatus('❌ 无法访问剪贴板', 'error');
            }
        }
        
        function updateProgress(percent) {
            progressFill.style.width = percent + '%';
        }
        
        function showStatus(message, type) {
            statusMessage.textContent = message;
            statusMessage.className = 'status-message status-' + type;
            statusMessage.style.display = 'block';
            
            setTimeout(() => {
                statusMessage.style.display = 'none';
            }, 3000);
        }
        
        // Toast 提示函数
        function showToast(message, duration = 2000) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            
            setTimeout(() => {
                toast.classList.remove('show');
            }, duration);
        }
        
        // 复制文本到剪贴板
        async function copyText(event, text) {
            event.stopPropagation();
            try {
                await navigator.clipboard.writeText(text);
                showToast('✅ 已复制到剪贴板！');
            } catch (error) {
                // 降级方案：使用传统方法
                const textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                showToast('✅ 已复制到剪贴板！');
            }
        }
        
        // 图片预览
        function previewImage(filename) {
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImg');
            modalImg.src = '/api/download/' + filename;
            modal.classList.add('active');
        }
        
        // 关闭模态框
        function closeModal() {
            const modal = document.getElementById('imageModal');
            modal.classList.remove('active');
        }
        
        // ESC键关闭模态框
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
        
        // 删除单个历史记录
        async function deleteItem(event, filename) {
            event.stopPropagation();
            
            if (!confirm('确定要删除这条记录吗？')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/history/delete/${filename}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showToast('✅ 已删除');
                    // 从DOM中移除该元素
                    const item = event.target.closest('.history-item');
                    if (item) {
                        item.style.transition = 'all 0.3s ease';
                        item.style.opacity = '0';
                        item.style.transform = 'translateX(-100%)';
                        setTimeout(() => item.remove(), 300);
                    }
                } else {
                    showToast('❌ 删除失败: ' + result.message);
                }
            } catch (error) {
                showToast('❌ 删除错误: ' + error.message);
            }
        }
        
        // 清空所有历史记录
        async function clearAllHistory() {
            if (!confirm('确定要清空所有历史记录吗？此操作不可恢复！')) {
                return;
            }
            
            try {
                const response = await fetch('/api/history/clear', {
                    method: 'POST'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showToast('✅ 已清空所有记录');
                    // 清空历史列表DOM
                    const historyList = document.getElementById('historyList');
                    historyList.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">暂无历史记录</p>';
                } else {
                    showToast('❌ 清空失败: ' + result.message);
                }
            } catch (error) {
                showToast('❌ 清空错误: ' + error.message);
            }
        }
        
        // 动态加载历史记录（无需刷新页面）
        async function loadHistory() {
            try {
                const response = await fetch('/api/files');
                const data = await response.json();
                
                if (data.success) {
                    // 这里可以动态更新历史列表，但为了简化，我们保留服务端渲染
                    console.log('历史记录已更新');
                }
            } catch (error) {
                console.error('加载历史记录失败:', error);
            }
        }
        
        // 页面加载完成后自动刷新历史记录（每30秒）
        setInterval(loadHistory, 30000);
    </script>
</body>
</html>
    '''
    
    return render_template_string(html_template, 
                                qr_code=qr_code, 
                                server_url=server_url,
                                history=transfer_history[-20:])  # 显示最近20条记录

@app.route('/api/upload/file', methods=['POST'])
def upload_file():
    """接收文件上传"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': '文件名为空'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': '不支持的文件类型'}), 400
    
    filename = secure_filename(file.filename)
    # 添加时间戳避免重名
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_')
    filename = timestamp + filename
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # 记录历史
    file_type = 'image' if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg')) else 'file'
    transfer_history.append({
        'type': file_type,
        'type_name': '🖼️ 图片' if file_type == 'image' else '📁 文件',
        'name': file.filename if file.filename else filename,  # 保留原始文件名用于显示
        'filename': filename,  # 实际保存的文件名
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'size': os.path.getsize(filepath)
    })
    
    return jsonify({'success': True, 'filename': filename})

@app.route('/api/upload/text', methods=['POST'])
def upload_text():
    """接收文本内容"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'success': False, 'message': '没有文本内容'}), 400
    
    text = data['text']
    
    # 检测是否为链接
    is_link = text.startswith(('http://', 'https://', 'www.'))
    
    # 保存文本到文件
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"text_{timestamp}.txt"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # 记录历史
    transfer_history.append({
        'type': 'text',
        'type_name': '链接' if is_link else '文本',
        'name': text[:50] + '...' if len(text) > 50 else text,
        'filename': filename,
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'content': text,
        'is_link': is_link
    })
    
    return jsonify({'success': True})

@app.route('/api/download/<filename>')
def download_file(filename):
    """下载文件（支持预览和下载）"""
    from flask import send_file
    import mimetypes
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'message': '文件不存在'}), 404
    
    # 自动检测MIME类型
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    # 判断是否为图片格式
    is_image = filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))
    
    if is_image:
        # 图片文件：允许浏览器预览（inline）
        return send_file(
            filepath,
            mimetype=mime_type,
            as_attachment=False,
            download_name=filename
        )
    else:
        # 其他文件：强制下载（attachment）
        return send_file(
            filepath,
            mimetype=mime_type,
            as_attachment=True,
            download_name=filename
        )

@app.route('/api/files', methods=['GET'])
def list_files():
    """列出所有接收的文件"""
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filepath):
            files.append({
                'filename': filename,
                'size': os.path.getsize(filepath),
                'created': datetime.datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return jsonify({'success': True, 'files': files})

@app.route('/api/history/delete/<filename>', methods=['DELETE'])
def delete_history_item(filename):
    """删除单个历史记录及对应文件"""
    try:
        # 查找并删除历史记录
        global transfer_history
        original_count = len(transfer_history)
        transfer_history = [item for item in transfer_history if item.get('filename') != filename]
        
        # 删除实际文件
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        deleted_count = original_count - len(transfer_history)
        
        if deleted_count > 0:
            return jsonify({'success': True, 'message': f'已删除 {deleted_count} 条记录'})
        else:
            return jsonify({'success': False, 'message': '记录不存在'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/history/clear', methods=['POST'])
def clear_all_history():
    """清空所有历史记录和文件"""
    try:
        global transfer_history
        
        # 删除所有文件
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
        
        # 清空历史记录
        cleared_count = len(transfer_history)
        transfer_history = []
        
        return jsonify({'success': True, 'message': f'已清空 {cleared_count} 条记录'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/devices', methods=['GET'])
def device_info():
    """返回服务器信息"""
    local_ip = get_local_ip()
    return jsonify({
        'success': True,
        'ip': local_ip,
        'port': 5000,
        'url': f'http://{local_ip}:5000',
        'device_name': 'Windows PC',
        'status': 'online'
    })

if __name__ == '__main__':
    local_ip = get_local_ip()
    server_url = f"http://{local_ip}:5000"
    
    print("=" * 60)
    print("🚀 局域网文件传输服务器启动成功！")
    print("=" * 60)
    print(f"📍 服务器地址: {server_url}")
    print(f"📱 手机浏览器访问上述地址即可上传文件")
    print(f"📁 文件保存目录: {os.path.abspath(UPLOAD_FOLDER)}")
    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    # 延迟2秒后自动打开浏览器（给服务器启动时间）
    def open_browser():
        import time
        time.sleep(2)
        webbrowser.open(server_url)
    
    # 在新线程中打开浏览器，避免阻塞服务器启动
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=False)

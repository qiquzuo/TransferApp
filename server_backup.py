from flask import Flask, request, jsonify, send_from_directory, render_template_string, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import socket
import datetime
import qrcode
import io
import base64
import webbrowser
import threading
import hashlib
import re
from werkzeug.utils import secure_filename
from web_templates import get_desktop_html_template, get_mobile_html_template

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 安全配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'transfer-app-secret-key-2026')

# 速率限制器
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# 身份认证配置
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH', 
    hashlib.sha256('admin123'.encode()).hexdigest())  # 默认密码: admin123

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

def verify_password(password):
    """验证密码"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == ADMIN_PASSWORD_HASH

def require_auth(f):
    """身份认证装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        # 检查session中是否已认证
        if not session.get('authenticated'):
            # 检查请求中的token
            token = request.headers.get('X-Auth-Token') or request.args.get('token')
            if token and verify_password(token):
                session['authenticated'] = True
            else:
                return jsonify({'error': 'Unauthorized', 'message': '需要身份认证'}), 401
        return f(*args, **kwargs)
    return decorated

def validate_file_magic_number(filepath, allowed_mimes):
    """验证文件真实类型（基于Magic Number）"""
    try:
        import magic
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(filepath)
        
        if file_type not in allowed_mimes:
            return False, file_type
        return True, file_type
    except Exception as e:
        print(f"⚠️ 文件类型验证失败: {e}")
        return True, "unknown"  # 如果验证失败，暂时允许通过

def sanitize_svg(filepath):
    """清理SVG中的恶意脚本，防止XSS攻击"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 移除script标签
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 移除恶意事件处理器 (onload, onclick, onerror等)
        content = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\s+on\w+\s*=\s*[^\s>]+', '', content, flags=re.IGNORECASE)
        
        # 移除javascript:协议
        content = re.sub(r'javascript\s*:', '', content, flags=re.IGNORECASE)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ SVG文件已清理恶意脚本")
        
        return True
    except Exception as e:
        print(f"⚠️ SVG清理失败: {e}")
        return False

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
    """主页 - 根据设备类型显示不同UI（电脑端左右分栏，手机端垂直流式）"""
    # 如果未认证，显示登录页面
    if not session.get('authenticated'):
        return render_login_page()
    
    local_ip = get_local_ip()
    port = request.host.split(':')[-1] if ':' in request.host else '5000'
    
    # 检测是否使用HTTPS
    if request.is_secure or request.headers.get('X-Forwarded-Proto') == 'https':
        protocol = 'https'
    else:
        protocol = 'http'
    
    server_url = f"{protocol}://{local_ip}:{port}"
    qr_code = generate_qr_code(server_url)
    
    # 检测设备类型
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(keyword in user_agent for keyword in ['mobile', 'android', 'iphone', 'ipad'])
    
    if is_mobile:
        # 手机端UI - 垂直流式布局
        html_template = get_mobile_html_template()
    else:
        # 电脑端UI - 左右分栏布局
        html_template = get_desktop_html_template()
    
    return render_template_string(html_template, 
                                qr_code=qr_code, 
                                server_url=server_url,
                                history=transfer_history[-20:])  # 显示最近20条记录

def render_login_page():
    """渲染登录页面"""
    login_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文件传输 - 登录</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 90%;
            max-width: 400px;
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
        }
        p {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #333;
            margin-bottom: 8px;
            font-weight: 500;
        }
        input[type="password"] {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        .error {
            color: #f56565;
            text-align: center;
            margin-top: 15px;
            display: none;
        }
        .hint {
            color: #999;
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🔐 文件传输</h1>
        <p>请输入访问密码</p>
        <form id="loginForm">
            <div class="input-group">
                <label for="password">密码</label>
                <input type="password" id="password" placeholder="输入密码..." required autofocus>
            </div>
            <button type="submit">登录</button>
            <div class="error" id="errorMsg">❌ 密码错误，请重试</div>
        </form>
        <div class="hint">默认密码: admin123<br>建议修改环境变量 ADMIN_PASSWORD_HASH</div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const password = document.getElementById('password').value;
            const errorMsg = document.getElementById('errorMsg');
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    window.location.reload();
                } else {
                    errorMsg.style.display = 'block';
                    document.getElementById('password').value = '';
                }
            } catch (error) {
                errorMsg.textContent = '❌ 网络错误，请重试';
                errorMsg.style.display = 'block';
            }
        });
    </script>
</body>
</html>
    '''
    return render_template_string(login_html)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")  # 防止暴力破解
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data or 'password' not in data:
        return jsonify({'success': False, 'message': '缺少密码'}), 400
    
    password = data['password']
    
    if verify_password(password):
        session['authenticated'] = True
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '密码错误'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.pop('authenticated', None)
    return jsonify({'success': True, 'message': '已登出'})

@app.route('/api/upload/file', methods=['POST'])
@require_auth  # 需要身份认证
@limiter.limit("10 per minute")  # 速率限制：每分钟最多10次上传
def upload_file():
    """接收文件上传"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': '文件名为空'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': '不支持的文件类型'}), 400
    
    # 保留原始文件名
    original_filename = secure_filename(file.filename)
    
    # 添加时间戳避免重名（服务器端存储）
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_')
    stored_filename = timestamp + original_filename
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
    file.save(filepath)
    
    # 安全增强1：验证文件真实类型（Magic Number）
    allowed_mimes = {
        'image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp', 'image/svg+xml',
        'application/pdf',
        'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/plain',
        'application/zip', 'application/x-rar-compressed',
        'video/mp4', 'audio/mpeg', 'video/x-msvideo', 'video/quicktime'
    }
    
    is_valid, detected_mime = validate_file_magic_number(filepath, allowed_mimes)
    if not is_valid:
        os.remove(filepath)  # 删除非法文件
        return jsonify({
            'success': False, 
            'message': f'文件类型不匹配：扩展名为.{original_filename.rsplit(".", 1)[-1]}，但实际类型为{detected_mime}'
        }), 400
    
    # 安全增强2：SVG文件清理（防止XSS）
    if stored_filename.lower().endswith('.svg'):
        if not sanitize_svg(filepath):
            os.remove(filepath)
            return jsonify({'success': False, 'message': 'SVG文件安全检查失败'}), 400
    
    # 记录历史
    file_type = 'image' if stored_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg')) else 'file'
    transfer_history.append({
        'type': file_type,
        'type_name': '🖼️ 图片' if file_type == 'image' else '📁 文件',
        'name': original_filename,  # 显示原始文件名
        'filename': stored_filename,  # 服务器存储的文件名
        'original_filename': original_filename,  # 原始文件名（用于下载）
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'size': os.path.getsize(filepath)
    })
    
    return jsonify({
        'success': True, 
        'filename': stored_filename,
        'original_filename': original_filename
    })

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
    
    # 查找原始文件名
    original_filename = filename
    for item in transfer_history:
        if item.get('filename') == filename:
            original_filename = item.get('original_filename', filename)
            break
    
    # 自动检测MIME类型
    mime_type, _ = mimetypes.guess_type(original_filename)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    # 判断是否为图片格式
    is_image = original_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))
    
    if is_image:
        # 图片文件：允许浏览器预览（inline）
        return send_file(
            filepath,
            mimetype=mime_type,
            as_attachment=False,
            download_name=original_filename
        )
    else:
        # 其他文件：强制下载（attachment）
        return send_file(
            filepath,
            mimetype=mime_type,
            as_attachment=True,
            download_name=original_filename
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
@require_auth  # 需要身份认证
@limiter.limit("20 per minute")  # 速率限制
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
@require_auth  # 需要身份认证
@limiter.limit("5 per minute")  # 速率限制（更严格）
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

@app.route('/api/history', methods=['GET'])
def get_history():
    """获取传输历史记录（用于AJAX自动刷新）"""
    try:
        # 返回最近20条记录
        history_data = []
        for item in transfer_history[-20:]:
            history_data.append({
                'type': item.get('type', 'file'),
                'type_name': item.get('type_name', '文件'),
                'name': item.get('name', ''),  # 原始文件名（显示用）
                'filename': item.get('filename', ''),  # 服务器存储的文件名
                'original_filename': item.get('original_filename', item.get('name', '')),  # 原始文件名（下载用）
                'time': item.get('time', ''),
                'content': item.get('content', ''),
                'is_link': item.get('is_link', False)
            })
        
        return jsonify({
            'success': True,
            'history': history_data,
            'count': len(history_data)
        })
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
    
    # 检查证书文件
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        # 使用HTTPS
        protocol = 'https'
        ssl_context = (cert_file, key_file)
        use_https = True
    else:
        # 降级到HTTP（警告）
        protocol = 'http'
        ssl_context = None
        use_https = False
    
    server_url = f"{protocol}://{local_ip}:5000"
    
    print("=" * 60)
    if use_https:
        print("🚀 局域网文件传输服务器启动成功！（HTTPS加密）")
        print("🔒 连接已加密，数据传输安全")
    else:
        print("⚠️  警告：未找到SSL证书，使用HTTP（不安全）")
        print("💡 建议运行 python generate_cert.py 生成证书以启用HTTPS")
    print("=" * 60)
    print(f"📍 服务器地址: {server_url}")
    print(f"🔐 默认密码: admin123")
    print(f"📱 手机浏览器访问上述地址即可上传文件")
    print(f"📁 文件保存目录: {os.path.abspath(UPLOAD_FOLDER)}")
    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    # 延迟2秒后自动打开浏览器
    def open_browser():
        import time
        time.sleep(1)
        webbrowser.open(server_url)
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # 启动服务器（支持HTTPS）
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=False,
        ssl_context=ssl_context  # SSL配置
    )

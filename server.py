"""
局域网文件传输服务器 - 简化版（无密码、无HTTPS）
"""
from flask import Flask, request, jsonify, send_file, render_template_string
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
import re
from werkzeug.utils import secure_filename
from web_templates import get_desktop_html_template, get_mobile_html_template

# ==================== 应用初始化 ====================
app = Flask(__name__)
CORS(app)

# 速率限制器
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],  # 1秒刷新，正常限制
    storage_uri="memory://"
)

# ==================== 配置 ====================
UPLOAD_FOLDER = './received_files'
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg',
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt',
    'zip', 'rar', 'mp4', 'mp3', 'avi', 'mov'
}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 历史记录
transfer_history = []

# ==================== 工具函数 ====================

def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_local_ip() -> str:
    """获取本机局域网IP地址"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except Exception:
        return '127.0.0.1'


def generate_qr_code(url: str) -> str:
    """生成二维码图片（base64编码）"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


def sanitize_svg(filepath: str) -> bool:
    """清理SVG中的恶意脚本，防止XSS攻击"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 移除script标签
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # 移除恶意事件处理器
        content = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\s+on\w+\s*=\s*[^\s>]+', '', content, flags=re.IGNORECASE)
        
        # 移除javascript:协议
        content = re.sub(r'javascript\s*:', '', content, flags=re.IGNORECASE)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ SVG文件已清理恶意脚本")
        
        return True
    except Exception as e:
        print(f"⚠️ SVG清理失败: {e}")
        return False


# ==================== 路由 ====================

@app.route('/')
def index():
    """主页 - 根据设备类型显示不同UI"""
    local_ip = get_local_ip()
    port = request.host.split(':')[-1] if ':' in request.host else '5000'
    server_url = f"http://{local_ip}:{port}"
    qr_code = generate_qr_code(server_url)
    
    # 检测设备类型
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(keyword in user_agent for keyword in ['mobile', 'android', 'iphone', 'ipad'])
    
    if is_mobile:
        html_template = get_mobile_html_template()
    else:
        html_template = get_desktop_html_template()
    
    return render_template_string(
        html_template, 
        qr_code=qr_code, 
        server_url=server_url,
        history=transfer_history[-20:]
    )


@app.route('/api/upload/file', methods=['POST'])
@limiter.limit("10 per minute")
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
    
    # 添加时间戳避免重名
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_')
    stored_filename = timestamp + original_filename
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
    file.save(filepath)
    
    # SVG安全检查
    if stored_filename.lower().endswith('.svg'):
        if not sanitize_svg(filepath):
            os.remove(filepath)
            return jsonify({'success': False, 'message': 'SVG文件安全检查失败'}), 400
    
    # 记录历史
    file_type = 'image' if stored_filename.lower().endswith(
        ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg')
    ) else 'file'
    
    transfer_history.append({
        'type': file_type,
        'type_name': '🖼️ 图片' if file_type == 'image' else '📁 文件',
        'name': original_filename,
        'filename': stored_filename,
        'original_filename': original_filename,
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'size': os.path.getsize(filepath)
    })
    
    return jsonify({
        'success': True, 
        'filename': stored_filename,
        'original_filename': original_filename
    })


@app.route('/api/upload/text', methods=['POST'])
@limiter.limit("20 per minute")
def upload_text():
    """接收文本内容"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'success': False, 'message': '没有文本内容'}), 400
    
    text = data['text']
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
    import mimetypes
    mime_type, _ = mimetypes.guess_type(original_filename)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    # 判断是否为图片格式
    is_image = original_filename.lower().endswith(
        ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg')
    )
    
    if is_image:
        # 图片文件：允许浏览器预览（inline）
        response = send_file(
            filepath,
            mimetype=mime_type,
            as_attachment=False
        )
        # 设置缓存控制，提高预览性能
        response.headers['Cache-Control'] = 'public, max-age=3600'
        return response
    else:
        # 其他文件：强制下载（attachment）
        return send_file(
            filepath,
            mimetype=mime_type,
            as_attachment=True,
            download_name=original_filename
        )


@app.route('/api/history', methods=['GET'])
@limiter.limit("100 per minute")  # 1秒刷新，每分钟60次，留有余量
def get_history():
    """获取传输历史记录（用于AJAX自动刷新）"""
    try:
        history_data = []
        for item in transfer_history[-20:]:
            history_data.append({
                'type': item.get('type', 'file'),
                'type_name': item.get('type_name', '文件'),
                'name': item.get('name', ''),
                'filename': item.get('filename', ''),
                'original_filename': item.get('original_filename', item.get('name', '')),
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


@app.route('/api/history/delete/<filename>', methods=['DELETE'])
@limiter.limit("20 per minute")
def delete_history_item(filename):
    """删除单个历史记录及对应文件"""
    try:
        global transfer_history
        original_count = len(transfer_history)
        transfer_history = [
            item for item in transfer_history 
            if item.get('filename') != filename
        ]
        
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
@limiter.limit("5 per minute")
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
                'created': datetime.datetime.fromtimestamp(
                    os.path.getctime(filepath)
                ).strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return jsonify({'success': True, 'files': files})


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


# ==================== 启动服务器 ====================

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
    
    # 延迟1秒后自动打开浏览器
    def open_browser():
        import time
        time.sleep(1)
        webbrowser.open(server_url)
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # 启动服务器（HTTP，无SSL）
    app.run(host='0.0.0.0', port=5000, debug=False)

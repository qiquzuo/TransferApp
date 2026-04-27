"""
Web界面HTML模板 - 分为电脑端和手机端两套独立UI
"""

def get_desktop_html_template():
    """电脑端UI - 左右分栏布局"""
    return '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>局域网文件传输 - 电脑版</title>
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
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2), 0 0 0 1px rgba(255,255,255,0.1);
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
            padding: 24px 30px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        
        @media (max-width: 1024px) {
            .container {
                grid-template-columns: 1fr;
                max-width: 900px;
            }
        }
        
        .header {
            text-align: center;
            margin-bottom: 16px;
            grid-column: 1 / -1;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2em;
            margin-bottom: 6px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        .header .server-url {
            color: #999;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
            background: rgba(102, 126, 234, 0.08);
            padding: 4px 12px;
            border-radius: 12px;
            display: inline-block;
            margin-top: 4px;
        }
        
        .header p {
            color: #666;
            font-size: 0.95em;
            margin-top: 8px;
        }
        
        .left-panel {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .right-panel {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .qr-section {
            text-align: center;
            padding: 16px;
            background: rgba(248, 249, 250, 0.6);
            backdrop-filter: blur(5px);
            border-radius: 16px;
            border: 1px solid rgba(102, 126, 234, 0.1);
        }
        
        .qr-section h3 {
            font-size: 0.95em;
            color: #667eea;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        .qr-code {
            width: 150px;
            height: 150px;
            margin: 0 auto;
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            padding: 8px;
            background: white;
            transition: all 0.3s ease;
        }
        
        .qr-code:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        

        
        .upload-zone {
            border: 2px dashed rgba(102, 126, 234, 0.4);
            border-radius: 16px;
            padding: 40px 20px;
            text-align: center;
            background: rgba(248, 249, 255, 0.5);
            backdrop-filter: blur(5px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        
        .upload-zone:hover {
            background: rgba(238, 240, 255, 0.7);
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
        }
        
        .upload-zone:active {
            transform: translateY(0);
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 20px;
            font-size: 0.95em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin: 8px 4px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .history-item {
            background: rgba(248, 249, 250, 0.8);
            backdrop-filter: blur(5px);
            padding: 12px 14px;
            border-radius: 12px;
            margin: 6px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }
        
        .history-item:hover {
            background: rgba(238, 240, 255, 0.9);
            transform: translateX(4px);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
        }
        
        .thumbnail {
            width: 48px;
            height: 48px;
            object-fit: cover;
            border-radius: 10px;
            margin-right: 10px;
            cursor: pointer;
            border: 2px solid rgba(102, 126, 234, 0.3);
            transition: all 0.2s ease;
        }
        
        .thumbnail:hover {
            transform: scale(1.1);
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .btn-small {
            padding: 6px 12px;
            font-size: 12px;
            border-radius: 15px;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        
        .btn-copy {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-download {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            color: white;
        }
        
        .btn-delete {
            background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
            color: white;
        }
        
        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            color: white;
            padding: 12px 24px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            z-index: 1000;
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        
        .toast.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💻 局域网文件传输</h1>
            <div class="server-url">{{ server_url }}</div>
            <p>快速在手机和电脑之间传输文件、图片和文本</p>
        </div>
        
        <div class="left-panel">
            <div class="qr-section">
                <h3>📱 手机扫描连接</h3>
                <img src="{{ qr_code }}" alt="QR Code" class="qr-code">
            </div>
            
            <div class="upload-zone" id="uploadZone">
                <div style="font-size: 3em; margin-bottom: 12px;">📁</div>
                <div style="font-size: 1.1em; color: #667eea; font-weight: 500;">拖拽文件到此处或点击选择</div>
                <input type="file" id="fileInput" style="display: none;" multiple>
            </div>
        </div>
        
        <div class="right-panel">
            <div style="padding: 16px; background: rgba(248, 249, 250, 0.6); backdrop-filter: blur(5px); border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.1);">
                <h3 style="margin-bottom: 12px; color: #667eea; font-size: 1em; font-weight: 600;">📝 发送文本</h3>
                <textarea id="textInput" placeholder="输入要发送的文本或链接..." 
                    style="width: 100%; min-height: 80px; padding: 12px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 0.95em; transition: all 0.2s;"></textarea>
                <div style="margin-top: 12px; text-align: center;">
                    <button class="btn" onclick="sendText()">发送文本</button>
                </div>
            </div>
            
            <div>
                <h2 style="color: #667eea; margin-bottom: 15px;">📋 传输历史</h2>
                <div id="historyList">
                {% for item in history %}
                <div class="history-item">
                    {% if item.type == 'image' %}
                    <img src="/api/download/{{ item.filename }}" class="thumbnail" alt="预览">
                    {% endif %}
                    <div style="flex: 1;">
                        <strong>{{ item.name }}</strong>
                        <div style="color: #999; font-size: 0.85em;">{{ item.time }}</div>
                    </div>
                    <div style="display: flex; gap: 6px;">
                        {% if item.type == 'text' %}
                        <button class="btn-small btn-copy" onclick="copyText('{{ item.content }}')">📋</button>
                        {% endif %}
                        {% if item.type != 'text' %}
                        <a href="/api/download/{{ item.filename }}" class="btn-small btn-download" download>⬇️</a>
                        {% endif %}
                        <button class="btn-small btn-delete" onclick="deleteItem('{{ item.filename }}')">🗑️</button>
                    </div>
                </div>
                {% endfor %}
                </div>
            </div>
        </div>
    </div>
    
    <div id="toast" class="toast"></div>
    
    <script>
        // 自动刷新相关变量
        let autoRefreshInterval = null;
        let isAutoRefreshEnabled = true;
        const REFRESH_INTERVAL = 1000; // 1秒
        
        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }
        
        async function sendText() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) return;
            
            try {
                await fetch('/api/upload/text', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });
                showToast('✅ 发送成功');
                // 不刷新页面，等待自动刷新
                document.getElementById('textInput').value = '';
            } catch (error) {
                showToast('❌ 发送失败');
            }
        }
        
        // 文本框键盘事件：Enter发送，Shift+Enter换行
        document.addEventListener('DOMContentLoaded', () => {
            const textInput = document.getElementById('textInput');
            if (textInput) {
                textInput.addEventListener('keydown', (e) => {
                    // Enter键（不按Shift）
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault(); // 阻止默认换行
                        sendText(); // 发送文本
                    }
                    // Shift+Enter：允许默认换行行为，不做任何处理
                });
            }
        });
        
        async function copyText(text) {
            try {
                // 尝试使用现代API
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(text);
                    showToast('✅ 已复制');
                } else {
                    // 降级方案：使用传统方法
                    fallbackCopyText(text);
                }
            } catch (error) {
                console.error('复制失败:', error);
                // 降级方案
                fallbackCopyText(text);
            }
        }
        
        // 降级复制方法（兼容旧浏览器）
        function fallbackCopyText(text) {
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            textarea.style.top = '-9999px';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            
            try {
                const successful = document.execCommand('copy');
                if (successful) {
                    showToast('✅ 已复制');
                } else {
                    showToast('❌ 复制失败');
                }
            } catch (err) {
                console.error('降级复制也失败:', err);
                showToast('❌ 复制失败，请手动复制');
            } finally {
                document.body.removeChild(textarea);
            }
        }
        
        async function deleteItem(filename) {
            if (!confirm('确定删除？')) return;
            try {
                await fetch(`/api/history/delete/${filename}`, { method: 'DELETE' });
                showToast('✅ 已删除');
                // 立即刷新历史记录
                await loadHistory();
            } catch (error) {
                showToast('❌ 删除失败');
            }
        }
        
        document.getElementById('uploadZone').addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });
        
        document.getElementById('fileInput').addEventListener('change', async (e) => {
            const files = e.target.files;
            if (files.length === 0) return;
            
            showToast(`正在上传 ${files.length} 个文件...`);
            
            for (let file of files) {
                const formData = new FormData();
                formData.append('file', file);
                await fetch('/api/upload/file', { method: 'POST', body: formData });
            }
            showToast('✅ 上传成功');
            // 不刷新页面，等待自动刷新
        });
        
        // ========== 自动刷新功能 ==========
        
        /**
         * 加载历史记录（AJAX方式）
         */
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();
                
                if (data.success) {
                    updateHistoryList(data.history);
                }
            } catch (error) {
                console.error('加载历史记录失败:', error);
            }
        }
        
        /**
         * 更新历史记录列表DOM
         */
        function updateHistoryList(history) {
            const historyList = document.getElementById('historyList');
            if (!historyList) return;
            
            // 如果为空
            if (history.length === 0) {
                historyList.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">暂无历史记录</p>';
                return;
            }
            
            // 生成HTML
            let html = '';
            history.forEach(item => {
                html += generateHistoryItemHTML(item);
            });
            
            // 检查是否有新记录（通过比较第一个元素的时间戳）
            const firstOldItem = historyList.querySelector('.history-item');
            const hasNewRecords = !firstOldItem || (history.length > 0 && firstOldItem.dataset.time !== history[0].time);
            
            // 更新DOM
            historyList.innerHTML = html;
            
            // 如果有新记录，添加高亮动画
            if (hasNewRecords && history.length > 0) {
                const firstNewItem = historyList.querySelector('.history-item');
                if (firstNewItem) {
                    firstNewItem.style.animation = 'highlightNew 1s ease';
                }
            }
        }
        
        /**
         * 生成单个历史记录项的HTML
         */
        function generateHistoryItemHTML(item) {
            const iconHtml = item.type === 'image' 
                ? `<img src="/api/download/${item.filename}" class="thumbnail" alt="预览">`
                : '';
            
            const actionButtons = [];
            
            if (item.type === 'text') {
                const escapedContent = item.content.replace(/'/g, "\\'").replace(/"/g, '\\"');
                actionButtons.push(`<button class="btn-small btn-copy" onclick="copyText('${escapedContent}')">📋</button>`);
            }
            
            if (item.type !== 'text') {
                actionButtons.push(`<a href="/api/download/${item.filename}" class="btn-small btn-download" download>⬇️</a>`);
            }
            
            actionButtons.push(`<button class="btn-small btn-delete" onclick="deleteItem('${item.filename}')">🗑️</button>`);
            
            return `
                <div class="history-item" data-time="${item.time}" data-filename="${item.filename}">
                    ${iconHtml}
                    <div style="flex: 1;">
                        <strong>${escapeHtml(item.name)}</strong>
                        <div style="color: #999; font-size: 0.85em;">${item.time}</div>
                    </div>
                    <div style="display: flex; gap: 6px;">
                        ${actionButtons.join('')}
                    </div>
                </div>
            `;
        }
        
        /**
         * HTML转义
         */
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        /**
         * 启动自动刷新
         */
        function startAutoRefresh() {
            if (autoRefreshInterval) return;
            
            autoRefreshInterval = setInterval(() => {
                if (isAutoRefreshEnabled) {
                    loadHistory();
                }
            }, REFRESH_INTERVAL);
            
            console.log('✅ 自动刷新已启动（每2秒）');
        }
        
        /**
         * 停止自动刷新
         */
        function stopAutoRefresh() {
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
                autoRefreshInterval = null;
                console.log('⏸️ 自动刷新已暂停');
            }
        }
        
        /**
         * 切换自动刷新状态
         */
        function toggleAutoRefresh() {
            isAutoRefreshEnabled = !isAutoRefreshEnabled;
            const statusText = isAutoRefreshEnabled ? '✅ 自动刷新已开启' : '⏸️ 自动刷新已暂停';
            showToast(statusText);
            console.log(statusText);
        }
        
        /**
         * 手动刷新（重置计时器）
         */
        async function manualRefresh() {
            showToast('🔄 正在刷新...');
            stopAutoRefresh();
            await loadHistory();
            startAutoRefresh();
        }
        
        // 页面加载完成后启动自动刷新
        window.addEventListener('load', () => {
            startAutoRefresh();
        });
        
        // 页面卸载时清除定时器
        window.addEventListener('beforeunload', () => {
            stopAutoRefresh();
        });
        
        // 添加高亮动画样式
        const style = document.createElement('style');
        style.textContent = `
            @keyframes highlightNew {
                0% { background-color: #fff3cd; transform: scale(1.02); }
                100% { background-color: #f8f9fa; transform: scale(1); }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
    '''


def get_mobile_html_template():
    """手机端UI - 垂直流式布局，专为移动浏览器优化"""
    return '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <title>文件传输</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 0;
            overflow-x: hidden;
        }
        
        /* 顶部标题栏 */
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 14px 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }
        
        .header p {
            color: #999;
            font-size: 11px;
            margin-top: 3px;
        }
        
        /* 主内容区 */
        .content {
            padding: 12px;
            padding-bottom: 80px;
        }
        
        /* 卡片样式 */
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .card-title {
            font-size: 15px;
            font-weight: 600;
            color: #333;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        /* 快捷操作按钮网格 */
        .action-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .action-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 16px 12px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            min-height: 70px;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
        }
        
        .action-btn:active {
            transform: scale(0.96);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        .action-btn.secondary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
        }
        
        .action-btn.success {
            background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
        }
        
        .action-icon {
            font-size: 24px;
        }
        
        /* 文本输入区 */
        .text-input-area {
            width: 100%;
            min-height: 100px;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 14px;
            resize: none;
            font-family: inherit;
            transition: all 0.2s ease;
        }
        
        .text-input-area:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .send-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 14px;
            font-size: 15px;
            font-weight: 600;
            margin-top: 10px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .send-btn:active {
            transform: scale(0.98);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        /* 历史记录列表 */
        .history-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .history-item {
            background: rgba(248, 249, 250, 0.8);
            backdrop-filter: blur(5px);
            border-radius: 12px;
            padding: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(0, 0, 0, 0.04);
        }
        
        .history-item:active {
            background: rgba(238, 240, 255, 0.9);
            transform: scale(0.98);
        }
        
        .history-icon {
            width: 42px;
            height: 42px;
            border-radius: 10px;
            object-fit: cover;
            border: 2px solid rgba(102, 126, 234, 0.3);
            flex-shrink: 0;
            transition: all 0.2s ease;
        }
        
        .history-icon:hover {
            transform: scale(1.05);
            border-color: #667eea;
        }
        
        .history-info {
            flex: 1;
            min-width: 0;
        }
        
        .history-name {
            font-size: 13px;
            font-weight: 600;
            color: #333;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-bottom: 3px;
        }
        
        .history-time {
            font-size: 11px;
            color: #999;
        }
        
        .history-actions {
            display: flex;
            gap: 8px;
            flex-shrink: 0;
        }
        
        .icon-btn {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .icon-btn:active {
            transform: scale(0.9);
        }
        
        .icon-btn.copy {
            background: #667eea;
            color: white;
        }
        
        .icon-btn.download {
            background: #48bb78;
            color: white;
        }
        
        .icon-btn.delete {
            background: #f56565;
            color: white;
        }
        
        /* Toast提示 */
        .toast {
            position: fixed;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: rgba(0, 0, 0, 0.85);
            color: white;
            padding: 14px 24px;
            border-radius: 25px;
            font-size: 14px;
            z-index: 1000;
            opacity: 0;
            transition: all 0.3s ease;
            pointer-events: none;
            white-space: nowrap;
        }
        
        .toast.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
        
        /* 空状态 */
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #999;
        }
        
        .empty-icon {
            font-size: 48px;
            margin-bottom: 12px;
        }
        
        /* 底部固定操作栏 */
        .bottom-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 12px 16px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            display: flex;
            gap: 10px;
            z-index: 99;
        }
        
        .bottom-btn {
            flex: 1;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 14px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
        }
        
        .bottom-btn:active {
            opacity: 0.9;
        }
        
        /* 隐藏文件输入 */
        #fileInput {
            display: none;
        }
    </style>
</head>
<body>
    <!-- 顶部标题 -->
    <div class="header">
        <h1>📱 文件传输</h1>
        <p>扫码连接 · 快速传输</p>
    </div>
    
    <!-- 主内容 -->
    <div class="content">
        <!-- 快捷操作 -->
        <div class="card">
            <div class="card-title">⚡ 快速发送</div>
            <div class="action-grid">
                <button class="action-btn" onclick="document.getElementById('fileInput').click()">
                    <span class="action-icon">📁</span>
                    <span>选择文件</span>
                </button>
                <button class="action-btn secondary" onclick="showTextInput()">
                    <span class="action-icon">📝</span>
                    <span>发送文本</span>
                </button>
                <button class="action-btn success" onclick="pasteFromClipboard()">
                    <span class="action-icon">📋</span>
                    <span>粘贴文本</span>
                </button>
                <button class="action-btn" onclick="location.reload()">
                    <span class="action-icon">🔄</span>
                    <span>刷新</span>
                </button>
            </div>
            <input type="file" id="fileInput" multiple accept="*/*">
        </div>
        
        <!-- 文本输入（默认隐藏） -->
        <div class="card" id="textInputCard" style="display: none;">
            <div class="card-title">📝 发送文本</div>
            <textarea id="textInput" class="text-input-area" placeholder="输入要发送的文本或链接..."></textarea>
            <button class="send-btn" onclick="sendText()">发送</button>
        </div>
        
        <!-- 传输历史 -->
        <div class="card">
            <div class="card-title">📋 最近传输</div>
            <div class="history-list" id="historyList">
                {% if history %}
                {% for item in history %}
                <div class="history-item">
                    {% if item.type == 'image' %}
                    <img src="/api/download/{{ item.filename }}" class="history-icon" alt="">
                    {% else %}
                    <div class="history-icon" style="display: flex; align-items: center; justify-content: center; background: #f0f0f0; font-size: 20px;">
                        {% if item.type == 'text' %}📝{% else %}📁{% endif %}
                    </div>
                    {% endif %}
                    <div class="history-info">
                        <div class="history-name">{{ item.name }}</div>
                        <div class="history-time">{{ item.time }}</div>
                    </div>
                    <div class="history-actions">
                        {% if item.type == 'text' %}
                        <button class="icon-btn copy" onclick="copyText('{{ item.content | replace("'", "\\'") }}')">📋</button>
                        {% endif %}
                        {% if item.type != 'text' %}
                        <a href="/api/download/{{ item.filename }}" class="icon-btn download" download>⬇️</a>
                        {% endif %}
                        <button class="icon-btn delete" onclick="deleteItem('{{ item.filename }}')">🗑️</button>
                    </div>
                </div>
                {% endfor %}
                {% else %}
                <div class="empty-state">
                    <div class="empty-icon">📭</div>
                    <div>暂无传输记录</div>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Toast提示 -->
    <div id="toast" class="toast"></div>
    
    <script>
        // 自动刷新相关变量
        let autoRefreshInterval = null;
        let isAutoRefreshEnabled = true;
        const REFRESH_INTERVAL = 1000; // 1秒
        
        // 显示Toast
        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }
        
        // 显示文本输入框
        function showTextInput() {
            const card = document.getElementById('textInputCard');
            card.style.display = card.style.display === 'none' ? 'block' : 'none';
            if (card.style.display === 'block') {
                document.getElementById('textInput').focus();
            }
        }
        
        // 发送文本
        async function sendText() {
            const text = document.getElementById('textInput').value.trim();
            if (!text) {
                showToast('请输入内容');
                return;
            }
            
            try {
                await fetch('/api/upload/text', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });
                showToast('✅ 发送成功');
                document.getElementById('textInput').value = '';
                // 不刷新页面，等待自动刷新
            } catch (error) {
                showToast('❌ 发送失败');
            }
        }
        
        // 文本框键盘事件：Enter发送，Shift+Enter换行
        document.addEventListener('DOMContentLoaded', () => {
            const textInput = document.getElementById('textInput');
            if (textInput) {
                textInput.addEventListener('keydown', (e) => {
                    // Enter键（不按Shift）
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault(); // 阻止默认换行
                        sendText(); // 发送文本
                    }
                    // Shift+Enter：允许默认换行行为，不做任何处理
                });
            }
        });
        
        // 从剪贴板粘贴
        async function pasteFromClipboard() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById('textInput').value = text;
                showTextInput();
                showToast('✅ 已粘贴');
            } catch (error) {
                showToast('❌ 无法访问剪贴板');
            }
        }
        
        // 复制文本
        async function copyText(text) {
            try {
                // 尝试使用现代API
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(text);
                    showToast('✅ 已复制');
                } else {
                    // 降级方案：使用传统方法
                    fallbackCopyText(text);
                }
            } catch (error) {
                console.error('复制失败:', error);
                // 降级方案
                fallbackCopyText(text);
            }
        }
        
        // 降级复制方法（兼容旧浏览器）
        function fallbackCopyText(text) {
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            textarea.style.top = '-9999px';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            
            try {
                const successful = document.execCommand('copy');
                if (successful) {
                    showToast('✅ 已复制');
                } else {
                    showToast('❌ 复制失败');
                }
            } catch (err) {
                console.error('降级复制也失败:', err);
                showToast('❌ 复制失败，请手动复制');
            } finally {
                document.body.removeChild(textarea);
            }
        }
        
        // 删除记录
        async function deleteItem(filename) {
            if (!confirm('确定删除？')) return;
            try {
                await fetch(`/api/history/delete/${filename}`, { method: 'DELETE' });
                showToast('✅ 已删除');
                // 立即刷新历史记录
                await loadHistory();
            } catch (error) {
                showToast('❌ 删除失败');
            }
        }
        
        // 文件上传
        document.getElementById('fileInput').addEventListener('change', async (e) => {
            const files = e.target.files;
            if (files.length === 0) return;
            
            showToast(`正在上传 ${files.length} 个文件...`);
            
            for (let file of files) {
                const formData = new FormData();
                formData.append('file', file);
                await fetch('/api/upload/file', { method: 'POST', body: formData });
            }
            
            showToast('✅ 上传成功');
            // 不刷新页面，等待自动刷新
        });
        
        // 阻止页面滚动反弹（iOS）
        document.body.addEventListener('touchmove', function(e) {
            if (e.target.closest('.history-list')) return;
        }, { passive: true });
        
        // ========== 自动刷新功能 ==========
        
        /**
         * 加载历史记录（AJAX方式）
         */
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();
                
                if (data.success) {
                    updateHistoryList(data.history);
                }
            } catch (error) {
                console.error('加载历史记录失败:', error);
            }
        }
        
        /**
         * 更新历史记录列表DOM
         */
        function updateHistoryList(history) {
            const historyList = document.getElementById('historyList');
            if (!historyList) return;
            
            // 如果为空
            if (history.length === 0) {
                historyList.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">📭</div>
                        <div>暂无传输记录</div>
                    </div>
                `;
                return;
            }
            
            // 生成HTML
            let html = '';
            history.forEach(item => {
                html += generateHistoryItemHTML(item);
            });
            
            // 检查是否有新记录
            const firstOldItem = historyList.querySelector('.history-item');
            const hasNewRecords = !firstOldItem || (history.length > 0 && firstOldItem.dataset.time !== history[0].time);
            
            // 更新DOM
            historyList.innerHTML = html;
            
            // 如果有新记录，添加高亮动画
            if (hasNewRecords && history.length > 0) {
                const firstNewItem = historyList.querySelector('.history-item');
                if (firstNewItem) {
                    firstNewItem.style.animation = 'highlightNew 1s ease';
                }
            }
        }
        
        /**
         * 生成单个历史记录项的HTML
         */
        function generateHistoryItemHTML(item) {
            const iconHtml = item.type === 'image'
                ? `<img src="/api/download/${item.filename}" class="history-icon" alt="">`
                : `<div class="history-icon" style="display: flex; align-items: center; justify-content: center; background: #f0f0f0; font-size: 20px;">${item.type === 'text' ? '📝' : '📁'}</div>`;
            
            const actionButtons = [];
            
            if (item.type === 'text') {
                const escapedContent = item.content.replace(/'/g, "\\'").replace(/"/g, '\\"');
                actionButtons.push(`<button class="icon-btn copy" onclick="copyText('${escapedContent}')">📋</button>`);
            }
            
            if (item.type !== 'text') {
                actionButtons.push(`<a href="/api/download/${item.filename}" class="icon-btn download" download>⬇️</a>`);
            }
            
            actionButtons.push(`<button class="icon-btn delete" onclick="deleteItem('${item.filename}')">🗑️</button>`);
            
            return `
                <div class="history-item" data-time="${item.time}" data-filename="${item.filename}">
                    ${iconHtml}
                    <div class="history-info">
                        <div class="history-name">${escapeHtml(item.name)}</div>
                        <div class="history-time">${item.time}</div>
                    </div>
                    <div class="history-actions">
                        ${actionButtons.join('')}
                    </div>
                </div>
            `;
        }
        
        /**
         * HTML转义
         */
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        /**
         * 启动自动刷新
         */
        function startAutoRefresh() {
            if (autoRefreshInterval) return;
            
            autoRefreshInterval = setInterval(() => {
                if (isAutoRefreshEnabled) {
                    loadHistory();
                }
            }, REFRESH_INTERVAL);
            
            console.log('✅ 自动刷新已启动（每2秒）');
        }
        
        /**
         * 停止自动刷新
         */
        function stopAutoRefresh() {
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
                autoRefreshInterval = null;
                console.log('⏸️ 自动刷新已暂停');
            }
        }
        
        /**
         * 切换自动刷新状态
         */
        function toggleAutoRefresh() {
            isAutoRefreshEnabled = !isAutoRefreshEnabled;
            const statusText = isAutoRefreshEnabled ? '✅ 自动刷新已开启' : '⏸️ 自动刷新已暂停';
            showToast(statusText);
            console.log(statusText);
        }
        
        /**
         * 手动刷新（重置计时器）
         */
        async function manualRefresh() {
            showToast('🔄 正在刷新...');
            stopAutoRefresh();
            await loadHistory();
            startAutoRefresh();
        }
        
        // 页面加载完成后启动自动刷新
        window.addEventListener('load', () => {
            startAutoRefresh();
        });
        
        // 页面卸载时清除定时器
        window.addEventListener('beforeunload', () => {
            stopAutoRefresh();
        });
        
        // 添加高亮动画样式
        const style = document.createElement('style');
        style.textContent = `
            @keyframes highlightNew {
                0% { background-color: #fff3cd; transform: scale(1.02); }
                100% { background-color: #f8f9fa; transform: scale(1); }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
    '''

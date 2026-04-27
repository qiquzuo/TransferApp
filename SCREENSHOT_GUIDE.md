# 📸 截图制作指南

**目的：** 为README和社交媒体准备精美的界面截图

---

## 🎯 需要准备的截图

### 1. 电脑端界面 (desktop.png)

**要求：**
- 分辨率：1920x1080
- 展示完整界面
- 包含上传区和历史记录
- 浏览器窗口居中显示

**步骤：**
1. 启动服务器 `python server.py`
2. 浏览器访问 `http://localhost:5000`
3. 调整浏览器窗口到合适大小
4. 使用截图工具（如Snipaste）截取
5. 保存为 `screenshots/desktop.png`

---

### 2. 手机端界面 (mobile.png)

**要求：**
- 分辨率：1080x1920（竖屏）
- 展示手机浏览器界面
- 包含操作按钮和历史记录

**方法1：真实手机截图**
1. 手机连接同一WiFi
2. 浏览器访问电脑IP:5000
3. 手机截图
4. 传到电脑

**方法2：浏览器模拟**
1. Chrome打开 `http://localhost:5000`
2. F12打开开发者工具
3. 点击设备切换按钮（Ctrl+Shift+M）
4. 选择iPhone或Android设备
5. 截图保存

---

### 3. 功能演示GIF (demo.gif)

**录制内容：**
1. 启动服务器
2. 手机扫码连接
3. 拖拽文件上传
4. 文本发送
5. 历史记录实时更新

**工具推荐：**
- Windows: ShareX、ScreenToGif
- Mac: LICEcap、Gifox
- 在线: ezgif.com

**要求：**
- 时长：10-15秒
- 文件大小：<5MB
- 帧率：15-20fps
- 清晰展示核心功能

---

### 4. 二维码扫描演示 (qrcode-scan.gif)

**录制内容：**
1. 显示电脑端二维码
2. 手机扫描二维码
3. 成功连接的提示

---

## 🎨 截图美化技巧

### 1. 添加边框和阴影

使用在线工具：
- https://mockuphone.com/
- https://shots.so/
- https://cleanmock.com/

### 2. 统一配色

确保截图中的颜色协调：
- 背景：渐变色或纯色
- 突出紫色主题 (#667eea, #764ba2)
- 避免杂乱元素

### 3. 标注重点

使用箭头或文字标注：
- 上传区域
- 发送按钮
- 历史记录
- 关键功能

---

## 📐 截图尺寸规范

| 用途 | 尺寸 | 格式 |
|------|------|------|
| README主图 | 1920x1080 | PNG |
| 手机界面 | 1080x1920 | PNG |
| 演示GIF | 1280x720 | GIF |
| 社交媒体 | 1200x630 | PNG/JPG |
| Product Hunt | 1270x760 | PNG |

---

## 🛠️ 快速截图脚本

创建一个Python脚本来自动生成截图：

```python
# screenshot_helper.py
from selenium import webdriver
from time import sleep

def take_desktop_screenshot():
    """自动截取电脑端界面"""
    driver = webdriver.Chrome()
    driver.get('http://localhost:5000')
    driver.maximize_window()
    sleep(2)  # 等待页面加载
    driver.save_screenshot('screenshots/desktop.png')
    driver.quit()
    print("✅ Desktop screenshot saved!")

def take_mobile_screenshot():
    """自动截取手机端界面"""
    mobile_emulation = {
        "deviceName": "iPhone 12 Pro"
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://localhost:5000')
    sleep(2)
    driver.save_screenshot('screenshots/mobile.png')
    driver.quit()
    print("✅ Mobile screenshot saved!")

if __name__ == '__main__':
    take_desktop_screenshot()
    take_mobile_screenshot()
```

**使用：**
```bash
pip install selenium
python screenshot_helper.py
```

---

## ✅ 截图检查清单

完成以下检查后再用于推广：

- [ ] 图片清晰，无模糊
- [ ] 尺寸符合要求
- [ ] 文件名正确（desktop.png, mobile.png等）
- [ ] 已保存到screenshots目录
- [ ] 在README中测试显示正常
- [ ] 无明显bug或错误信息
- [ ] 展示了核心功能
- [ ] 视觉美观，配色协调

---

## 💡 替代方案

如果暂时无法制作精美截图：

### 方案1：使用占位图
```markdown
![Desktop UI](https://via.placeholder.com/1920x1080?text=Desktop+UI+Screenshot)
```

### 方案2：文字说明
```markdown
> 📸 Screenshots coming soon! 
> The UI features a modern glassmorphism design with purple gradient theme.
```

### 方案3：邀请贡献
```markdown
## 📸 Screenshot Contribution Wanted!

Help us make TransferApp better by contributing beautiful screenshots!

Requirements:
- Desktop UI (1920x1080)
- Mobile UI (1080x1920)
- Demo GIF showing file transfer

Submit via Pull Request! 🙏
```

---

<div align="center">

**准备好截图后，README会更加吸引人！**

**立即行动：启动服务器，开始截图！** 📸✨

</div>

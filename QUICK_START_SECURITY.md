# 🚀 快速开始 - 安全增强版

## ⚡ 3步启用安全功能

### 步骤1：生成SSL证书（1分钟）

```bash
python generate_cert.py
```

**输出：**
```
✅ 证书生成成功！
📄 cert.pem
🔑 key.pem
```

---

### 步骤2：启动服务器（自动HTTPS）

```bash
python server.py
```

**输出：**
```
🚀 局域网文件传输服务器启动成功！（HTTPS加密）
🔒 连接已加密，数据传输安全
📍 服务器地址: https://192.168.0.102:5000
🔐 默认密码: admin123
```

---

### 步骤3：浏览器访问

1. 扫描二维码或访问 `https://192.168.0.102:5000`
2. 接受证书警告（点击"高级" → "继续访问"）
3. 输入密码：`admin123`
4. 开始使用！

---

## 🔑 修改密码（可选但推荐）

### Windows PowerShell

```powershell
# 生成新密码的哈希值
$env:ADMIN_PASSWORD_HASH = (echo -n "your_new_password" | python -c "import sys,hashlib; print(hashlib.sha256(sys.stdin.read().encode()).hexdigest())")

# 启动服务器
python server.py
```

### Linux/Mac

```bash
# 生成新密码的哈希值
export ADMIN_PASSWORD_HASH=$(echo -n "your_new_password" | python3 -c "import sys,hashlib; print(hashlib.sha256(sys.stdin.read().encode()).hexdigest())")

# 启动服务器
python3 server.py
```

---

## 📱 消除证书警告（可选）

### Windows

```powershell
certutil -addstore -f "ROOT" cert.pem
```

### Android

设置 → 安全 → 从SD卡安装证书 → 选择 `cert.pem`

### iOS

1. 通过AirDrop发送 `cert.pem` 到iPhone
2. 点击文件 → 安装
3. 设置 → 通用 → 关于本机 → 证书信任设置 → 启用

---

## 🛡️ 安全特性

| 特性 | 状态 | 说明 |
|------|------|------|
| HTTPS加密 | ✅ | 数据传输安全 |
| 身份认证 | ✅ | 密码保护 |
| 文件验证 | ✅ | Magic Number检查 |
| XSS防护 | ✅ | SVG脚本清理 |
| 速率限制 | ✅ | 防止暴力攻击 |

---

## 📊 API使用示例

### 登录

```bash
curl -X POST https://192.168.0.102:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"password":"admin123"}'
```

### 上传文件

```bash
curl -X POST https://192.168.0.102:5000/api/upload/file \
  -H "X-Auth-Token: admin123" \
  -F "file=@photo.jpg"
```

### 登出

```bash
curl -X POST https://192.168.0.102:5000/api/logout
```

---

## ⚠️ 重要提示

1. **首次使用会看到证书警告** - 这是正常的，点击"继续访问"即可
2. **默认密码是 admin123** - 建议尽快修改
3. **关闭浏览器后需要重新登录** - Session会自动失效
4. **证书有效期1年** - 明年需要重新生成

---

## 🆘 常见问题

**Q: 忘记密码怎么办？**  
A: 重启服务器，或者设置新的 `ADMIN_PASSWORD_HASH` 环境变量

**Q: 如何查看当前密码？**  
A: 密码以哈希形式存储，无法反向解密。如果忘记，只能重置

**Q: 可以不用HTTPS吗？**  
A: 可以，删除 `cert.pem` 和 `key.pem` 文件，服务器会自动降级到HTTP（不推荐）

**Q: 速率限制太严格？**  
A: 修改 `server.py` 中的 `@limiter.limit()` 参数

---

<div align="center">

**🎉 安全增强版已就绪！**

**享受安全的文件传输体验！** 🔒✨

</div>

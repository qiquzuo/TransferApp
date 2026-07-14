@echo off
chcp 65001 >nul
echo ========================================
echo   TransferApp 网络连接诊断工具
echo ========================================
echo.

echo [1] 检查服务器运行状态...
netstat -ano | findstr "LISTENING" | findstr "5000" >nul
if %errorlevel% equ 0 (
    echo ✓ 服务器正在运行
    netstat -ano | findstr "LISTENING" | findstr "5000"
) else (
    echo ✗ 服务器未运行
    echo 请运行 start_server.bat 启动服务器
    goto end
)
echo.

echo [2] 检查本机IP地址...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set ip=%%a
    echo !ip!
)
echo.

echo [3] 当前WiFi IP地址:
ipconfig | findstr -A 3 "WLAN" | findstr "IPv4"
echo.

echo [4] 测试本地访问...
curl -s http://127.0.0.1:5000/api/history >nul
if %errorlevel% equ 0 (
    echo ✓ 本地访问正常
) else (
    echo ✗ 本地访问失败
)
echo.

echo [5] 防火墙状态:
netsh advfirewall show allprofiles state | findstr "状态"
echo.

echo ========================================
echo 手机连接说明:
echo ========================================
echo 1. 确保手机和电脑连接到同一个WiFi
echo 2. 在手机浏览器中输入上述显示的IP地址
echo 3. 如果无法连接，请检查:
echo    - Windows防火墙是否允许5000端口
echo    - 路由器是否阻止设备间通信
echo    - 手机和电脑是否在同一网段
echo.
echo 推荐访问地址:
echo http://192.168.0.102:5000
echo ========================================

:end
pause

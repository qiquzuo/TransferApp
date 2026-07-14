@echo off
chcp 65001 >nul
echo ========================================
echo   打包 TransferApp 自启动便携版
echo ========================================
echo.

REM 清理旧的构建文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [1/3] 正在使用PyInstaller打包...
pyinstaller --onefile ^
    --windowed ^
    --name=TransferApp ^
    --add-data "requirements.txt;." ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
    --hidden-import=flask_limiter ^
    --hidden-import=qrcode ^
    --hidden-import=PIL ^
    server.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo [2/3] 正在准备发布文件...

REM 创建发布文件夹
if not exist Release rmdir /s /q Release
mkdir Release

REM 复制exe
copy dist\TransferApp.exe Release\

REM 复制启动器和自启动脚本
copy background_launcher.vbs Release\
copy setup_autostart.bat Release\
copy remove_autostart.bat Release\
copy README.md Release\

echo.
echo [3/3] 创建ZIP压缩包...

REM 获取版本号
for /f "tokens=*" %%i in ('powershell -Command "(Get-Date).ToString(\"yyyyMMdd\")"') do set DATE_VER=%%i

set ZIP_NAME=TransferApp_AutoStart_v%DATE_VER%.zip

if exist "%ZIP_NAME%" del /q "%ZIP_NAME%"
powershell -Command "Compress-Archive -Path 'Release\*' -DestinationPath '%ZIP_NAME%' -Force"

echo.
echo ========================================
echo   ✅ 打包成功！
echo ========================================
echo.
echo 📦 发布文件: %ZIP_NAME%
echo.
echo 包含的文件:
echo   - TransferApp.exe          (主程序，后台运行)
echo   - background_launcher.vbs  (静默启动器)
echo   - setup_autostart.bat      (设置开机自启动)
echo   - remove_autostart.bat     (移除开机自启动)
echo   - README.md                (使用说明)
echo.
echo 🚀 使用方法:
echo   1. 解压ZIP到任意目录
echo   2. 双击 TransferApp.exe 启动（后台运行，无窗口）
echo   3. 运行 setup_autostart.bat 设置开机自启动
echo   4. 浏览器访问 http://本机IP:5000
echo.
echo ========================================
pause

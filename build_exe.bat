@echo off
chcp 65001 >nul
echo ========================================
echo   正在打包为exe文件...
echo ========================================
echo.

REM 清理旧的构建文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist server.spec del /q server.spec

echo [1/3] 正在使用PyInstaller打包...
pyinstaller --onefile ^
    --windowed ^
    --name=FileTransferServer ^
    --icon=NONE ^
    --add-data "requirements.txt;." ^
    --hidden-import=flask ^
    --hidden-import=flask_cors ^
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
echo [2/3] 打包完成！
echo.
echo [3/3] 正在整理文件...

REM 创建发布文件夹
if not exist Release mkdir Release

REM 复制exe到Release文件夹
copy dist\FileTransferServer.exe Release\

REM 复制说明文档
copy README.md Release\
copy QUICKSTART.md Release\

echo.
echo ========================================
echo   ✅ 打包成功！
echo ========================================
echo.
echo 📦 发布文件位置: .\Release\
echo.
echo 包含的文件:
echo   - FileTransferServer.exe  (主程序)
echo   - README.md              (使用说明)
echo   - QUICKSTART.md          (快速入门)
echo.
echo 🚀 使用方法:
echo   1. 将整个Release文件夹拷贝到其他电脑
echo   2. 双击运行 FileTransferServer.exe
echo   3. 无需安装Python或其他依赖！
echo.
echo 💡 提示:
echo   - 首次运行可能需要几秒启动时间
echo   - 接收的文件会保存在exe同目录的received_files文件夹
echo   - 确保目标电脑和目标手机在同一WiFi网络
echo.
echo ========================================

pause

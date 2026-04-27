@echo off
chcp 65001 >nul
echo ========================================
echo   局域网文件传输服务器 - 启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/2] 正在安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if errorlevel 1 (
    echo [警告] 依赖安装失败，尝试使用默认源...
    pip install -r requirements.txt
)

echo.
echo [2/2] 正在启动服务器...
echo.

python server.py

pause

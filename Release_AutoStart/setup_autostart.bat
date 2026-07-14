@echo off
chcp 65001 >nul
echo ========================================
echo   TransferApp 开机自启动设置
echo ========================================
echo.

:: 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "VBS_PATH=%SCRIPT_DIR%background_launcher.vbs"
set "TASK_NAME=TransferApp_AutoStart"

:: 检查VBS文件是否存在
if not exist "%VBS_PATH%" (
    echo [错误] 找不到 background_launcher.vbs
    echo 请确保此脚本与 background_launcher.vbs 在同一目录
    pause
    exit /b 1
)

:: 删除旧任务（如果存在）
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

:: 创建计划任务：用户登录时自动启动
schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "wscript.exe \"%VBS_PATH%\"" ^
    /sc onlogon ^
    /rl highest ^
    /f

if errorlevel 1 (
    echo.
    echo [错误] 创建计划任务失败！
    echo 请尝试右键"以管理员身份运行"
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 设置成功！
echo ========================================
echo.
echo 已配置：每次登录Windows时自动后台启动TransferApp
echo.
echo 任务名称: %TASK_NAME%
echo 启动方式: 后台静默运行（无窗口）
echo 停止方法: 运行 remove_autostart.bat 或在任务管理器中结束进程
echo.
echo 💡 提示:
echo   - 可在"任务计划程序"中查看和管理此任务
echo   - 服务器运行在后台，可通过浏览器访问
echo   - 文件保存在 exe 同目录的 received_files 文件夹
echo.
echo ========================================
pause

@echo off
chcp 65001 >nul
echo ========================================
echo   TransferApp 移除开机自启动
echo ========================================
echo.

set "TASK_NAME=TransferApp_AutoStart"

:: 删除计划任务
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

if errorlevel 1 (
    echo [提示] 未找到自启动任务（可能已被移除）
) else (
    echo ✅ 已移除开机自启动任务
)

:: 结束后台进程
taskkill /F /IM TransferApp.exe >nul 2>&1

echo.
echo ========================================
echo   操作完成
echo ========================================
echo.
echo - 开机自启动已关闭
echo - 后台进程已终止
echo - 如需重新启动，双击 TransferApp.exe 或 background_launcher.vbs
echo.
pause

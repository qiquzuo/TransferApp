' TransferApp 后台静默启动器
' 双击运行此文件即可在后台启动服务器（无控制台窗口）
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' 获取脚本所在目录
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)
exePath = scriptPath & "\TransferApp.exe"

' 检查exe是否存在
If Not fso.FileExists(exePath) Then
    MsgBox "找不到 TransferApp.exe" & vbCrLf & "请确保此文件与 TransferApp.exe 在同一目录", vbCritical, "启动失败"
    WScript.Quit
End If

' 静默启动（第二个参数0=隐藏窗口，第三个参数False=不等待进程结束）
WshShell.Run Chr(34) & exePath & Chr(34), 0, False

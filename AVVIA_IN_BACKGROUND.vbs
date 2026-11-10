Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

WshShell.CurrentDirectory = scriptDir
WshShell.Run "node bin\pendpost.mjs", 0, False

WScript.Sleep 2000

On Error Resume Next
WshShell.Run "msedge --app=http://127.0.0.1:8090", 1, False
If Err.Number <> 0 Then
    WshShell.Run "http://127.0.0.1:8090", 1, False
End If

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "Path\notifier_bat.bat" & Chr(34), 0
Set WshShell = Nothing
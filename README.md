# Todo List - Python Program (Beginners)
Todo List (Terminal) for use in College.

## General Note<br>
- Alignment issues in PyCharm run tool window.
- Run program directly in terminal to avoid this problem.
- Set terminal window width to minimum of 146 pixels.
- Shortcut to Visual Basic Script (.vbs) file should be placed in the startup (Run shell:startup) folder.
- Use Python version 3.8 or 3.9 only for *winrt* library compatibility.

### Batch File (.bat)
_@echo off<br>
"Path\python.exe" "Path\notifier.py"_<br>

### Visual Basic Script (.vbs)
_Set WshShell = CreateObject("WScript.Shell")<br>
WshShell.Run chr(34) & "Path\batch_file.bat" & Chr(34), 0<br>
Set WshShell = Nothing<br>_

### Todo Launcher (Shortcut Properties)
- **Target:** C:\WINDOWS\system32\cmd.exe /k "python todo.py"
- **Start in:** Path\Project Folder\

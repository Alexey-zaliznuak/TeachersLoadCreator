# powershell ./build.ps1
Remove-Item .\dist -Recurse -Force
flet pack main.py --icon icon.ico
Remove-Item .\build -Recurse -Force
Remove-Item .\main.spec

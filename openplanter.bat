cd D:\src\openplanter

$env:EXA_API_KEY = Read-Host "5637f031-20d9-47be-b371-ec417867f8b5" -MaskInput
$env:OPENPLANTER_SHELL = "C:\Program Files\Git\bin\bash.exe"
$env:OPENPLANTER_PROVIDER = "openrouter"
$env:OPENPLANTER_MODEL = "deepseek/deepseek-v4.1-flash"
.\openplanter-desktop\target\release\op-tauri.exe
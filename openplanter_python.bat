$env:OPENPLANTER_SHELL = "C:\Program Files\Git\bin\bash.exe"
$env:EXA_API_KEY = Read-Host "5637f031-20d9-47be-b371-ec417867f8b5" -MaskInput

python -m agent --provider openrouter --model "deepseek/deepseek-v4.1-flash"
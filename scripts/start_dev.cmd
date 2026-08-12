@echo off
REM Dev startup: native endpoint + TypeScript API

set PYTHONPATH=%~dp0..
start "Native AI" "C:\Users\Brandon\AppData\Local\Programs\Python\Python311\python.exe" "%~dp0native_chat_endpoint.py"
timeout /t 2 >nul
cd "%~dp0.."
set ASCENSION_NATIVE_ENABLED=true
set ASCENSION_NATIVE_URL=http://localhost:8000/chat
"C:\Program Files\nodejs\npm.cmd" run dev

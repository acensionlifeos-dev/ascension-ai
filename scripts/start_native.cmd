@echo off
REM Start the native Ascension AI chat endpoint for local development
set PYTHONPATH=%~dp0..
"C:\Users\Brandon\AppData\Local\Programs\Python\Python311\python.exe" "%~dp0native_chat_endpoint.py"

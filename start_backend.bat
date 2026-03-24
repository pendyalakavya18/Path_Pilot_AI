@echo off
cd %~dp0\backend
echo Starting PathPilotAI Backend...
call .venv\Scripts\activate.bat
uvicorn main:app --reload
pause

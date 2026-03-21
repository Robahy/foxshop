@echo off
call venv\scripts\activate

@REM start cmd /k fastapi dev server\app\main.py
python client\main.py

pause
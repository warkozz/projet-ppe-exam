@echo off
py -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
for /f "tokens=*" %%a in (.env.example) do set %%a
py hybrid_main.py
pause

\
        @echo off
        python -m venv venv
        call venv\Scripts\activate.bat
        pip install -r desktop_app\requirements.txt
        for /f "tokens=*" %%a in (desktop_app\.env.example) do set %%a
        python desktop_app\app\main.py
        pause

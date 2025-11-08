@echo off
echo ===========================
echo Starting NutriAI Project
echo ===========================

REM --- Setup Backend ---
cd Backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating environment...
call venv\Scripts\activate

if not exist requirements.txt (
    echo Missing requirements.txt
    pause
    exit /b
)

echo Installing dependencies (if needed)...
pip install -r requirements.txt >nul

if not exist models (
    mkdir models
)

if not exist "models\llama-2-7b-chat.Q4_K_S.gguf" (
    echo Model file not found!
    echo Please download it and place it here:
    echo %cd%\models\
    pause
)

echo Starting backend server...
start cmd /k "call venv\Scripts\activate && python main.py"
timeout /t 3 >nul

REM --- Setup Frontend ---
cd ..
if exist Frontend\app (
    echo Starting frontend...
    start cmd /k "cd Frontend\app && npm install && npm start"
) else (
    echo Frontend folder not found!
)

echo ---------------------------
echo All systems are running.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ---------------------------

pause

@echo off
echo Starting NeuralFlare AI Video Editor...
echo.

echo [1/2] Starting Backend API...
start "NeuralFlare Backend" cmd /k "cd backend && python main.py"

echo [2/2] Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo Starting Frontend...
start "NeuralFlare Frontend" cmd /k "streamlit run frontend/streamlit_app.py"

echo.
echo ========================================
echo NeuralFlare is running!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:8501
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause
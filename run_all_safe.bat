@echo off
title FAMILY TREE - RUN ALL (SAFE MODE)

echo ==========================================
echo FAMILY TREE - SAFE START
echo ==========================================

REM --- BACKEND ---
echo.
echo [1/2] Starting BACKEND (Flask)...
start cmd /k run_backend.bat

REM Đợi backend khởi động
timeout /t 5 >nul

REM --- FRONTEND ---
echo.
echo [2/2] Starting FRONTEND (Vite)...
start cmd /k run_frontend.bat

REM Mở trình duyệt
timeout /t 5 >nul
start http://localhost:5173

echo.
echo ==========================================
echo DONE.
echo - Do NOT close backend window
echo - Do NOT close frontend window
echo ==========================================

@echo off
title FAMILY TREE - BACKEND (FLASK)

echo ===============================
echo STARTING BACKEND (FLASK)
echo ===============================

cd backend

if not exist venv\Scripts\activate (
    echo ❌ ERROR: venv not found!
    pause
    exit
)

call venv\Scripts\activate

echo.
echo ▶ Running Flask on port 5000...
echo.

python app.py

echo.
echo ❌ Flask stopped!
pause

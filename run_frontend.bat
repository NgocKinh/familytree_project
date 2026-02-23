@echo off
title FAMILY TREE - FRONTEND (VITE)

echo ===============================
echo STARTING FRONTEND (VITE)
echo ===============================

cd frontend-vite

if not exist package.json (
    echo ❌ ERROR: frontend-vite not found!
    pause
    exit
)

echo.
echo ▶ Running Vite on port 5173...
echo.

npm run dev

pause

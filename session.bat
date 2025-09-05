@echo off
cd /d "."
set /p project="Project name (optional): "
set /p goal="Session goal (optional): "
python Scripts/quick-session.py --project "%project%" --goal "%goal%"
pause

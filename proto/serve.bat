@echo off
cd /d "%~dp0"
echo CobbleSpire proto: http://localhost:8765/
python -I -m http.server 8765 --bind 0.0.0.0

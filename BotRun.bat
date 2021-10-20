@echo off

call %~dp0/UpdateBot/venv/bin/activate

cd %~dp0/UpdateBot

set TOKEN = 2098888741:AAHCJY8UGeCADgCU7wHb1qlAwNLPW4Auo2A

python3 BotMain.py

pause
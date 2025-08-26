@echo off
setlocal
cd /d %~dp0

REM -- Choisir le lanceur Python : py si dispo, sinon python
where py >nul 2>nul
if %ERRORLEVEL%==0 (set "PY=py") else (set "PY=python")

REM -- Créer la venv si absente
if not exist .venv\Scripts\activate.bat (
  echo [setup] Creation de la venv...
  %PY% -m venv .venv || (echo [X] Echec creation venv & goto :end)
)

REM -- Activer la venv
echo [setup] Activation venv...
call .venv\Scripts\activate || (echo [X] Echec activation venv & goto :end)

REM -- Installer les deps si requirements.txt existe
if exist requirements.txt (
  echo [setup] Installation deps...
  pip install -r requirements.txt || (echo [X] Echec pip install & goto :end)
)

REM -- Lancer Flask
set FLASK_ENV=development
echo [run] Demarrage Flask...
python app.py
goto :eof

:end
echo.
echo [!] Le script s'est arrete suite a une erreur ci-dessus.
echo     Lance-le depuis une fenetre CMD pour voir les details.
pause

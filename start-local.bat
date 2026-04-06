@echo off
setlocal

set "ROOT=%~dp0"
set "BACKEND=%ROOT%backend"
set "FRONTEND=%ROOT%frontend"
set "PYTHON=%BACKEND%\.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
  echo [ERRO] Ambiente virtual do backend nao encontrado em "%PYTHON%".
  echo Rode a instalacao descrita no README antes de usar este script.
  exit /b 1
)

pushd "%BACKEND%"
"%PYTHON%" init_db.py
if errorlevel 1 (
  popd
  exit /b 1
)
"%PYTHON%" seed.py
if errorlevel 1 (
  popd
  exit /b 1
)
popd

start "RESTAURANTE Backend" cmd /k "cd /d %BACKEND% && .venv\Scripts\python.exe -m uvicorn app.main:app --reload"
start "RESTAURANTE Frontend" cmd /k "cd /d %FRONTEND% && npm run dev"

echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo Credenciais iniciais:
echo   admin / admin123
echo   gerente / gerente123
echo   garcom / garcom123
echo   cozinha / cozinha123

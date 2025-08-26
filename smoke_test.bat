@echo off
setlocal
set "BASE=http://127.0.0.1:5000"

echo [Smoke] /health (HTTP code)...
for /f %%I in ('curl.exe -s -o nul -w "%%{http_code}" %BASE%/health') do set CODE=%%I
if not "%CODE%"=="200" (
  echo [X] /health code = %CODE%
  exit /b 1
)

echo [Smoke] /internal/send...
curl.exe -s -X POST "%BASE%/internal/send?format=text" -H "Content-Type: application/json" -d "{\"text\":\"Salut\"}" >nul || (
  echo [X] /internal/send KO
  exit /b 1
)

echo [OK] Smoke test passe.
exit /b 0

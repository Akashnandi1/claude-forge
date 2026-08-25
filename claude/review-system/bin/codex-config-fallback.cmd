@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  py -3 "%SCRIPT_DIR%codex_config_fallback.py" %*
  exit /b %ERRORLEVEL%
)
python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  python "%SCRIPT_DIR%codex_config_fallback.py" %*
  exit /b %ERRORLEVEL%
)
echo ERROR: Python 3.11+ is required. 1>&2
exit /b 1

$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Target = 'codex_feature_review.py'
$ScriptPath = Join-Path $ScriptDir $Target

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        & py -3 $ScriptPath @args
        exit $LASTEXITCODE
    }
}
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        & python $ScriptPath @args
        exit $LASTEXITCODE
    }
}
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        & python3 $ScriptPath @args
        exit $LASTEXITCODE
    }
}

Write-Error 'Python 3.11+ is required. Install Python and ensure py, python, or python3 is available on PATH.'
exit 1

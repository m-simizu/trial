$ErrorActionPreference = "Stop"

$ObjectFile = "arithmetic_callbacks.o"
$Tests = @(
    "c_test_add_callback",
    "c_test_subtract_callback",
    "c_test_multiply_callback",
    "c_test_divide_callback"
)

$GeneratedFiles = @($ObjectFile)
foreach ($Test in $Tests) {
    $GeneratedFiles += "$Test.exe"
}

try {
    Write-Host "`n[BUILD] C source -> object file" -ForegroundColor Cyan
    Write-Host "> gcc -DARITHMETIC_CALLBACKS_NO_MAIN -c arithmetic_callbacks.c -o $ObjectFile" -ForegroundColor DarkGray
    gcc -DARITHMETIC_CALLBACKS_NO_MAIN -c arithmetic_callbacks.c -o $ObjectFile
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "`n[BUILD] C test sources -> executables" -ForegroundColor Cyan
    foreach ($Test in $Tests) {
        Write-Host "> gcc $Test.c $ObjectFile -I. -o $Test.exe" -ForegroundColor DarkGray
        gcc "$Test.c" $ObjectFile -I. -o "$Test.exe"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    Write-Host "`n[RUN] C tests" -ForegroundColor Cyan
    foreach ($Test in $Tests) {
        Write-Host "> .\$Test.exe" -ForegroundColor DarkGray
        Write-Host "[TEST OUTPUT] $Test" -ForegroundColor Yellow
        & ".\$Test.exe"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}
finally {
    Write-Host "`n[CLEANUP] generated files" -ForegroundColor Cyan
    foreach ($File in $GeneratedFiles) {
        if (Test-Path $File) {
            Write-Host "> Remove-Item -LiteralPath $File -Force" -ForegroundColor DarkGray
            Remove-Item -LiteralPath $File -Force
        }
    }
}

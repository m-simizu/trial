$ErrorActionPreference = "Stop"

$ObjectFile = "null_pointer.o"
$Tests = @(
    "c_test_read_non_null",
    "c_test_read_null",
    "c_test_write_non_null",
    "c_test_write_null"
)

$GeneratedFiles = @($ObjectFile)
foreach ($Test in $Tests) {
    $GeneratedFiles += "$Test.exe"
}

try {
    Write-Host "`n[BUILD] C source -> object file" -ForegroundColor Cyan
    Write-Host "> gcc -DNULL_POINTER_NO_MAIN -c null_pointer.c -o $ObjectFile" -ForegroundColor DarkGray
    gcc -DNULL_POINTER_NO_MAIN -c null_pointer.c -o $ObjectFile
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

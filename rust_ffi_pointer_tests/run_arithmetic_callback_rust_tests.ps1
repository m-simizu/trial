$ErrorActionPreference = "Stop"

$ObjectFile = "arithmetic_callbacks_rust.o"
$Tests = @(
    "c_test_add_callback",
    "c_test_subtract_callback",
    "c_test_multiply_callback",
    "c_test_divide_callback"
)

$GeneratedFiles = @($ObjectFile)
foreach ($Test in $Tests) {
    $GeneratedFiles += "rust_impl_$Test.exe"
}

try {
    Write-Host "`n[BUILD] Rust source -> object file" -ForegroundColor Cyan
    Write-Host "> rustc +stable-x86_64-pc-windows-gnu --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort --cfg arithmetic_callbacks_no_main arithmetic_callbacks.rs -o $ObjectFile" -ForegroundColor DarkGray
    rustc +stable-x86_64-pc-windows-gnu --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort --cfg arithmetic_callbacks_no_main arithmetic_callbacks.rs -o $ObjectFile
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "`n[BUILD] C test sources -> executables" -ForegroundColor Cyan
    foreach ($Test in $Tests) {
        Write-Host "> gcc $Test.c $ObjectFile -I. -o rust_impl_$Test.exe" -ForegroundColor DarkGray
        gcc "$Test.c" $ObjectFile -I. -o "rust_impl_$Test.exe"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    Write-Host "`n[RUN] C tests against Rust implementation" -ForegroundColor Cyan
    foreach ($Test in $Tests) {
        Write-Host "> .\rust_impl_$Test.exe" -ForegroundColor DarkGray
        Write-Host "[TEST OUTPUT] $Test" -ForegroundColor Yellow
        & ".\rust_impl_$Test.exe"
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

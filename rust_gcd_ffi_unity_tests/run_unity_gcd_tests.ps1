$ErrorActionPreference = "Stop"

$GeneratedFiles = @("gcd.o", "unity_test_gcd.exe")

$Rustc = "$env:USERPROFILE\.cargo\bin\rustc.exe"
if (-not (Test-Path $Rustc)) {
    $Rustc = "rustc"
}

$UnitySrc = "third_party\unity\src"

try {
    Write-Host "> $Rustc +stable-x86_64-pc-windows-gnu --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort gcd.rs -o gcd.o"
    & $Rustc +stable-x86_64-pc-windows-gnu --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort gcd.rs -o gcd.o
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "> gcc unity_test_gcd.c $UnitySrc\unity.c gcd.o -I. -I$UnitySrc -o unity_test_gcd.exe"
    gcc unity_test_gcd.c "$UnitySrc\unity.c" gcd.o -I. "-I$UnitySrc" -o unity_test_gcd.exe
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "> .\unity_test_gcd.exe"
    .\unity_test_gcd.exe
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    foreach ($File in $GeneratedFiles) {
        if (Test-Path $File) {
            Write-Host "> Remove-Item -LiteralPath $File -Force"
            Remove-Item -LiteralPath $File -Force
        }
    }
}

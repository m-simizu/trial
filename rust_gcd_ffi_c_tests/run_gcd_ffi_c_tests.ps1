$ErrorActionPreference = "Stop"

# rustup で入れた rustc.exe を、この PowerShell セッションの PATH に追加します。
# すでに PATH に rustc がある環境でも、この行はそのまま実行できます。
$env:PATH = "$env:USERPROFILE\.cargo\bin;$env:PATH"

$ObjectFile = "gcd.o"
$Tests = @(
    "c_test_gcd_common_factor",
    "c_test_gcd_coprime",
    "c_test_gcd_argument_order"
)

$GeneratedFiles = @($ObjectFile)
foreach ($Test in $Tests) {
    $GeneratedFiles += "$Test.exe"
}

try {
    # Rust の gcd.rs を、C のリンカに渡せるオブジェクトファイル gcd.o に変換します。
    Write-Host "`n[BUILD] Rust source -> object file" -ForegroundColor Cyan
    Write-Host "> rustc +stable-x86_64-pc-windows-gnu --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort gcd.rs -o $ObjectFile" -ForegroundColor DarkGray
    rustc +stable-x86_64-pc-windows-gnu --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort gcd.rs -o $ObjectFile
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    # C の各テストファイルと Rust 由来の gcd.o をリンクし、実行ファイルを作ります。
    Write-Host "`n[BUILD] C test sources -> executables" -ForegroundColor Cyan
    foreach ($Test in $Tests) {
        Write-Host "> gcc $Test.c $ObjectFile -o $Test.exe" -ForegroundColor DarkGray
        gcc "$Test.c" $ObjectFile -o "$Test.exe"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    # 作成した 3 つの C テスト実行ファイルを順に実行します。
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

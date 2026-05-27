# Rust FFI null pointer sample

`NULL` を引数に渡すCコードを、Cテストから検証するサンプルです。

同じCテストファイルを使って、移植前のC実装と移植後のRust実装を別々に確認できます。

## 実行方法

C実装だけをテストします。

```powershell
.\run_null_pointer_tests.ps1
```

Rust実装を、同じCテストファイルからテストします。

```powershell
.\run_null_pointer_rust_tests.ps1
```

どちらのスクリプトも、生成した `.o` と `.exe` を実行後に自動削除します。

# Rust FFI gcd sample

Rust で実装した最大公約数関数 `gcd` を C のテストプログラムから呼び出すサンプルです。

## ファイル構成

- `gcd.rs`: Rust で書いた最大公約数の実装です。
- `gcd.h`: C 側が参照する関数宣言です。
- `c_test_gcd_common_factor.c`: `gcd(48, 18) == 6` を検証します。
- `c_test_gcd_coprime.c`: `gcd(35, 64) == 1` を検証します。
- `c_test_gcd_argument_order.c`: `gcd(192, 270) == 6` を検証します。
- `run_gcd_ffi_c_tests.ps1`: Windows PowerShell 用のビルド・テスト一括実行スクリプトです。
- `Makefile`: `make` がある環境向けのビルド定義です。

## 実行方法

Windows PowerShell では、作業ディレクトリで次を実行します。

```powershell
.\run_gcd_ffi_c_tests.ps1
```

このスクリプトは次の順で動きます。

1. `rustc +stable-x86_64-pc-windows-gnu --emit=obj --crate-type=lib -C opt-level=2 -C panic=abort gcd.rs -o gcd.o`
   - `gcd.rs` を Rust のオブジェクトファイル `gcd.o` にコンパイルします。
   - `--emit=obj` は、最終実行ファイルではなく C リンカに渡せるオブジェクトファイルを出力する指定です。
   - `--crate-type=lib` は、Rust のライブラリとしてコンパイルする指定です。
   - `-C opt-level=2` は最適化を有効にします。この例では、到達不能なゼロ除算 panic 経路を消すためにも必要です。
   - `-C panic=abort` は panic 時の unwind ランタイムを使わない指定です。C 側リンクを単純にするために入れています。
2. `gcc c_test_gcd_common_factor.c gcd.o -o c_test_gcd_common_factor.exe`
   - C のテストコードと Rust 由来の `gcd.o` をリンクし、テスト実行ファイルを作ります。
3. 残り 2 つの C テストも同様にコンパイルします。
4. 3 つの `.exe` を実行し、C の `assert` で結果を検証します。

成功すると次のような出力になります。

```text
c_test_gcd_common_factor: gcd(48, 18) = 6
c_test_gcd_coprime: gcd(35, 64) = 1
c_test_gcd_argument_order: gcd(192, 270) = 6
```

`make` がある環境なら、次でも同じ処理を実行できます。

```sh
make test
```

## FFI の仕組み

Rust 側の関数は次の形で定義しています。

```rust
#[no_mangle]
pub extern "C" fn gcd(a: u64, b: u64) -> u64
```

`extern "C"` は、この関数を C の呼び出し規約で呼べるようにする指定です。Rust 独自の ABI ではなく C ABI に合わせることで、C から普通の関数のように呼び出せます。

`#[no_mangle]` は、コンパイル後のシンボル名を Rust 独自の長い名前に変換せず、`gcd` のまま公開する指定です。これにより、C 側の `uint64_t gcd(uint64_t a, uint64_t b);` という宣言とリンク時に名前が一致します。

C 側では `gcd.h` に次の宣言を書いています。

```c
uint64_t gcd(uint64_t a, uint64_t b);
```

Rust の `u64` と C の `uint64_t` はどちらも 64 bit の符号なし整数なので、FFI 境界で型の幅が一致します。

## 補足

参考記事では `cdylib` として共有ライブラリを作る方法が紹介されています。この環境では TDM-GCC に Rust GNU DLL リンクで必要な `libgcc_eh` がなく、DLL 生成が失敗しました。そのため、今回は `--emit=obj` で Rust のオブジェクトファイルを作り、C のテストに直接リンクしています。

共有ライブラリ方式にする場合の基本は同じで、Rust 側は `#[no_mangle]` と `pub extern "C"` を使い、`cdylib` としてビルドした成果物を C 側でリンクします。

## 参考文献

- https://zenn.dev/forcia_tech/articles/20211201_advent_calendar
- https://doc.rust-lang.org/nomicon/ffi.html
- https://doc.rust-lang.org/reference/linkage.html
- https://rust-lang.github.io/rustup/installation/windows.html

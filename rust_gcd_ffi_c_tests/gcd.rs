// Rust は通常、関数名をコンパイラ内部用に変換します。
// これを name mangling といいます。
// #[no_mangle] を付けることで、コンパイル後も関数名を gcd のまま残します。
// C 側は gcd という名前で探すので、これが必要です。
#[no_mangle]
// pub extern "C" fnは、
//「外部から見える、C の呼び出し規約に従う Rust 関数を定義する」
pub extern "C" fn gcd(a: u64, b: u64) -> u64 {
    let mut x = a; //(let は変数に値を束縛)
    let mut y = b; //let mutは後から変更可能

    while y != 0 {
        let r = x % y;
        x = y;
        y = r;
    }

    x
}

// まず #[...] は Rust の属性です。属性とは、直後の関数・モジュール・構造体などに追加の指示を与える書き方です。
// cfg は configuration の略です。
// 条件付きコンパイルを表します。
// 「ある条件のときだけ、このコードをコンパイルする」という意味です。
// test は Rust のテストビルド時に有効になる条件です。
// つまり #[cfg(test)] は、「テストとしてコンパイルするときだけ、この下のコードを含める」という意味になります。

// フルパスではなく、PATH から rustc を探す設定に切り替えます[cfg(test)] 以下は、Rust 単体でも一応 gcd の動作確認ができるように入れている補助的なテストです。
#[cfg(test)]
mod tests {
    use super::gcd;

    #[test]
    fn computes_gcd() {
        assert_eq!(gcd(48, 18), 6);
        assert_eq!(gcd(35, 64), 1);
        assert_eq!(gcd(270, 192), 6);
    }
}

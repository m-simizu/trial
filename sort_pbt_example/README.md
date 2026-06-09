# ソートプログラムのPBTサンプル

このフォルダは、PythonでProperty-Based Testingを実際に動かすための小さなサンプルです。
題材はソート関数で、通常の単体テストとHypothesisを使ったPBTテストを比較できるようにしています。

## 各ファイルの説明

- `sort_program.py`
  - テスト対象のソート関数を定義しています。
  - `insertion_sort()` は正しいソート実装です。
  - `buggy_unique_sort()` はPBTの反例発見を確認するため、意図的に重複要素を削除してしまうバグを入れた関数です。
  - `is_non_decreasing()` は、リストが昇順かどうかを判定する補助関数です。

- `tests/test_sort_unit.py`
  - 通常の単体テストを定義しています。
  - 人間が `[3, 1, 2]` や `[2, 1, 2, 1]` のような具体例を選び、期待される結果と一致するか確認します。
  - 少数の例を確認するため、単純で読みやすい一方、入力の網羅性は人間の選び方に依存します。

- `tests/test_sort_pbt.py`
  - Hypothesisを使ったPBTテストを定義しています。
  - 整数リストを自動生成し、ソート結果が満たすべき性質を確認します。
  - 確認している性質は、昇順であること、長さが変わらないこと、要素の個数が保たれること、Python標準の `sorted()` と一致することです。
  - `buggy_unique_sort()` のテストは `xfail` にしてあり、バグがあることを教材として示しつつ、通常のテスト実行全体は成功するようにしています。

- `requirements.txt`
  - このサンプルを実行するために必要なPythonパッケージを記述しています。
  - `pytest` はテスト実行用、`hypothesis` はPBT用です。

- `.gitignore`
  - 仮想環境やテストキャッシュなど、保存対象にしないファイルを指定しています。
  - `.venv/`, `__pycache__/`, `.pytest_cache/`, `.hypothesis/` を除外します。

- `.venv/`
  - このサンプル用に作成済みのPython仮想環境です。
  - `pytest` と `hypothesis` はこの環境にインストール済みです。

## 実行方法

```powershell
cd C:\Users\masoc\Documents\Codex\PBTtrial\sort_pbt_example
.\.venv\Scripts\python.exe -m pytest
```

`pytest.ini` で `-s` を指定しているため、Hypothesisが生成した各入力について、入力値・実際の結果・期待値・PASS/FAILが表示されます。

確認済みの実行結果は次の通りです。

```text
7 passed, 1 xfailed
```

`1 xfailed` は失敗ではありません。`buggy_unique_sort()` が重複を削除するバグを持つため、Hypothesisが反例を見つけられることを示す教材用テストです。

## PBTで確認している性質

このサンプルでは、正しいソート関数に対して次の性質を確認しています。

1. 出力は昇順である。
2. 出力の長さは入力と同じである。
3. 出力には入力と同じ要素が同じ個数だけ含まれる。
4. 出力はPython標準の `sorted()` と一致する。

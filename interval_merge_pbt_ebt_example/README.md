# 区間マージによるPBT・EBTサンプル

このフォルダは、区間マージ `merge_intervals` を対象にExample-Based Testing（EBT）とProperty-Based Testing（PBT）を比較し、後からmutation testingとSBFLを行うための題材です。

## SUTの概要

中心となる呼び出しは次の形です。

```python
merge_intervals([(1, 3), (2, 5), (10, 12)])
# [(1, 5), (10, 12)]
```

`interval_merger.py` は約100行で、次の処理を含みます。

1. 区間の形式・型・有限値・始点と終点の順序を検証する。
2. 区間を始点順に並べる。
3. 空入力を処理する。
4. 区間が離れていれば結果へ追加する。
5. 区間が完全に含まれていれば読み飛ばす。
6. 一部が重なれば終点を延長する。
7. 境界が接する区間を統合するか選択する。

## 入力による分岐の違い

| 入力 | 主に通る処理 |
|---|---|
| `[]` | 空入力の早期return |
| `[(1, 3), (2, 5)]` | 部分重複、終点の延長 |
| `[(1, 10), (3, 5)]` | 完全包含、`continue` |
| `[(1, 3), (3, 5)]` | 境界接触の判定 |
| `[(1, 2), (4, 5)]` | 非重複、結果への追加 |
| `[(3, 1)]` | 不正区間として例外 |

入力によって通る行・分岐が変わるため、テストごとのカバレッジと合否を用いるSBFLに適しています。

## 各ファイル

- `interval_merger.py`: 約100行のSUTです。
- `tests/test_interval_merge_ebt.py`: 代表的な具体例と不正入力を確認するEBTです。
- `tests/test_interval_merge_pbt.py`: Hypothesisで区間列を生成して性質を確認するPBTです。
- `requirements.txt`: pytest、Hypothesis、pytest-covを指定します。
- `pytest.ini`: 入力ごとの表示とテスト探索先を設定します。

## PBTで確認する性質

- 出力区間は始点順で、互いに重ならない。
- 入力と出力が覆う整数点の集合は同じである。
- マージ結果を再度マージしても結果が変わらない。
- 入力順を逆にしても結果が変わらない。
- 同じ区間を重複追加しても結果が変わらない。
- 終点と始点が接する2区間は1区間に統合される。

## セットアップ

```powershell
cd C:\Users\masoc\Documents\Codex\PBTtrial\interval_merge_pbt_ebt_example
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 実行コマンド

すべて実行:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

EBTのみ:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_interval_merge_ebt.py
```

PBTのみ:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_interval_merge_pbt.py
```

分岐カバレッジ:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=interval_merger --cov-branch --cov-report=term-missing
```

作成時点では、EBT 11件とPBT 6件の合計17件がすべて成功することを確認しています。

- EBTのみの行・分岐カバレッジ: 91%
- PBTのみの行・分岐カバレッジ: 77%

EBTとPBTはどちらも `merge_intervals()` とその内部処理だけを対象にしています。PBTは有効な整数区間を生成するため、入力エラーなどの分岐を通りません。この差を、後のmutation testingやSBFL分析で利用できます。

## ミュータント候補

画像にある境界バグは、次の条件を変更することで作れます。

```python
current.start <= last.end
# 変更例
current.start < last.end
```

この変更では `(1, 3)` と `(3, 5)` の結果だけが変わりやすく、境界値を含むEBT/PBTがミュータントを殺せるか比較できます。

ほかにも次の変更が候補になります。

- `current.end <= last.end` を `<` にする。
- 非重複時の `append` を削除する。
- 並べ替えキーの始点と終点を入れ替える。
- `start > end` を `start >= end` にする。

各ミュータントについてテストごとの通過行と合否を記録すれば、SBFLの `ef`, `ep`, `nf`, `np` を計算できます。

## SBFL結果表の作成

今回のミュータントでは、`interval_merger.py` の重複判定を手作業で変更します。

```python
# 正常版
overlaps = current.start <= last.end

# 変更後
overlaps = current.start < last.end  # ミュータント（<= を < に変更）
```

変更後、次のコマンドを実行します。

```powershell
.\.venv\Scripts\python.exe sbfl_analysis.py --label overlaps_less_than --formula ochiai
```

スクリプトはEBTとPBTを別々に実行し、pytestのテスト単位で行カバレッジと合否を記録します。疑惑値の既定式はOchiaiです。

結果は次のフォルダへ保存されます。

```text
sbfl_results/overlaps_less_than/
├─ ebt_test_results.json
├─ pbt_test_results.json
├─ ebt_line_sbfl.csv
├─ pbt_line_sbfl.csv
├─ ebt_ranked_sbfl.csv
├─ pbt_ranked_sbfl.csv
├─ ebt_sbfl.md
├─ pbt_sbfl.md
├─ ebt_pbt_comparison.csv
├─ ebt_pytest_output.txt
├─ pbt_pytest_output.txt
└─ summary.json
```

## SBFL結果の確認方法

この実験では、まず次の4種類のファイルを確認します。

1. `summary.json`: EBTとPBTの成功・失敗テスト数を確認する。
2. `ebt_sbfl.md` / `pbt_sbfl.md`: EBTとPBTについて、疑惑値が高い行から確認する。
3. `ebt_pbt_comparison.csv`: 同じSUT行の `ef`, `nf`, `ep`, `np` と疑惑値をEBT/PBTで比較する。
4. `ebt_pytest_output.txt` / `pbt_pytest_output.txt`: 失敗したテストや、Hypothesisが発見した反例を確認する。

次の順序で確認すると、実験結果を追いやすくなります。

```text
summary.json
    ↓
ebt_sbfl.md / pbt_sbfl.md
    ↓
ebt_pbt_comparison.csv
    ↓
ebt_pytest_output.txt / pbt_pytest_output.txt
```

その他のファイルには、次の役割があります。

- `ebt_line_sbfl.csv` / `pbt_line_sbfl.csv`: SUTの行番号順に並んだSBFL結果。
- `ebt_ranked_sbfl.csv` / `pbt_ranked_sbfl.csv`: 疑惑値の高い順に並んだSBFL結果。
- `ebt_test_results.json` / `pbt_test_results.json`: pytestの各テストの合否を記録した内部データ。
- `.coverage.ebt` / `.coverage.pbt`: 行カバレッジ計算用の内部データ。通常は直接開く必要はない。

結果フォルダをエクスプローラーで開く場合は、プロジェクトフォルダで次を実行します。

```powershell
explorer .\sbfl_results\overlaps_less_than
```

CSVファイルはExcelなどの表計算ソフトで開くと、列の比較や並べ替えがしやすくなります。

```powershell
Invoke-Item .\sbfl_results\overlaps_less_than\ebt_pbt_comparison.csv
```

MarkdownファイルはVS Codeで開き、`Ctrl+Shift+V` を押すと表としてプレビューできます。

```powershell
code .\sbfl_results\overlaps_less_than\ebt_sbfl.md
code .\sbfl_results\overlaps_less_than\pbt_sbfl.md
```

今回の分析では、ミュータントを仕込んだ重複判定行とその周辺が疑惑値ランキングの上位に現れるか、またEBTとPBTで疑惑値や順位にどのような差があるかを確認します。

各行について次の値が出力されます。

- `ef`: その行を実行した失敗テスト数
- `nf`: その行を実行しなかった失敗テスト数
- `ep`: その行を実行した成功テスト数
- `np`: その行を実行しなかった成功テスト数
- `suspiciousness`: 指定した計算式による疑惑値

疑惑値は次の式で計算します。

```text
Ochiai    = ef / sqrt((ef + nf) * (ef + ep))
Tarantula = (ef / (ef + nf))
             / ((ef / (ef + nf)) + (ep / (ep + np)))
Jaccard   = ef / (ef + nf + ep)
```

0除算になる場合、このプログラムでは疑惑値を `0.0` とします。結果を保存した後は、次の実験と混ざらないよう重複判定を正常版の `current.start <= last.end` に戻します。

別の計算式を使う場合は、次のいずれかを指定できます。

```powershell
.\.venv\Scripts\python.exe sbfl_analysis.py --label mutant_name --formula ochiai
.\.venv\Scripts\python.exe sbfl_analysis.py --label mutant_name --formula tarantula
.\.venv\Scripts\python.exe sbfl_analysis.py --label mutant_name --formula jaccard
```

注意: EBTのパラメータは1入力ごとに別テストとして測定されます。一方、Hypothesisが1つのPBT関数内で生成する複数入力は、pytest上では1つのテストとしてカバレッジが合算されます。

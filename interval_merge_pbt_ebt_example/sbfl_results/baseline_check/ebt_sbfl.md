# EBT SBFL結果

- 計算式: `ochiai`
- 成功テスト: 11
- 失敗テスト: 0

|順位|行|コード|ef|nf|ep|np|疑惑値|
|---:|---:|---|---:|---:|---:|---:|---:|
|1|2|`"""prepare→_coerce_interval→Intrvalクラス"""`|0|0|0|11|0.000000|
|1|9|`from collections.abc import Iterable, Sequence`|0|0|0|11|0.000000|
|1|10|`from dataclasses import dataclass`|0|0|0|11|0.000000|
|1|13|`import math`|0|0|0|11|0.000000|
|1|16|`Number = int \| float`|0|0|0|11|0.000000|
|1|26|`@dataclass(frozen=True, order=True)`|0|0|0|11|0.000000|
|1|27|`class Interval:`|0|0|0|11|0.000000|
|1|30|`start: Number`|0|0|0|11|0.000000|
|1|31|`end: Number`|0|0|0|11|0.000000|
|1|34|`def as_tuple(self) -> tuple[Number, Number]:`|0|0|0|11|0.000000|
|1|36|`return (self.start, self.end)`|0|0|6|5|0.000000|
|1|39|`def _is_number(value: object) -> bool:`|0|0|0|11|0.000000|
|1|41|`return isinstance(value, (int, float)) and not isinstance(value, bool)`|0|0|9|2|0.000000|
|1|45|`"""1件の入力を検証し、Intervalへ変換する。"""`|0|0|0|11|0.000000|
|1|46|`def _coerce_interval(raw: object, index: int) -> Interval:`|0|0|0|11|0.000000|
|1|47|`if isinstance(raw, Interval):#すでにインターバル型のとき(ex)入力値:Interval(1,3)`|0|0|10|1|0.000000|
|1|48|`start = raw.start`|0|0|0|11|0.000000|
|1|49|`end = raw.end`|0|0|0|11|0.000000|
|1|51|`if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):`|0|0|10|1|0.000000|
|1|52|`raise TypeError(f"intervals[{index}]は2要素の配列で指定してください")`|0|0|0|11|0.000000|
|1|54|`if len(raw) != 2:`|0|0|10|1|0.000000|
|1|55|`raise ValueError(f"intervals[{index}]は始点と終点の2要素が必要です")`|0|0|1|10|0.000000|
|1|57|`start = raw[0]`|0|0|9|2|0.000000|
|1|58|`end = raw[1]`|0|0|9|2|0.000000|
|1|60|`if not _is_number(start) or not _is_number(end):`|0|0|9|2|0.000000|
|1|61|`raise TypeError(f"intervals[{index}]の始点と終点は数値で指定してください")`|0|0|1|10|0.000000|
|1|63|`if not math.isfinite(start) or not math.isfinite(end):`|0|0|8|3|0.000000|
|1|64|`raise ValueError(f"intervals[{index}]に無限大やNaNは使用できません")`|0|0|1|10|0.000000|
|1|66|`if start > end:`|0|0|7|4|0.000000|
|1|67|`raise ValueError(f"intervals[{index}]の始点は終点以下である必要があります")`|0|0|1|10|0.000000|
|1|69|`return Interval(start, end)`|0|0|6|5|0.000000|
|1|71|`"""全区間を検証し、始点、終点の順に並べる。"""`|0|0|0|11|0.000000|
|1|73|`def _prepare_intervals(intervals: Iterable[object]) -> list[Interval]:`|0|0|0|11|0.000000|
|1|75|`if isinstance(intervals, (str, bytes)):`|0|0|11|0|0.000000|
|1|76|`raise TypeError("intervalsには区間の反復可能オブジェクトを指定してください")`|0|0|0|11|0.000000|
|1|78|`try:#関数への入力値intervals: Iterable[object]の中身を一つずつ取り出して,_coerce_intervalへと渡す`|0|0|11|0|0.000000|
|1|79|`prepared = [_coerce_interval(raw, index) for index, raw in enumerate(intervals)]`|0|0|11|0|0.000000|
|1|80|`except TypeError:`|0|0|4|7|0.000000|
|1|81|`raise`|0|0|1|10|0.000000|
|1|83|`prepared.sort(key=lambda interval: (interval.start, interval.end))`|0|0|7|4|0.000000|
|1|84|`return prepared`|0|0|7|4|0.000000|
|1|86|`"""重なる区間を統合し、始点順のタプルとして返す。`|0|0|0|11|0.000000|
|1|91|`def merge_intervals(`|0|0|0|11|0.000000|
|1|97|`prepared = _prepare_intervals(intervals)`|0|0|11|0|0.000000|
|1|99|`if not prepared:#入力された区間がないとき、空リストを返す`|0|0|7|4|0.000000|
|1|100|`return []`|0|0|1|10|0.000000|
|1|105|`merged: list[Interval] = [prepared[0]]`|0|0|6|5|0.000000|
|1|108|`for current in prepared[1:]:#2番目以降を順にみていく`|0|0|6|5|0.000000|
|1|109|`last = merged[-1]#直前の区間`|0|0|5|6|0.000000|
|1|112|`if merge_touching:#統合条件に端が接しているかどうかを考える`|0|0|5|6|0.000000|
|1|113|`overlaps = current.start <= last.end`|0|0|4|7|0.000000|
|1|115|`overlaps = current.start < last.end`|0|0|1|10|0.000000|
|1|117|`if not overlaps:`|0|0|5|6|0.000000|
|1|119|`merged.append(current)`|0|0|3|8|0.000000|
|1|120|`elif current.end <= last.end:`|0|0|3|8|0.000000|
|1|122|`continue`|0|0|1|10|0.000000|
|1|124|`merged[-1] = Interval(last.start, current.end)`|0|0|2|9|0.000000|
|1|126|`return [interval.as_tuple() for interval in merged]`|0|0|6|5|0.000000|

# PBT SBFL結果

- 計算式: `ochiai`
- 成功テスト: 3
- 失敗テスト: 3

|順位|行|コード|ef|nf|ep|np|疑惑値|
|---:|---:|---|---:|---:|---:|---:|---:|
|1|36|`return (self.start, self.end)`|3|0|3|0|0.707107|
|1|41|`return isinstance(value, (int, float)) and not isinstance(value, bool)`|3|0|3|0|0.707107|
|1|47|`if isinstance(raw, Interval):#すでにインターバル型のとき(ex)入力値:Interval(1,3)`|3|0|3|0|0.707107|
|1|51|`if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):`|3|0|3|0|0.707107|
|1|54|`if len(raw) != 2:`|3|0|3|0|0.707107|
|1|57|`start = raw[0]`|3|0|3|0|0.707107|
|1|58|`end = raw[1]`|3|0|3|0|0.707107|
|1|60|`if not _is_number(start) or not _is_number(end):`|3|0|3|0|0.707107|
|1|63|`if not math.isfinite(start) or not math.isfinite(end):`|3|0|3|0|0.707107|
|1|66|`if start > end:`|3|0|3|0|0.707107|
|1|69|`return Interval(start, end)`|3|0|3|0|0.707107|
|1|75|`if isinstance(intervals, (str, bytes)):`|3|0|3|0|0.707107|
|1|78|`try:#関数への入力値intervals: Iterable[object]の中身を一つずつ取り出して,_coerce_intervalへと渡す`|3|0|3|0|0.707107|
|1|79|`prepared = [_coerce_interval(raw, index) for index, raw in enumerate(intervals)]`|3|0|3|0|0.707107|
|1|83|`prepared.sort(key=lambda interval: (interval.start, interval.end))`|3|0|3|0|0.707107|
|1|84|`return prepared`|3|0|3|0|0.707107|
|1|98|`prepared = _prepare_intervals(intervals)`|3|0|3|0|0.707107|
|1|100|`if not prepared:#入力された区間がないとき、空リストを返す`|3|0|3|0|0.707107|
|1|106|`merged: list[Interval] = [prepared[0]]`|3|0|3|0|0.707107|
|1|109|`for current in prepared[1:]:#2番目以降を順にみていく`|3|0|3|0|0.707107|
|1|110|`last = merged[-1]#直前の区間`|3|0|3|0|0.707107|
|1|113|`if merge_touching:#統合条件に端が接しているかどうかを考える`|3|0|3|0|0.707107|
|1|114|`overlaps = current.start < last.end  # ミュータント（<= を < に変更）`|3|0|3|0|0.707107|
|1|118|`if not overlaps:`|3|0|3|0|0.707107|
|1|120|`merged.append(current)`|3|0|3|0|0.707107|
|1|127|`return [interval.as_tuple() for interval in merged]`|3|0|3|0|0.707107|
|27|121|`elif current.end <= last.end:`|2|1|3|0|0.516398|
|27|123|`continue`|2|1|3|0|0.516398|
|27|125|`merged[-1] = Interval(last.start, current.end)`|2|1|3|0|0.516398|
|30|101|`return []`|1|2|3|0|0.288675|
|31|2|`"""prepare→_coerce_interval→Intrvalクラス"""`|0|3|0|3|0.000000|
|31|9|`from collections.abc import Iterable, Sequence`|0|3|0|3|0.000000|
|31|10|`from dataclasses import dataclass`|0|3|0|3|0.000000|
|31|13|`import math`|0|3|0|3|0.000000|
|31|16|`Number = int \| float`|0|3|0|3|0.000000|
|31|26|`@dataclass(frozen=True, order=True)`|0|3|0|3|0.000000|
|31|27|`class Interval:`|0|3|0|3|0.000000|
|31|30|`start: Number`|0|3|0|3|0.000000|
|31|31|`end: Number`|0|3|0|3|0.000000|
|31|34|`def as_tuple(self) -> tuple[Number, Number]:`|0|3|0|3|0.000000|
|31|39|`def _is_number(value: object) -> bool:`|0|3|0|3|0.000000|
|31|45|`"""1件の入力を検証し、Intervalへ変換する。"""`|0|3|0|3|0.000000|
|31|46|`def _coerce_interval(raw: object, index: int) -> Interval:`|0|3|0|3|0.000000|
|31|48|`start = raw.start`|0|3|0|3|0.000000|
|31|49|`end = raw.end`|0|3|0|3|0.000000|
|31|52|`raise TypeError(f"intervals[{index}]は2要素の配列で指定してください")`|0|3|0|3|0.000000|
|31|55|`raise ValueError(f"intervals[{index}]は始点と終点の2要素が必要です")`|0|3|0|3|0.000000|
|31|61|`raise TypeError(f"intervals[{index}]の始点と終点は数値で指定してください")`|0|3|0|3|0.000000|
|31|64|`raise ValueError(f"intervals[{index}]に無限大やNaNは使用できません")`|0|3|0|3|0.000000|
|31|67|`raise ValueError(f"intervals[{index}]の始点は終点以下である必要があります")`|0|3|0|3|0.000000|
|31|71|`"""全区間を検証し、始点、終点の順に並べる。"""`|0|3|0|3|0.000000|
|31|73|`def _prepare_intervals(intervals: Iterable[object]) -> list[Interval]:`|0|3|0|3|0.000000|
|31|76|`raise TypeError("intervalsには区間の反復可能オブジェクトを指定してください")`|0|3|0|3|0.000000|
|31|80|`except TypeError:`|0|3|0|3|0.000000|
|31|81|`raise`|0|3|0|3|0.000000|
|31|86|`"""重なる区間を統合し、始点順のタプルとして返す。`|0|3|0|3|0.000000|
|31|91|`def merge_intervals(`|0|3|0|3|0.000000|
|31|116|`overlaps = current.start < last.end`|0|3|0|3|0.000000|

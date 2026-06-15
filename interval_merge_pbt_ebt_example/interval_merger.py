"""区間マージを題材にした、分岐を含むEBT/PBT用SUT。"""
"""prepare→_coerce_interval→Intrvalクラス"""
# Iterable と Sequence を使うための import です。

# Iterable: for文で回せるもの
# 例: list, tuple, set
# Sequence: 順番があり、len() や raw[0] が使えるもの
# 例: list, tuple
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

# math.isfinite() を使って、数値が有限かどうかを確認します。
import math

# Number という型名を定義
Number = int | float

# frozen=True: 作成後に値を変更できない, 
# order=True: 区間同士を比較可能にする
# dataclass: 初期化処理や比較処理を自動生成する

#Interval クラスを dataclass として定義します
#Interval型のデータを生成する関数

#dataclass はデータを入れるためのクラスを簡単に作る機能
@dataclass(frozen=True, order=True)
class Interval:
    """始点と終点を持つ、変更不能な区間。"""

    start: Number
    end: Number

    # Interval をタプル (start, end) に変換するメソッドを定義。
    def as_tuple(self) -> tuple[Number, Number]:
        """外部向けのタプル表現を返す。"""
        return (self.start, self.end)

# 入力値が数値(int, float)であることを確認する関数
def _is_number(value: object) -> bool:
    """boolを除くintまたはfloatならTrueを返す。"""
    return isinstance(value, (int, float)) and not isinstance(value, bool)
# isinstanceは片方だけでよくないか？boolはintの一種

# indexは入力された区間リストのうち、ある区間がリストの何番目かを示す
"""1件の入力を検証し、Intervalへ変換する。"""
def _coerce_interval(raw: object, index: int) -> Interval:
    if isinstance(raw, Interval):#すでにインターバル型のとき(ex)入力値:Interval(1,3)
        start = raw.start
        end = raw.end
    else:#配列のような型ではないか、もしくはstr/bytesであるとき（配列のような連続する型)は、エラー
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
            raise TypeError(f"intervals[{index}]は2要素の配列で指定してください")
        #入力の配列やタプルが2つのみのとき
        if len(raw) != 2:
            raise ValueError(f"intervals[{index}]は始点と終点の2要素が必要です")
        #データの型を満たすとき
        start = raw[0]
        end = raw[1]
    #各区間の端が数値で表記されているかどうか
    if not _is_number(start) or not _is_number(end):
        raise TypeError(f"intervals[{index}]の始点と終点は数値で指定してください")
    #数値の値が有効なものか？(例：無限大や NaN)
    if not math.isfinite(start) or not math.isfinite(end):
        raise ValueError(f"intervals[{index}]に無限大やNaNは使用できません")
    #左端の数値が、右端より大きくないかチェック
    if start > end:
        raise ValueError(f"intervals[{index}]の始点は終点以下である必要があります")

    return Interval(start, end)

"""全区間を検証し、始点、終点の順に並べる。"""
# 左端に近い(0に近い)始点で並べ、始点が同じなら終点で並べます。
def _prepare_intervals(intervals: Iterable[object]) -> list[Interval]:
    #intervals に文字列や bytesの場合にエラー
    if isinstance(intervals, (str, bytes)):
        raise TypeError("intervalsには区間の反復可能オブジェクトを指定してください")

    try:#関数への入力値intervals: Iterable[object]の中身を一つずつ取り出して,_coerce_intervalへと渡す
        prepared = [_coerce_interval(raw, index) for index, raw in enumerate(intervals)]
    except TypeError:
        raise
    #引数intervalを基に出力を返す
    prepared.sort(key=lambda interval: (interval.start, interval.end))
    return prepared

"""重なる区間を統合し、始点順のタプルとして返す。

    merge_touching=Trueでは(1, 3)と(3, 5)も統合する。
    Falseでは、正の長さで重なる場合だけ統合する。
    """
def merge_intervals(
    intervals: Iterable[object],
    *,#呼び出し側の意図を明確にするためです。
    #統合条件として、true:端が接しているとき,false:端が接していないとき
    merge_touching: bool = True,
) -> list[tuple[Number, Number]]:

    prepared = _prepare_intervals(intervals)

    if not prepared:#入力された区間がないとき、空リストを返す
        return []

    # 統合結果を入れるリスト merged を作ります。

    # 最初の区間を初期値として入れています。
    merged: list[Interval] = [prepared[0]]

    #2番目以降の区間を順番に見ていきます
    for current in prepared[1:]:#2番目以降を順にみていく
        last = merged[-1]#直前の区間

        #直前の区間の右端よりも、左側に現在の区間の左端が位置しているか？
        if merge_touching:#統合条件に端が接しているかどうかを考える
            overlaps = current.start < last.end  # ミュータント（<= を < に変更）
        else:
            overlaps = current.start < last.end

        if not overlaps:
            #統合できないとき
            merged.append(current)
        elif current.end <= last.end:
            #直前の区間に内包されているとき
            continue
        else:
            merged[-1] = Interval(last.start, current.end)

    return [interval.as_tuple() for interval in merged]

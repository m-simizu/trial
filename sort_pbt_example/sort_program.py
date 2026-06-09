"""PBTの題材として使う、小さなソート関数群。"""

# リストだけでなく、タプルなども受け取れる関数にするために使っている
from collections.abc import Iterable


def insertion_sort(values: Iterable[int]) -> list[int]:
    """入力と同じ要素を保ったまま、昇順に並べた新しいリストを返す関数。"""
    result: list[int] = []
    for value in values:
        index = 0
        while index < len(result) and result[index] <= value:
            index += 1
        result.insert(index, value)
    return result


def buggy_unique_sort(values: Iterable[int]) -> list[int]:
    """意図的にバグを入れたソート関数。重複要素を消してしまう。"""
    return sorted(set(values))


def is_non_decreasing(values: list[int]) -> bool:
    """リストが昇順、つまり各要素が次の要素以下ならTrueを返す関数。"""
    return all(left <= right for left, right in zip(values, values[1:]))

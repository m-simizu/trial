"""具体例を人間が指定して確認する、通常の単体テスト。"""

from sort_program import buggy_unique_sort, insertion_sort


def test_insertion_sort_simple_example():
    assert insertion_sort([3, 1, 2]) == [1, 2, 3]


def test_insertion_sort_with_duplicates():
    assert insertion_sort([2, 1, 2, 1]) == [1, 1, 2, 2]


def test_buggy_unique_sort_can_look_ok_on_distinct_values():
    assert buggy_unique_sort([3, 1, 2]) == [1, 2, 3]

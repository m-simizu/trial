"""代表入力を明示して確認するExample-Based Testing。"""

import pytest

from interval_merger import merge_intervals


@pytest.mark.parametrize(
    ("intervals", "expected"),
    [
        ([], []),
        ([(1, 3)], [(1, 3)]),
        ([(1, 3), (2, 5), (10, 12)], [(1, 5), (10, 12)]),
        ([(1, 10), (3, 5)], [(1, 10)]),
        ([(1, 3), (3, 5)], [(1, 5)]),
        ([(8, 10), (1, 2), (4, 6)], [(1, 2), (4, 6), (8, 10)]),
    ],
)#代表的な正常入力に対して、期待通りに区間がマージされるか
def test_merge_intervals_examples(intervals, expected):
    actual = merge_intervals(intervals)
    print(f"EBT: input={intervals!r} | actual={actual!r} | expected={expected!r}")
    assert actual == expected

#merge_touching=False のとき、接している区間を分離したままにできるか
def test_touching_intervals_can_be_kept_separate():
    assert merge_intervals([(1, 3), (3, 5)], merge_touching=False) == [(1, 3), (3, 5)]

#不正入力に対して適切に例外が出るか
@pytest.mark.parametrize(
    "invalid",
    [
        [(3, 1)],
        [(1,)],
        [(1, "2")],
        [(1, float("inf"))],
    ],
)
def test_invalid_intervals_raise_error(invalid):
    with pytest.raises((TypeError, ValueError)):
        merge_intervals(invalid)

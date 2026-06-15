"""Hypothesisが区間列を生成して性質を確認するProperty-Based Testing。"""

from hypothesis import given, settings, strategies as st

from interval_merger import merge_intervals


intervals = st.lists(
    st.tuples(
        st.integers(min_value=-50, max_value=50),
        st.integers(min_value=0, max_value=20),
    ).map(lambda pair: (pair[0], pair[0] + pair[1])),#必ず1つ目≦2つ目となる区間を作るため
    min_size=0,
    max_size=20,
)

def show_result(property_name, values, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {property_name} | input={values!r}")

#この関数は、区間が覆っている整数点の集合を返します。
def covered_integer_points(values):
    points = set()
    for start, end in values:
        points.update(range(start, end + 1))
    return points


@given(intervals)
@settings(max_examples=20)
def test_output_is_sorted_and_non_overlapping(values):
    result = merge_intervals(values)
    valid_intervals = all(start <= end for start, end in result)
    #このプログラムでは merge_touching=True がデフォルトなので、接している区間もマージされます。
    separated_intervals = all(left[1] < right[0] for left, right in zip(result, result[1:]))
    passed = valid_intervals and separated_intervals
    show_result("sorted and non-overlapping", values, passed)
    assert passed


@given(intervals)
@settings(max_examples=20)
def test_merging_preserves_covered_integer_points(values):#マージ後とマージ前で、覆っている整数点が同じかを確認しています
    result = merge_intervals(values)
    passed = covered_integer_points(result) == covered_integer_points(values)
    show_result("covered points are preserved", values, passed)
    assert passed


@given(intervals)
@settings(max_examples=20)
def test_merging_is_idempotent(values):#一度マージした結果は、もうマージする必要がない完成形になっているか
    once = merge_intervals(values)
    twice = merge_intervals(once)
    passed = twice == once
    show_result("idempotence", values, passed)
    assert passed


@given(intervals)
@settings(max_examples=20)
def test_input_order_does_not_change_result(values):#merge_intervals は一度マージ済みの入力に対して、結果を変えない
    result = merge_intervals(values)
    reversed_result = merge_intervals(reversed(values))
    passed = reversed_result == result
    show_result("input order invariance", values, passed)
    assert passed


@given(intervals)
@settings(max_examples=20)
def test_adding_duplicate_interval_does_not_change_result(values):#入力順序に依存しないことを確認しています。
    if not values:
        return

    result = merge_intervals(values)
    with_duplicate = merge_intervals(values + [values[0]])#入力を逆順にしてマージ
    passed = with_duplicate == result
    show_result("duplicate invariance", values, passed)
    assert passed


@given(
    start=st.integers(min_value=-50, max_value=50),
    left_length=st.integers(min_value=0, max_value=20),
    right_length=st.integers(min_value=0, max_value=20),
)
@settings(max_examples=20)
def test_touching_intervals_are_merged(start, left_length, right_length):#端が接している区間は1つにマージされる
    boundary = start + left_length
    values = [(start, boundary), (boundary, boundary + right_length)]
    result = merge_intervals(values)
    expected = [(start, boundary + right_length)]
    passed = result == expected
    show_result("touching intervals are merged", values, passed)
    assert passed

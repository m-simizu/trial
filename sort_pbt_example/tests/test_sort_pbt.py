"""Hypothesisで多数の入力を自動生成して確認するPBTテスト。"""

from collections import Counter

import pytest
from hypothesis import given, settings, strategies as st

from sort_program import buggy_unique_sort, insertion_sort, is_non_decreasing

# Hypothesisは完全な単純ランダムではありません。
# 空リスト、0、境界値、重複、短い例など、バグを見つけやすい値も優先的に試します。
# 失敗したら、その入力をより小さい反例へ縮小します。
int_lists = st.lists(
    st.integers(min_value=-100, max_value=100),
    min_size=0,
    max_size=50,
)

#結果表示用
def show_result(property_name, values, actual, expected, passed):
    status = "PASS" if passed else "FAIL"
    print(
        f"{status}: {property_name} | "
        f"input={values!r} | actual={actual!r} | expected={expected!r}"
    )

#昇順になっているか判定
@given(int_lists)
@settings(max_examples=10)
def test_insertion_sort_output_is_ordered(values):
    result = insertion_sort(values)
    passed = is_non_decreasing(result)
    show_result("output is ordered", values, result, "non-decreasing list", passed)
    assert passed

#要素数判定
@given(int_lists)
@settings(max_examples=10)
def test_insertion_sort_preserves_length(values):
    result = insertion_sort(values)
    passed = len(result) == len(values)
    show_result("length is preserved", values, len(result), len(values), passed)
    assert passed

#要素の種類ごとの数判定
@given(int_lists)
@settings(max_examples=10)
def test_insertion_sort_preserves_elements(values):
    result = insertion_sort(values)
    passed = Counter(result) == Counter(values)
    show_result("elements are preserved", values, Counter(result), Counter(values), passed)
    assert passed

#Python標準のsorted()と結果が一致するかを判定
@given(int_lists)
@settings(max_examples=10)
def test_insertion_sort_matches_python_sorted(values):
    result = insertion_sort(values)
    expected = sorted(values)
    passed = result == expected
    show_result("matches sorted()", values, result, expected, passed)
    assert passed

#バグを埋め込んだ関数の実行
#xfailにより失敗が期待されるテストとして扱う
@given(int_lists)
@settings(max_examples=10)
@pytest.mark.xfail(reason="buggy_unique_sort removes duplicates", strict=True)
def test_buggy_unique_sort_does_not_match_python_sorted(values):
    result = buggy_unique_sort(values)
    expected = sorted(values)
    passed = result == expected
    show_result("buggy sorter matches sorted()", values, result, expected, passed)
    assert passed

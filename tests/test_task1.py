import pytest

from task1.solution import strict


@strict
def sum_int(a: int, b: int) -> int:
    return a + b


@strict
def sum_int_float(a: int, b: float) -> float:
    return a + b


@strict
def sum_str(a: str, b: str) -> str:
    return a + b


@strict
def sum_bool(a: bool, b: bool) -> int:
    return a + b


@pytest.mark.parametrize(
    "func, arg1, arg2, expected_result",
    [
        (sum_int, 1, 2, 3),
        (sum_int_float, 1, 2.1, 3.1),
        (sum_str, "a", "b", "ab"),
        (sum_bool, True, True, 2),
        pytest.param(sum_int, 1, 2.4, None, marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(sum_int, True, 1, None, marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(sum_int_float, 1.1, 2, None, marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(sum_str, "1", 2, None, marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(sum_bool, True, 1, None, marks=pytest.mark.xfail(raises=TypeError)),
    ],
)
def test(func, arg1, arg2, expected_result):

    assert func(arg1, arg2) == expected_result

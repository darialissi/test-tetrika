import pytest

from task1.solution import strict


@strict
def sum_int(a: int, b: int, c: int) -> int:
    return a + b + c


@strict
def sum_int_float(a: int, b: float, c: float) -> float:
    return a + b + c


@strict
def sum_str(a: str, b: str, c: str) -> str:
    return a + b + c


@strict
def sum_bool(a: bool, b: bool) -> int:
    return a + b


@pytest.mark.parametrize(
    "func, args, kwargs, expected_result",
    [
        (sum_int, (1, 2, 3), {}, 6),
        (sum_int, (1,), {"c": 3, "b": 2}, 6),
        (sum_int_float, (1,), {"c": 1.1, "b": 2.1}, 4.2),
        (sum_str, ("a", "b", "c"), {}, "abc"),
        (sum_str, ("a"), {"c": "c", "b": "b"}, "abc"),
        (sum_bool, (), {"b": True, "a": True}, 2),
        pytest.param(sum_int_float, (1,), {"c": "1", "b": 2.1}, None, marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(sum_str, (), {"b": "1", "a": 1, "c": "c"}, None, marks=pytest.mark.xfail(raises=TypeError)),
        pytest.param(sum_bool, (1,), {"b": True}, None, marks=pytest.mark.xfail(raises=TypeError)),
    ],
)
def test_kwargs(func, args, kwargs, expected_result):

    assert func(*args, **kwargs) == expected_result

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
    "func, arg1, arg2, expected_result, mark",
    [
        (sum_int, 1, 2, 3, "answer"),
        (sum_int, 1, 2.4, TypeError, "error"),
        (sum_int, True, 1, TypeError, "error"),
        (sum_int_float, 1, 2.1, 3.1, "answer"),
        (sum_int_float, 1.1, 2, TypeError, "error"),
        (sum_str, "1", 2, TypeError, "error"),
        (sum_str, "a", "b", "ab", "answer"),
        (sum_bool, True, True, 2, "answer"),
        (sum_bool, True, 1, TypeError, "error"),
    ],
)
def test(func, arg1, arg2, expected_result, mark):

    match mark:
        case "answer":
            assert func(arg1, arg2) == expected_result

        case "error":
            with pytest.raises(Exception) as e:
                func(arg1, arg2)

            assert e.type is expected_result

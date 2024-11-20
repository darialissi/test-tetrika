from functools import wraps


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        types = list(func.__annotations__.values())
        args = list(args) + list(kwargs.values())

        for arg, t in zip(args, types):
            if not isinstance(arg, t):
                raise TypeError
            
        result = func(*args, **kwargs)
        return result
    
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
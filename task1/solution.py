from functools import wraps


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        types = list(func.__annotations__.values())
        args = list(args) + list(kwargs.values())

        for arg, t in zip(args, types):
            if type(arg) != t:
                raise TypeError

        result = func(*args, **kwargs)
        return result

    return wrapper

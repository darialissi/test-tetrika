from functools import wraps


def strict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        types: dict = func.__annotations__

        for arg, t in zip(args, types.values()):
            if type(arg) != t:
                raise TypeError

        for k, v in kwargs.items():
            if type(v) != types.get(k):
                raise TypeError

        result = func(*args, **kwargs)
        return result

    return wrapper

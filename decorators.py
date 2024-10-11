from functools import wraps
from log import save_log

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        save_log(f"Calling {func.__name__} {", ".join(map(str, args))}")
        result = func(*args, **kwargs)
        save_log(f"Returning {func.__name__}")
        return result
    return wrapper

def try_except(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error en la función '{func.__name__}': {str(e)}")
    
    return wrapper

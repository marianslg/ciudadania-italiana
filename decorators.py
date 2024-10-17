from functools import wraps

def log(func):
    from log import save_log

    @wraps(func)
    def wrapper(*args, **kwargs):
        # save_log(f"start {func.__name__} {", ".join(map(str, args))}")
        result = func(*args, **kwargs)
        # save_log(f"end {func.__name__}")
        return result
    return wrapper

def try_except(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise Exception(f"Error en la función '{func.__name__}' del tipo '{type(e)}': {str(e)}")
    
    return wrapper

def create_folder(foler_name):
    from log import create_folder_if_not_exists

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                create_folder_if_not_exists(foler_name)
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error en la función '{func.__name__}': {str(e)}")
        
        return wrapper
    return decorator

def create_folder_if_not_exists(folder_name):
    import os
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
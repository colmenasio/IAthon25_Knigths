import functools
import time

def retriable(max_tries, exception_to_catch: Exception):
    """Decorator that retries an operation up to a max amount of times if an exception of the type specified is caught.
    If the function it wraps excepts more times than allowed, returns None"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tries = 0
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except exception_to_catch as e:
                    tries += 1
                    if tries >= max_tries:
                        return None 
                    time.sleep(0.1)  
        return wrapper
    return decorator
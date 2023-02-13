from loguru import logger

def test_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Start test: {func.__name__}")
        res = func(*args, **kwargs)
        print(f"Finish test: {func.__name__}")
        return res
    return wrapper
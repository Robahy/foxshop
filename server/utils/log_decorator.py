import logging

logging.basicConfig(filename="/app.log",
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y/%m/%d - %I:%M:%S %p",
                    encoding="utf-8")
def log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.info(f"func: {func.__name__} | params: args:{args}, keywargs:{kwargs} | OUT: {result}")
        return result
    return wrapper
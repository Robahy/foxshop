import logging, os
logging.getLogger("watchfiles").setLevel(logging.WARNING)

LOG_PATH = os.path.join(os.path.dirname(__file__),'..', '..', '..', 'logs')

os.makedirs(LOG_PATH, exist_ok=True)
logging.basicConfig(filename= os.path.join(LOG_PATH, 'app.log'),
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y/%m/%d - %I:%M:%S %p",
                    encoding="utf-8")
def fastLog(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.info(f"func: {func.__name__} | params: args:{args}, keywargs:{kwargs} | OUT: {result}")
        return result
    return wrapper
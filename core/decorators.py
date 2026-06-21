from functools import wraps
import time
import logging

logger = logging.getLogger("app_logger")
logging.basicConfig(level=logging.INFO)


def simple_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()

        logger.info(f"START: {func.__name__}")

        try:
            result = func(*args, **kwargs)
            return result

        except Exception as e:
            logger.error(f"ERROR in {func.__name__}: {str(e)}")
            raise

        finally:
            logger.info(
                f"END: {func.__name__} | TIME: {time.time() - start:.4f}s"
            )

    return wrapper
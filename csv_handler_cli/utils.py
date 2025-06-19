import functools
import operator
import re
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set minimum log level
file_handler = logging.FileHandler(f"csv_handler_cli/app.log", mode="a", encoding="utf-8")
formatter = logging.Formatter(
   "{asctime} - {levelname} - {funcName} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

operator_map = {
    '=': operator.eq,
    '>': operator.gt,
    '<': operator.lt,
    'min': min,
    'max': max,
    'avg': lambda elements: sum(elements) / len(elements) if type(elements) == float else sum(elements) // len(elements)
}

prepare_args = lambda argumets: re.split(r'([<>=])', argumets)


def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(msg=f'{func.__name__} invoked with parameters positional arguments {args} '
                        f'and keyword arguments {kwargs}. Result = \n{result}')
        return result
    return wrapper

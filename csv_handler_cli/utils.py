import functools
import operator
import re
import logging
from conf import PROJECT_ROOT


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set minimum log level
file_handler = logging.FileHandler(f"{PROJECT_ROOT}/csv_handler_cli/app.log", mode="a", encoding="utf-8")
formatter = logging.Formatter(
   "{asctime} - {levelname} - {funcName} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
file_handler.setLevel(logging.DEBUG)
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

def recursively_sort_data(data: list, parameter) -> list:
    if len(data) < 1:
        return data
    median = data[len(data)//2]._asdict().get(parameter)
    less = [elem for elem in data if elem._asdict().get(parameter) < median]
    bigger = [elem for elem in data if elem._asdict().get(parameter) > median]
    equal = [elem for elem in data if elem._asdict().get(parameter) == median]
    return recursively_sort_data(bigger, parameter) + equal + recursively_sort_data(less, parameter)

def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(msg=f'{func.__name__} invoked with parameters positional arguments {args} '
                        f'and keyword arguments {kwargs}. Result = \n{result}')
        return result
    return wrapper

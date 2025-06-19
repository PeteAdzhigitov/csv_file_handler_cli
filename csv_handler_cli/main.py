import argparse
from argparse import Namespace
import csv
from collections import namedtuple
from tabulate import tabulate
import tabulate
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from csv_handler_cli.utils import operator_map, prepare_args, recursively_sort_data, logger
from csv_handler_cli.utils import logger_decorator
from typing import List

headers = None

@logger_decorator
def prepare_data(file_path: Path) -> List[namedtuple]:
    with open(file_path) as file:
        packed_data = []
        read_lines = csv.reader(file)
        # Csv file first line = headers
        global headers
        headers = next(read_lines)
        # Packing our csv lines into namedtuples for further easier work with attributes
        pack = namedtuple('Params', 'name, brand, price, rating')
        for line in read_lines:
            packed_data.append(pack(name=line[0], brand=line[1], price=int(line[2]), rating=float(line[3])))
        return packed_data

@logger_decorator
def sort_data(data: List[namedtuple], parser_arguments: Namespace) -> List[namedtuple]:
    if parser_arguments.where:
        name, _, _ = prepare_args(parser_arguments.where)
        if name in ['name', 'brand']:
            return sorted([elem for elem in data], key=lambda elem: elem.name)
        elif name in ['rating', 'price']:
            return recursively_sort_data(data, name)
    return data

@logger_decorator
def main_file_handler(data: List[namedtuple], parser_arguments: Namespace) -> list|List[list]:
    try:
        if parser_arguments.where:
            name, condition, value = prepare_args(parser_arguments.where)
            condition = operator_map.get(condition)
            if name == 'price':
                value = int(value)
            elif name == 'rating':
                value = float(value)
            return [elem for elem in data if condition(elem._asdict().get(name), value)]
        elif parser_arguments.aggregate:
            name, condition, value = prepare_args(parser_arguments.aggregate)
            condition = operator_map.get(value)
            return [[condition([elem._asdict().get(name) for elem in data])]]
        else:
            return [elem for elem in data]
    except ValueError as exs_info:
        logger.error(msg=exs_info)
        raise ValueError("Please check carefully your input parameters")

@logger_decorator
def order_by_and_pretify(sequence: list, parser_arguments: Namespace, headers: str|None) -> str:
    if parser_arguments.order_by:
        name, _ , value = prepare_args(parser_arguments.order_by)
        if value == 'desc':
            return tabulate.tabulate(sorted(sequence, key=lambda elem: elem._asdict().get(name))[::-1],
                                     headers, tablefmt="github")
        elif value == 'asc':
            return tabulate.tabulate(sorted(sequence, key=lambda elem: elem._asdict().get(name)),
                                     headers, tablefmt="github")
    else:
        if parser_arguments.aggregate:
            name, _, value = prepare_args(parser_arguments.aggregate)
            return tabulate.tabulate(sequence, [name], tablefmt="github")
        return tabulate.tabulate(sequence, headers, tablefmt="github")

@logger_decorator
def arguments_error_validation(parser_arguments: Namespace) -> None:
    try:
        if not parser_arguments.file:
            raise Exception('Please provide valid path to a csv file')
        if parser_arguments.aggregate and parser_arguments.where:
            raise Exception('Sorry, but right now you can only filter out lines or aggregate them.')
        if parser_arguments.aggregate:
            name, condition, value = prepare_args(parser_arguments.aggregate)
            if name not in ['price', 'rating'] or value not in ['avg', 'min', 'max']:
                raise Exception('Not acceptable operator or name by which you intend to aggregate.')
        if parser_arguments.where:
            name, condition, value = prepare_args(parser_arguments.where)
            if name not in ['price', 'rating'] and condition in ['>', '<']:
                raise Exception('You can not filer out string lines with operators gt, lt.')
        if parser_arguments.order_by:
            if parser_arguments.aggregate:
                raise Exception('Can\'t use order-by with aggregate flag.')
            name, _, value = prepare_args(parser_arguments.order_by)
            if name not in ['price', 'brand', 'rating', 'name'] or value not in ['desc', 'asc']:
                raise Exception('Typo in parameters input. Please check order-by flag parameters.')
    except ValueError as exc_info:
        logger.error(msg=exc_info)
        raise ValueError("Please check carefully your input parameters")
    except Exception as exc_info:
        logger.error(msg=exc_info)
        raise

def main():
    packed_data = prepare_data(csv_file_path)
    sorted_list = sort_data(packed_data, parser_arguments)
    output = main_file_handler(sorted_list, parser_arguments)
    print(order_by_and_pretify(output, parser_arguments, headers))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='csv_handler_cli',
                                     description='Csv files handler, with filtering and aggregation functionality.')

    parser.add_argument('--file', help='path to products csv file')
    parser.add_argument('--where', help='filter output out flag')
    parser.add_argument('--aggregate', help='aggregating price or rating flag')
    parser.add_argument('--order-by', help='ordering output by a field')
    parser_arguments = parser.parse_args()
    arguments_error_validation(parser_arguments)
    csv_file_path = Path(parser_arguments.file)
    main()

import argparse
from argparse import Namespace
import csv
from collections import namedtuple
from tabulate import tabulate
import tabulate
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from csv_handler_cli.utils import operator_map, prepare_args
from csv_handler_cli.utils import logger_decorator

headers = None

@logger_decorator
def main_file_handler(file_path, parser_arguments: Namespace) -> list:
    with open(file_path) as file:
        result = []
        read_lines = csv.reader(file)
        # Csv file first line = headers
        global headers
        headers = next(read_lines)
        # Packing our csv lines into namedtuples for further easier work with attributes
        pack = namedtuple('Params', 'name, brand, price, rating')
        for line in read_lines:
            result.append(pack(name=line[0], brand=line[1], price=int(line[2]), rating=float(line[3])))
        if parser_arguments.where:
            name, condition, value = prepare_args(parser_arguments.where)
            condition = operator_map.get(condition)
            if name == 'price':
                value = int(value)
            elif name == 'rating':
                value = float(value)
            return [elem for elem in result if condition(elem._asdict().get(name), value)]
        elif parser_arguments.aggregate:
            name, condition, value = prepare_args(parser_arguments.aggregate)
            condition = operator_map.get(value)
            return [[condition([elem._asdict().get(name) for elem in result])]]
        else:
            return [elem for elem in result]

def order_by_and_pretify(sequence: list, parser_arguments, headers) -> str:
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


def main():
    output = main_file_handler(csv_file_path, parser_arguments)
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
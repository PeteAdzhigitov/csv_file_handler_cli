import argparse
import csv
from argparse import ArgumentParser
import pytest


@pytest.fixture
def create_parser(request) -> ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='csv_handler_cli',
        description='Csv files handler with filtering and aggregation'
    )
    parser.add_argument('--file', help='path to products csv file')
    parser.add_argument('--where', help='filter condition')
    parser.add_argument('--aggregate', help='aggregation field')
    parser.add_argument('--order-by', help='sort field')
    return parser

@pytest.fixture
def receive_list_out_test_csv():
    def _receive_list_out_csv(path_to_test_csv_file) -> list:
        with open(path_to_test_csv_file) as file:
            read_file = csv.reader(file)
            next(read_file)
            result = [elem for elem in read_file]
            return result
    return _receive_list_out_csv

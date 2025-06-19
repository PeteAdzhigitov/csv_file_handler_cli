import random

import pytest
from conf import PROJECT_ROOT
from csv_handler_cli.main import main_file_handler, arguments_error_validation


class TestCSVHandler:

    def test_main_handler_returns_output_with_minimum_arguments(self, create_parser, receive_list_out_test_csv):
        # Receiving parser arguments
        parser_arguments = create_parser.parse_args(['--file', f'{PROJECT_ROOT}/tests/test_products.csv'])
        data = main_file_handler(parser_arguments.file, parser_arguments)
        random_element = random.choice(data)
        # Receiving list out of csv file forr further assertion
        test_csv_data = receive_list_out_test_csv(f'{PROJECT_ROOT}/tests/test_products.csv')
        test_csv_data_element = [elem for elem in test_csv_data if elem[0] == random_element.name][0]

        assert random_element.name == test_csv_data_element[0]
        assert random_element.brand == test_csv_data_element[1]
        assert random_element.price == int(test_csv_data_element[2])
        assert random_element.rating == float(test_csv_data_element[3])

    def test_main_handler_returns_error_if_not_existing_path_provided(self, create_parser):
        # Receiving parser arguments
        parser_arguments = create_parser.parse_args(['--file', "not_existing_path"])
        with pytest.raises(FileNotFoundError) as exc_info:
            main_file_handler(parser_arguments.file, parser_arguments)
        assert exc_info.type == FileNotFoundError

    def test_error_validator_returns_error_when_bjth_arguments_are_passed(self, create_parser):
        parser_arguments = create_parser.parse_args(['--file', f'{PROJECT_ROOT}/tests/test_products.csv', '--where', 'brand=apple', '--aggregate', 'rating=min'])
        with pytest.raises(Exception) as exc_info:
            arguments_error_validation(parser_arguments)
        assert exc_info.type == Exception

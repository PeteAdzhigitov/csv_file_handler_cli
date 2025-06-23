import random
import allure
import pytest
from conf import PROJECT_ROOT
from csv_handler_cli.main import prepare_data, arguments_error_validation, sort_data, main_file_handler


class TestCSVHandler:

    @pytest.mark.parametrize('additional_args', [['--where', 'price>1'], ['--where', 'rating>1'],
                                                 ['--aggregate', 'rating=min'],['--aggregate', 'price=avg']])
    def test_main_handler_return_correct_data_type(self, create_parser, additional_args):
        list_of_arguemnts = ['--file', f'{PROJECT_ROOT}/tests/test_products.csv']
        list_of_arguemnts.extend(additional_args)
        parser_arguments = create_parser.parse_args(list_of_arguemnts)
        data = prepare_data(parser_arguments.file)
        result = main_file_handler(data, parser_arguments)
        if parser_arguments.where:
            assert type(result) == list
        else:
            assert all(isinstance(sublist, list) for sublist in result)

    @pytest.mark.parametrize('not_valid_args', [['--where', 'price!100'], ['--where', 'rating^100'],
                                                ['--where', 'price-100'], ['--where', 'price 100']])
    def test_exception_when_not_valid_operator_passed(self, create_parser, not_valid_args):
        list_of_arguemnts = ['--file', f'{PROJECT_ROOT}/tests/test_products.csv']
        list_of_arguemnts.extend(not_valid_args)
        parser_arguments = create_parser.parse_args(list_of_arguemnts)
        data = prepare_data(parser_arguments.file)
        with pytest.raises(ValueError) as exc_info:
            sort_data(data, parser_arguments)

    def test_prepared_data_returns_named_tuple(self, create_parser):
        parser_arguments = create_parser.parse_args(['--file', f'{PROJECT_ROOT}/tests/test_products.csv'])
        data = prepare_data(parser_arguments.file)
        data = random.choice(data)
        assert hasattr(data, '_fields')

    def test_prepare_data_returns_output_with_minimum_arguments(self, create_parser, receive_list_out_test_csv):
        with allure.step("Preparing test data"):
            # Receiving parser arguments
            parser_arguments = create_parser.parse_args(['--file', f'{PROJECT_ROOT}/tests/test_products.csv'])
            data = prepare_data(parser_arguments.file)
            random_element = random.choice(data)
        with allure.step("Receiving list of data for further assertion"):
            test_csv_data = receive_list_out_test_csv(f'{PROJECT_ROOT}/tests/test_products.csv')
            test_csv_data_element = [elem for elem in test_csv_data if elem[0] == random_element.name][0]

        assert random_element.name == test_csv_data_element[0]
        assert random_element.brand == test_csv_data_element[1]
        assert random_element.price == int(test_csv_data_element[2])
        assert random_element.rating == float(test_csv_data_element[3])

    def test_prepare_data_returns_error_if_not_existing_path_provided(self, create_parser):
        with allure.step("Preparing test data"):
            # Receiving parser arguments
            parser_arguments = create_parser.parse_args(['--file', "not_existing_path"])
        with allure.step("Invoke main test method and receive expected error"):
            with pytest.raises(FileNotFoundError) as exc_info:
                prepare_data(parser_arguments.file)
            assert exc_info.type == FileNotFoundError

    def test_error_validator_returns_error_when_both_arguments_are_passed(self, create_parser):
        with allure.step("Preparing test data"):
            parser_arguments = create_parser.parse_args(['--file', f'{PROJECT_ROOT}/tests/test_products.csv', '--where',
                                                     'brand=apple', '--aggregate', 'rating=min'])
        with allure.step("Passing by both main arguemnts where and aggregate and assertin the result"):
            with pytest.raises(Exception) as exc_info:
                arguments_error_validation(parser_arguments)
            assert exc_info.type == Exception

    @pytest.mark.parametrize('not_valid_args', [['--where', 'brand>apple'], ['--where', 'name<poco'],
                                                ['--aggregate', 'brand=avg'], ['--aggregate', 'name=min'],
                                                ['--aggregate', 'price=test'], ['--aggregate', 'rating=not_valid'],
                                                ['--aggregate', 'rating=not_valid', '--order-by', 'price=desc'],
                                                ['--order-by', 'priceless=desc'], ['--order-by', 'price=desckk']])
    def test_arguments_error_validator_raise_error_when_arguments_not_valid(self, create_parser, not_valid_args):
        list_of_arguemnts = ['--file', f'{PROJECT_ROOT}/tests/test_products.csv']
        list_of_arguemnts.extend(not_valid_args)
        parser_arguments = create_parser.parse_args(list_of_arguemnts)
        with pytest.raises(Exception):
            arguments_error_validation(parser_arguments)

Csv files handler, with filtering and aggregation functionality.

Prepare environment

Run command `poetry install`

Run tests

`poetry run pytest tests/csv_handler_test.py`

Examples of using:

python3 csv_handler_cli/main.py --file products.csv
python3 csv_handler_cli/main.py --file products.csv --where "price>100" 
python3 csv_handler_cli/main.py --file products.csv --aggregate "rating=avg" 

All available flags:

'--file'*, help='path to products csv file'
'--where', help='filter output out flag'
'--aggregate', help='aggregating price or rating flag'
'--order-by', help='ordering output by a field'

* - Obligatory flag 

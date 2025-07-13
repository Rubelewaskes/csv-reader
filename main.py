import argparse

from handler import CSVHandler

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="Путь к CSV-файлу", required=True)
parser.add_argument("--where", help="Фильтр: column=|<|>value")
parser.add_argument("--aggregate", help="Агрегация: column=avg|min|max")

args = parser.parse_args()

proc = CSVHandler()
columns, data = proc.read(args.file)
if args.where:
    data = proc.filt(args.where, data, columns)
if args.aggregate:
    data = proc.aggr(args.aggregate, data, columns)
proc.table_print(data)

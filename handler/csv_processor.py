from handler.modules import CSVReader, CSVFilter, CSVAggregator, CSVPrinter


class CSVHandler:
    """A coordinator class for reading, filtering, aggregating, and outputting CSV data."""

    def read(self, filepath) -> tuple[dict[str, type], list[dict[str, str|int|float]]]:
        """
        Reads a CSV file and returns column types and converted data.

        Args:
            filepath (str): The path to the CSV file.

        Returns:
            tuple: A dictionary with column types and a list of strings with specified types.
        """
        reader = CSVReader()
        return reader.read_file(filepath)

    def filt(self,
               condition_str: str,
               data: list[dict[str, str|int|float]],
               columns: dict[str, type]) -> list[dict[str, str|int|float]]:
        """
        Applies filtering to data based on a given condition.

        Args:
            condition_str (str): The string of the filtering condition.
            data (list): A list of dictionaries with data.
            columns (dict): Dictionary of column types.

        Returns:
            list: Filtered data.
        """
        filterer = CSVFilter()
        return filterer.filter_data(condition_str, data, columns)

    def aggr(self,
                  condition_str: str,
                  data: list[dict[str, str|int|float]],
                  columns: dict[str, type],
                  digits: int | None = None) -> list[dict[str, int|float]]:
        """
        Applies an aggregating function to the data.

        Args:
            condition_str (str): Aggregation condition.
            data (list): A list of dictionaries with data.
            columns (dict): Dictionary of column types.
            digits (int, optional): The number of decimal places for rounding.

        Returns:
            list: A list with a single dictionary containing the result of aggregation.
        """
        aggregator = CSVAggregator()
        return aggregator.aggregate_data(condition_str, data, columns, digits)

    def table_print(self, data: list[dict[str, str|int|float]]):
        """
        Outputs a data table to the console.

        Args:
            data (list): A list of dictionaries with data to display.
        """
        printer = CSVPrinter()
        printer.print_table(data)

from re import search
from statistics import mean


class CSVAggregator():
    """A class for performing aggregating operations on CSV numeric data."""

    pattern = r"^(?P<col>[a-zA-Z0-9а-яА-Я_ -]*)\s*=\s*(?P<func>max|min|avg)$"
    operations = {
                "min": min,
                "max": max,
                "avg": mean,
            }

    def aggregate_data(self,
                       condition_str: str,
                       data: list[dict[str, str|int|float]],
                       columns: dict[str, type],
                       digits: int | None) -> list[dict[str, int|float]]:
        """
        Performs aggregation of data for the specified column and operations.

        Args:
            condition_str (str): String of the aggregation condition.
            data (list): A list of rows with data.
            columns (dict): A dictionary with column names and types.
            digits (int | None): The number of decimal places to round the result.

        Returns:
            list: A list with a single dictionary containing the aggregation result.
        """
        if not condition_str:
            raise ValueError("Empty condition")

        condition = self._condition_formatting(condition_str)
        if self._correct_check(condition, columns):
            operator = self.operations[condition["func"]]
            values = []
            for item in data:
                values.append(item[condition["col"]])
            result = operator(values)

            if digits:
                result = round(result, digits)

            return [{condition["func"]: result}]

        raise ValueError("Incorrect aggregation condition", condition_str)

    def _condition_formatting(self, condition_str: str) -> dict[str, str]:
        """
        Parses the aggregation condition string and extracts the column name and function.

        Args:
            condition_str (str): A string with a condition.

        Returns:
            dict: A dictionary with the keys "func" and "col".
        """
        match = search(self.pattern, condition_str)
        if match:
            return {
                "func": match["func"],
                "col": match["col"]
            }

        raise ValueError("Incorrect aggregation condition:", condition_str)

    def _correct_check(self,
                       condition: dict[str, str],
                       columns: dict[str, type]) -> bool:
        """
        Checks that the column exists and its type is numeric.

        Args:
            condition (dict): The dictionary of the condition.
            columns (dict): A dictionary with the types of all columns.

        Returns:
            bool: True if the column exists and has a valid type.
        """
        col_type = columns.get(condition["col"])
        if col_type:
            if col_type is int or col_type is float:
                return True

            raise ValueError("Invalid column data type")

        raise ValueError("The condition specifies a non-existent column:", condition["col"])

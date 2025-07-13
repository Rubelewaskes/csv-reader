from operator import eq, gt, lt
from re import search


class CSVFilter():
    """A class for filtering CSV file data based on a condition."""

    pattern = r"^(?P<col>[a-zA-Z0-9а-яА-Я_ -]*)\s*(?P<sign>>|=|<)\s*(?P<condition>[a-zA-Z0-9а-яА-Я_ -]*|\d*[.]\d*)$"
    operations = {
                "=": eq,
                ">": gt,
                "<": lt,
            }

    def filter_data(self,
                    condition_str: str,
                    data: list[dict[str, str|int|float]],
                    columns: dict[str, type]) -> list[dict[str, str|int|float]]:
        """
        Filters the data according to the specified condition.

        Args:
            condition_str (str): Filtering condition.
            data (list): A list of table rows obtained from CSV.
            columns (dict): A dictionary with column types.

        Returns:
            list: Filtered strings as a dictionary list.
        """
        if not condition_str:
            raise ValueError("An empty condition")

        incor_condition = self._condition_formatting(condition_str)
        cor_condition = self._condition_correction(incor_condition, columns)

        operator = self.operations[cor_condition["sign"]]
        filtered = []

        for row in data:
            if operator(row[cor_condition["col"]], cor_condition["condition"]):
                filtered.append(row)

        return filtered

    def _condition_formatting(self, condition_str: str) -> dict[str, str]:
        """
        Parses the condition string into components: column, operator, value.

        Args:
            condition_str (str): The condition string (for example, "rating=5").

        Returns:
            dict: A dictionary with a split condition.
        """
        match = search(self.pattern, condition_str)
        if match:
            return {
                "col": match["col"],
                "sign": match["sign"],
                "condition": match["condition"]
            }

        raise ValueError("Incorrect filtering condition:", condition_str)

    def _condition_correction(self,
                              condition_inc: dict[str, str],
                              columns: dict[str, type]) -> dict[str, str|int|float]:
        """
        Sets the value from the condition to the type of the corresponding column.

        Args:
            condition_inc (dict): The condition after formatting (lines).
            columns (dict): A dictionary with column types.

        Returns:
            dict: A condition with the specified value type.
        """
        if columns.get(condition_inc["col"]):
            try:
                col_type = columns[condition_inc["col"]]
                return {
                    "col": condition_inc["col"],
                    "sign": condition_inc["sign"],
                    "condition": col_type(condition_inc["condition"])
                }
            except (ValueError, TypeError) as e:
                raise ValueError("The criterion contains an incorrect data type ") from e

        raise ValueError("The condition specifies a non-existent column:", condition_inc["col"])

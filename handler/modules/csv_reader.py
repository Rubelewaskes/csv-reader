import csv


class CSVReader():
    """A class for reading CSV files with definition and type conversion."""

    def read_file(self, filepath) -> tuple[dict[str, type], list[dict[str, str|int|float]]]:
        """
        Reads the CSV file, determines the data types on the first line, and lists the types in all lines.

        Args:
            filepath (str): The path to the CSV file.

        Returns:
            tuple:
                - dict[str, type]: A dictionary containing column names and their specific types.
                - list[dict[str, str | int | float]]: A list of strings with specified value types.
        """
        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                raw_data = list(reader)
        except FileNotFoundError as e:
            raise FileNotFoundError("File not found:", filepath) from e
        except Exception as e:
            raise RuntimeError("Error when opening the file:", filepath) from e

        if not raw_data:
            raise ValueError("The CSV file is empty or contains only headers")

        columns = self._detect_column_types(raw_data)
        data = self._convert_types(raw_data, columns)

        return columns, data

    def _detect_column_types(self, data: list[dict[str, str]]) -> dict[str, type]:
        """
        Defines the data type for each column by the first row.

        Args:
            data (list[dict[str, str]]): Data read from CSV as strings.

        Returns:
            dict[str, type]: Dictionary with types for each column (int, float, str).
        """
        types: dict[str, type] = {}
        if not data:
            return types

        first_row = data[0]
        for key, value in first_row.items():
            if value.isdigit():
                types[key] = int
            else:
                try:
                    float(value)
                    types[key] = float
                except ValueError:
                    types[key] = str
        return types

    def _convert_types(self,
                       data: list[dict[str, str]],
                       types: dict[str, type]) -> list[dict[str, str|int|float]]:
        """
        Converts the values in the rows to the types defined for the columns.

        Args:
            data (list[dict[str, str]]): CSV strings as dictionaries of strings.
            types (dict[str, type]): Data types for each column.

        Returns:
            list[dict[str, str|int|float]]: A list of strings with specified types.
        """
        converted = []
        for row in data:
            new_row = {
                key: types[key](value) if types[key] != str else value
                for key, value in row.items()
            }
            converted.append(new_row)
        return converted

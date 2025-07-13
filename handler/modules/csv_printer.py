from tabulate import tabulate


class CSVPrinter():
    """A class for outputting received data to the console"""

    def print_table(self, data: list[dict[str, str | int | float]]):
        """
        Outputs the received data to the console in the form of a table.

        Args:
            data (list): A list of rows with data.
        """
        if data:
            print(tabulate(data, headers="keys", tablefmt="grid"))
        else:
            print("There are no data")
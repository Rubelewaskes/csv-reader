import pytest
import tempfile
from handler.modules import CSVReader


def test_read_file_success():
    content = "name,price,rating\niphone,999,4.7\nsamsung,899,4.5\n"
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", newline="") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    reader = CSVReader()
    columns, data = reader.read_file(tmp_path)

    assert columns == {"name": str, "price": int, "rating": float}
    assert len(data) == 2
    assert data[0]["name"] == "iphone"
    assert data[0]["price"] == 999
    assert data[0]["rating"] == 4.7


def test_read_file_empty_raises():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", newline="") as tmp:
        tmp.write("")
        tmp_path = tmp.name

    reader = CSVReader()

    with pytest.raises(ValueError, match="The CSV file is empty"):
        reader.read_file(tmp_path)


def test_read_file_file_not_found():
    reader = CSVReader()
    with pytest.raises(FileNotFoundError):
        reader.read_file("nonexistent_file.csv")


def test_detect_column_types():
    data = [{"name": "product", "price": "100", "rating": "4.8"}]
    reader = CSVReader()
    result = reader._detect_column_types(data)
    assert result == {"name": str, "price": int, "rating": float}


def test_convert_types():
    data = [{"price": "100", "rating": "4.8", "name": "abc"}]
    types = {"price": int, "rating": float, "name": str}
    reader = CSVReader()
    result = reader._convert_types(data, types)
    assert result == [{"price": 100, "rating": 4.8, "name": "abc"}]
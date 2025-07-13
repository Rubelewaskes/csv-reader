import pytest
from handler.modules import CSVFilter


@pytest.fixture
def sample_data():
    return [
        {"name": "iPhone", "price": 999, "rating": 4.5},
        {"name": "Redmi", "price": 299, "rating": 4.2},
        {"name": "Galaxy", "price": 799, "rating": 4.6},
    ]


@pytest.fixture
def column_types():
    return {"name": str, "price": int, "rating": float}


def test_filter_eq_str(sample_data, column_types):
    result = CSVFilter().filter_data("name=Redmi", sample_data, column_types)
    assert len(result) == 1
    assert result[0]["name"] == "Redmi"


def test_filter_gt_int(sample_data, column_types):
    result = CSVFilter().filter_data("price>500", sample_data, column_types)
    assert len(result) == 2
    assert {row["name"] for row in result} == {"iPhone", "Galaxy"}


def test_filter_lt_float(sample_data, column_types):
    result = CSVFilter().filter_data("rating<4.5", sample_data, column_types)
    assert len(result) == 1
    assert result[0]["name"] == "Redmi"


def test_condition_formatting():
    result = CSVFilter()._condition_formatting("rating<4.5")
    assert result == {"col": "rating", "sign": "<", "condition": "4.5"}


def test_condition_correction(column_types):
    result = CSVFilter()._condition_correction({"col": "rating", "sign": "<", "condition": "4.5"}, column_types)
    assert result == {"col": "rating", "sign": "<", "condition": 4.5}


def test_filter_empty_condition_raises(sample_data, column_types):
    with pytest.raises(ValueError, match="An empty condition"):
        CSVFilter().filter_data("", sample_data, column_types)


def test_filter_invalid_column_raises(sample_data, column_types):
    with pytest.raises(ValueError, match="non-existent column"):
        CSVFilter().filter_data("model=Galaxy", sample_data, column_types)


def test_filter_invalid_format_raises(sample_data, column_types):
    with pytest.raises(ValueError, match="Incorrect filtering condition"):
        CSVFilter().filter_data("rating>=4.5", sample_data, column_types)


def test_filter_wrong_type_conversion(sample_data, column_types):
    with pytest.raises(ValueError, match="incorrect data type"):
        CSVFilter().filter_data("price=abc", sample_data, column_types)
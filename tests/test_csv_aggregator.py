import pytest
from handler.modules import CSVAggregator


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


def test_aggregate_avg_rating(sample_data, column_types):
    result = CSVAggregator().aggregate_data("rating=avg", sample_data, column_types, digits=2)
    assert result == [{"avg": 4.43}]


def test_aggregate_max_price(sample_data, column_types):
    result = CSVAggregator().aggregate_data("price=max", sample_data, column_types, None)
    assert result == [{"max": 999}]


def test_aggregate_min_rating(sample_data, column_types):
    result = CSVAggregator().aggregate_data("rating=min", sample_data, column_types, 1)
    assert result == [{"min": 4.2}]


def test_condition_formatting():
    result = CSVAggregator()._condition_formatting("rating=min")
    assert result == {"func":"min", "col": "rating"}


def test_condition_correction(column_types):
    result = CSVAggregator()._correct_check({"func":"min", "col": "rating"}, column_types)
    assert result


def test_aggregate_empty_condition_raises(sample_data, column_types):
    with pytest.raises(ValueError, match="Empty condition"):
        CSVAggregator().aggregate_data("", sample_data, column_types, None)


def test_aggregate_invalid_condition_raises(sample_data, column_types):
    with pytest.raises(ValueError, match="Incorrect aggregation condition"):
        CSVAggregator().aggregate_data("rating=>avg", sample_data, column_types, None)


def test_aggregate_nonexistent_column_raises(sample_data, column_types):
    with pytest.raises(ValueError, match="non-existent column"):
        CSVAggregator().aggregate_data("memory=max", sample_data, column_types, None)


def test_aggregate_invalid_column_type_raises():
    data = [{"name": "iPhone"}, {"name": "Samsung"}]
    columns = {"name": str}

    with pytest.raises(ValueError, match="Invalid column data type"):
        CSVAggregator().aggregate_data("name=avg", data, columns, None)
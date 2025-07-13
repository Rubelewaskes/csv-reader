import pytest
from handler import CSVHandler

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


def test_heandler_filter_and_aggregate(sample_data, column_types):
    handler = CSVHandler()
    filtered = handler.filt("price>300", sample_data, column_types)
    result = handler.aggr("rating=max", filtered, column_types, None)
    assert result == [{"max": 4.6}]
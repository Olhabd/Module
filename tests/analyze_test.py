from datetime import datetime
import pytest

from src.analyze_price import (
    read_price,
    product_filter,
    last_month_records,
    price_change,
)


@pytest.fixture
def sample_records():
    return [
        {"product_name": "Кава", "date": datetime(2024, 3, 1), "price": 150.0},
        {"product_name": "Кава", "date": datetime(2024, 3, 25), "price": 155.0},
        {"product_name": "Кава", "date": datetime(2024, 4, 5), "price": 160.0},
        {"product_name": "Чай", "date": datetime(2024, 3, 10), "price": 80.0},
        {"product_name": "Чай", "date": datetime(2024, 4, 1), "price": 85.0},
        {"product_name": "Сік", "date": datetime(2024, 3, 15), "price": 60.0},
        {"product_name": "Сік", "date": datetime(2024, 4, 10), "price": 65.0},
    ]


def test_product_filter(sample_records):
    result = product_filter(sample_records, "Кава")
    assert len(result) == 3


def test_last_month_records(sample_records):
    coffee_records = product_filter(sample_records, "Кава")
    result = last_month_records(coffee_records)
    assert len(result) == 2


def test_price_change(sample_records):
    coffee_records = product_filter(sample_records, "Кава")
    recent_records = last_month_records(coffee_records)
    result = price_change(recent_records)

    assert result["start_price"] == 155.0
    assert result["end_price"] == 160.0
    assert result["change"] == 5.0
    assert round(result["percent_change"], 2) == 3.23


def test_not_enough_data():
    records = [
        {"product_name": "Цукор", "date": datetime(2024, 4, 1), "price": 30.0}
    ]

    with pytest.raises(ValueError):
        price_change(records)
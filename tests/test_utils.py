from app.utils.formatting import (
    format_currency,
    format_number,
    format_percentage,
    format_category_name,
    format_payment_type,
)


def test_format_currency():
    assert format_currency(16008872.12) == "$16,008,872.12"


def test_format_number():
    assert format_number(5466) == "5,466"


def test_format_percentage():
    assert format_percentage(86.7234) == "86.72%"


def test_format_category_name():
    assert format_category_name("furniture_decor") == "Furniture Decor"


def test_format_payment_type():
    assert format_payment_type("credit_card") == "Credit Card"
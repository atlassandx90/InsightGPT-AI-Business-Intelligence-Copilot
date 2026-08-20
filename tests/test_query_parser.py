from app.llm.query_parser import parse_question


def test_parse_state():

    result = parse_question(
        "What is total revenue in Sao Paulo?"
    )

    assert result.intent == "total_revenue"
    assert result.state == "SP"


def test_parse_payment():

    result = parse_question(
        "Revenue for credit card payments"
    )

    assert result.intent == "total_revenue"
    assert result.payment_type == "credit_card"


def test_parse_category():

    result = parse_question(
        "Revenue for electronics category"
    )

    assert result.intent == "total_revenue"
    assert result.category == "eletronicos"


def test_parse_multiple_filters():

    result = parse_question(
        "Revenue in SP for credit card electronics"
    )

    assert result.intent == "total_revenue"
    assert result.state == "SP"
    assert result.payment_type == "credit_card"
    assert result.category == "eletronicos"
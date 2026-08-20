from app.llm.sql_generator import generate_sql


def test_revenue_sql():

    sql = generate_sql(
        "What is total revenue?"
    )

    assert "SUM" in sql.upper()


def test_orders_sql():

    sql = generate_sql(
        "How many orders?"
    )

    assert "COUNT" in sql.upper()
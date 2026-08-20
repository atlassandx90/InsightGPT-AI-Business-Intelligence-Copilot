from app.llm.sql_validator import validate_sql


def test_valid_select():

    sql = """
    SELECT *
    FROM payments
    """

    assert validate_sql(sql) is True


def test_drop_blocked():

    sql = """
    DROP TABLE payments
    """

    assert validate_sql(sql) is False


def test_delete_blocked():

    sql = """
    DELETE FROM payments
    """

    assert validate_sql(sql) is False


def test_update_blocked():

    sql = """
    UPDATE payments
    SET amount = 0
    """

    assert validate_sql(sql) is False
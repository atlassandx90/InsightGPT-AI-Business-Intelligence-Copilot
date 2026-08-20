from app.llm.copilot import copilot_engine
from app.llm.response_models import CopilotResponse


def test_total_revenue():
    result = copilot_engine("What is the total revenue?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.sql is not None


def test_total_orders():
    result = copilot_engine("How many orders are there?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.sql is not None


def test_average_order_value():
    result = copilot_engine("What is the average order value?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.sql is not None


def test_top_state():
    result = copilot_engine("What is the top state?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.sql is not None


def test_top_category():
    result = copilot_engine("What is the top category?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.sql is not None


def test_payment_type():
    result = copilot_engine("What is the most used payment type?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.sql is not None


def test_customer_rating():
    result = copilot_engine("What is the average customer rating?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.sql is not None


def test_revenue_forecast():
    result = copilot_engine("What is the revenue forecast?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.sql is not None


def test_revenue_trend():
    result = copilot_engine("What is the revenue trend?")

    assert isinstance(result, CopilotResponse)
    assert result.answer
    assert result.insight
    assert result.recommendation
    assert result.chart_metadata is not None


def test_empty_question():
    result = copilot_engine("")

    assert result == "Please provide a business question."
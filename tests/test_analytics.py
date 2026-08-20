from app.services.analytics import (
    get_kpis,
    get_monthly_sales,
    get_state_revenue,
    get_top_categories,
    get_payment_types,
    get_review_scores,
    get_revenue_forecast,
    get_dashboard_filters,
    get_ai_insights,
)


def test_get_kpis():
    data = get_kpis()

    assert isinstance(data, dict)
    assert "total_revenue" in data
    assert "total_orders" in data
    assert "average_order_value" in data
    assert "order_status" in data


def test_get_monthly_sales():
    data = get_monthly_sales()

    assert isinstance(data, list)

    if data:
        assert "month" in data[0]
        assert "revenue" in data[0]


def test_get_state_revenue():
    data = get_state_revenue()

    assert isinstance(data, list)

    if data:
        assert "state" in data[0]
        assert "revenue" in data[0]


def test_get_top_categories():
    data = get_top_categories()

    assert isinstance(data, list)

    if data:
        assert "category" in data[0]
        assert "revenue" in data[0]


def test_get_payment_types():
    data = get_payment_types()

    assert isinstance(data, list)

    if data:
        assert "payment_type" in data[0]
        assert "total_payments" in data[0]


def test_get_review_scores():
    data = get_review_scores()

    assert isinstance(data, dict)
    assert "average_rating" in data
    assert "ratings" in data


def test_get_revenue_forecast():
    data = get_revenue_forecast()

    assert isinstance(data, dict)
    assert "history" in data
    assert "forecast" in data


def test_get_dashboard_filters():
    data = get_dashboard_filters()

    assert isinstance(data, dict)
    assert "states" in data
    assert "categories" in data
    assert "payment_types" in data


def test_get_ai_insights():
    data = get_ai_insights()

    assert isinstance(data, dict)
    assert "revenue" in data
    assert "top_state" in data
    assert "top_category" in data
    assert "payment_type" in data
    assert "rating" in data
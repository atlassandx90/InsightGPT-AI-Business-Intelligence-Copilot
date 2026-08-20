from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to InsightGPT API"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "API Running"


def test_kpis():
    response = client.get("/kpis")

    assert response.status_code == 200

    data = response.json()

    assert "total_revenue" in data
    assert "total_orders" in data
    assert "average_order_value" in data


def test_monthly_sales():
    response = client.get("/sales/monthly")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_state_revenue():
    response = client.get("/sales/state")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_top_categories():
    response = client.get("/categories/top")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_payment_types():
    response = client.get("/payments/types")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_review_scores():
    response = client.get("/reviews/score")

    assert response.status_code == 200

    data = response.json()

    assert "average_rating" in data
    assert "ratings" in data


def test_revenue_forecast():
    response = client.get("/forecast/revenue")

    assert response.status_code == 200

    data = response.json()

    assert "history" in data
    assert "forecast" in data


def test_dashboard_filters():
    response = client.get("/filters")

    assert response.status_code == 200

    data = response.json()

    assert "states" in data
    assert "categories" in data
    assert "payment_types" in data


def test_insights():
    response = client.get("/insights")

    assert response.status_code == 200

    data = response.json()

    assert "revenue" in data
    assert "top_state" in data
    assert "top_category" in data


def test_ask_copilot():
    response = client.post(
        "/ask",
        json={"question": "What is the total revenue?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "Total revenue is" in data["answer"]


def test_copilot():
    response = client.get(
        "/copilot",
        params={"query": "What is the total revenue?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sql" in data
    assert "result" in data
    assert "insight" in data
    assert "recommendation" in data


def test_ask_without_question():
    response = client.post(
        "/ask",
        json={}
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Please provide a question."
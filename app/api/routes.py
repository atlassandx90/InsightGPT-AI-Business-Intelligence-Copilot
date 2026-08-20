from fastapi import APIRouter, Query
from app.llm.copilot import copilot_engine
from app.llm.response_models import CopilotResponse

from app.services.analytics import (
    get_kpis,
    get_monthly_sales,
    get_state_revenue,
    get_top_categories,
    get_payment_types,
    get_review_scores,
    get_revenue_forecast,
    get_dashboard_filters,
    get_ai_insights
)

router = APIRouter()


@router.get("/kpis")
def kpis(
    state: str = Query(None),
    category: str = Query(None),
    payment_type: str = Query(None)
):
    return get_kpis(state, category, payment_type)


@router.get("/health")
def health():
    return {"status": "API Running"}


@router.get("/sales/monthly")
def monthly_sales(
    state: str = Query(None),
    category: str = Query(None),
    payment_type: str = Query(None)
):
    return get_monthly_sales(state, category, payment_type)


@router.get("/sales/state")
def state_revenue(
    state: str = Query(None),
    category: str = Query(None),
    payment_type: str = Query(None)
):
    return get_state_revenue(state, category, payment_type)


@router.get("/categories/top")
def top_categories(
    state: str = Query(None),
    category: str = Query(None),
    payment_type: str = Query(None)
):
    return get_top_categories(state, category, payment_type)


@router.get("/payments/types")
def payment_types(
    state: str = Query(None),
    category: str = Query(None),
    payment_type: str = Query(None)
):
    return get_payment_types(state, category, payment_type)


@router.get("/reviews/score")
def review_score(
    state: str = Query(None),
    category: str = Query(None),
    payment_type: str = Query(None)
):
    return get_review_scores(state, category, payment_type)


@router.get("/forecast/revenue")
def revenue_forecast(
    state: str = Query(None),
    category: str = Query(None),
    payment_type: str = Query(None)
):
    return get_revenue_forecast(state, category, payment_type)


@router.get("/insights")
def insights(
    state: str = Query(None),
    category: str = Query(None),
    payment_type: str = Query(None)
):
    return get_ai_insights(state, category, payment_type)


@router.get("/filters")
def dashboard_filters():
    return get_dashboard_filters()

@router.post(
    "/ask",
    response_model=CopilotResponse
)
def ask_ai(payload: dict):

    question = payload.get("question")

    if not question:
        return CopilotResponse(
            answer="Please provide a question."
        )

    return copilot_engine(question)

@router.get(
    "/copilot",
    response_model=CopilotResponse
)
def copilot(query: str):
    return copilot_engine(query)
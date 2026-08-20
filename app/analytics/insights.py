from app.services.analytics import get_ai_insights


def generate_business_insights(
    state=None,
    category=None,
    payment_type=None
):

    data = get_ai_insights(
        state=state,
        category=category,
        payment_type=payment_type
    )

    recommendations = []

    if data["rating"] < 4:
        recommendations.append(
            "Customer satisfaction is below target. Review customer feedback and fulfillment quality."
        )

    if data["top_state"]:
        recommendations.append(
            f"Increase marketing investment in {data['top_state']} because it is the strongest revenue-generating state."
        )

    if data["top_category"]:
        recommendations.append(
            f"Expand inventory and promotions for {data['top_category']} because it is the highest-performing category."
        )

    data["recommendations"] = recommendations

    return data
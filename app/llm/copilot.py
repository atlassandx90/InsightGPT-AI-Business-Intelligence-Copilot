from app.services.analytics import (
    get_kpis,
    get_monthly_sales,
    get_state_revenue,
    get_top_categories,
    get_payment_types,
    get_review_scores,
    get_revenue_forecast,
)

from app.llm.query_parser import parse_question, GEMINI_CLIENT, GEMINI_MODEL
from app.llm.response_models import CopilotResponse
from app.llm.sql_generator import generate_sql
from app.llm.sql_validator import validate_sql

# ==========================================================
# GEMINI ANSWER GENERATOR
# ==========================================================

def generate_gemini_answer(
    question: str,
    business_result: str,
) -> str:
    """
    Use Gemini to turn a verified business result into
    a concise natural-language answer.

    Gemini does NOT calculate or modify business numbers.
    The analytics layer remains the source of truth.
    """

    if not GEMINI_CLIENT:
        return business_result

    prompt = f"""
You are a business intelligence assistant.

Answer the user's question using ONLY the verified
business result provided below.

Do not invent numbers.
Do not calculate different numbers.
Do not change dates, percentages, currencies, or metrics.
Do not introduce facts that are not present in the result.

Keep the answer concise and professional.

User question:
{question}

Verified business result:
{business_result}

Return only the final answer to the user.
"""

    try:
        response = GEMINI_CLIENT.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        answer = response.text

        if answer and answer.strip():
            return answer.strip()

    except Exception:
        pass

    # Safe fallback:
    # if Gemini fails, return the verified analytics result.
    return business_result

# ==========================================================
# COPILOT ENGINE
# ==========================================================

def _copilot_engine_raw(question: str):
    """
    Main business intelligence copilot.

    Flow:

        User question
            ↓
        query_parser.parse_question()
            ↓
        BusinessQuery
            ↓
        Analytics functions
            ↓
        Business answer

    Gemini/deterministic parsing is handled entirely by
    query_parser.py.

    This module is responsible only for:
        1. Receiving the question.
        2. Using the structured query.
        3. Calling the correct analytics function.
        4. Formatting the final answer.
    """

    # ------------------------------------------------------
    # EMPTY QUESTION
    # ------------------------------------------------------

    if not question or not question.strip():
        return "Please provide a business question."

    # ------------------------------------------------------
    # PARSE QUESTION
    # ------------------------------------------------------

    parsed = parse_question(question)

    print("QUESTION =", question)
    print("PARSED =", parsed)
    print("INTENT =", parsed.intent)
    print("STATE =", parsed.state)
    print("CATEGORY =", parsed.category)
    print("PAYMENT =", parsed.payment_type)

    generated_sql = generate_sql(question)

    if generated_sql:

       if not validate_sql(generated_sql):

          return CopilotResponse(
              answer="Unsafe SQL detected.",
              sql=generated_sql,
              insight="SQL validation failed.",
              recommendation="Use a read-only business query."
           )

    # ------------------------------------------------------
    # STRUCTURED QUERY
    # ------------------------------------------------------

    intent = parsed.intent
    state = parsed.state
    category = parsed.category
    payment = parsed.payment_type
    chart_metadata = None

    # ======================================================
    # REVENUE TREND
    # ======================================================

    if intent == "revenue_trend":

        data = get_monthly_sales(
            state,
            category,
            payment,
        )

        chart_metadata = {
            "chart_type": "line",
            "x": [row["month"] for row in data],
            "y": [float(row["revenue"]) for row in data],
            "title": "Monthly Revenue Trend"
        }

        if len(data) < 2:
            return (
                "Not enough data to analyze the revenue trend."
            )

        last = float(data[-1]["revenue"])
        previous = float(data[-2]["revenue"])

        if previous == 0:
            return (
                "Revenue trend cannot be calculated because "
                "the previous period revenue is zero."
            )

        change = ((last - previous) / previous) * 100

        if change > 10:

            insight = (
                f"Revenue increased by {change:.2f}% compared with the previous month."
            )

            recommendation = (
                "Scale high-performing campaigns and maintain inventory levels."
            )

        elif change > 0:

            insight = (
                f"Revenue grew moderately by {change:.2f}%."
            )

            recommendation = (
                "Identify top-performing products and accelerate growth."
            )

        elif change < -10:

            insight = (
                f"Revenue declined significantly by {abs(change):.2f}%."
            )

            recommendation = (
                "Investigate demand decline and customer retention issues."
            )

        else:

            insight = (
                f"Revenue decreased slightly by {abs(change):.2f}%."
            )

            recommendation = (
                "Monitor performance closely and optimize marketing spend."
            )

        return CopilotResponse(
            answer=f"Revenue changed by {change:.2f}% compared with the previous month.",
            sql=generated_sql,
            result=data,
            insight=insight,
            recommendation=recommendation,
            chart_metadata=chart_metadata
        )
    # ======================================================
    # TOTAL REVENUE
    # ======================================================

    elif intent == "total_revenue":

        data = get_kpis(
            state,
            category,
            payment,
        )

        revenue = float(
           data.get("total_revenue", 0)
        )

        if revenue >= 15000000:

           insight = (
               f"Revenue exceeded ${revenue:,.2f}, indicating strong business performance and healthy market demand."
            )

           recommendation = (
               "Focus on margin optimization, customer retention, and scaling high-performing product categories."
            )

        elif revenue >= 10000000:

           insight = (
               f"Revenue reached ${revenue:,.2f}, showing stable commercial performance across the business."
            )

           recommendation = (
               "Identify the highest-performing regions and categories for additional investment."
            )

        else:

           insight = (
               f"Revenue currently stands at ${revenue:,.2f}, indicating opportunities for growth."
            )

           recommendation = (
               "Increase customer acquisition efforts and improve conversion rates."
            )

        return CopilotResponse(
           answer=f"Total revenue is ${revenue:,.2f}.",
           sql=generated_sql,
           result=data,
           insight=insight,
           recommendation=recommendation,
           chart_metadata=chart_metadata
        )

    # ======================================================
    # ORDERS
    # ======================================================

    elif intent == "orders":

        data = get_kpis(
            state,
            category,
            payment,
        )

        orders = int(
            data.get("total_orders", 0)
        )

        if orders > 50000:

            insight = (
                "Order volume indicates strong customer demand."
            )

            recommendation = (
                "Ensure logistics capacity can support demand."
            )

        else:

            insight = (
               "Order volume has room for improvement."
            )

            recommendation = (
               "Run acquisition campaigns to increase orders."
            )

        return CopilotResponse(
            answer=f"Total orders are {orders:,}.",
            sql=generated_sql,
            result=data,
            insight=insight,
            recommendation=recommendation,
            chart_metadata=None
        )

    # ======================================================
    # AVERAGE ORDER VALUE
    # ======================================================

    elif intent == "aov":

        data = get_kpis(
            state,
            category,
            payment,
        )

        aov = float(
            data.get("average_order_value", 0)
        )


        insight = (
            f"Customers spend an average of ${aov:,.2f} per order."
        )

        recommendation = (
            "Use upselling, cross-selling, and product bundles to increase average order value."
        )

        return CopilotResponse(
            answer=f"Average order value is ${aov:,.2f}.",
            sql=generated_sql,
            result=data,
            insight=insight,
            recommendation=recommendation,
            chart_metadata=None
        )

    # ======================================================
    # STATE
    # ======================================================

    elif intent == "state":

        data = get_state_revenue(
            state,
            category,
            payment,
        )

        if not data:
            return "No state revenue data is available."

        top = data[0]

        top_revenue = float(top["revenue"])

        total_revenue = sum(
            float(row["revenue"])
            for row in data
        )

        share = (
            top_revenue / total_revenue
        ) * 100

        chart_metadata = {
            "chart_type": "bar",
            "x": [row["state"] for row in data[:10]],
            "y": [float(row["revenue"]) for row in data[:10]],
            "title": "Top States by Revenue"
        }
        return CopilotResponse(
            answer=f"Top performing state is {top['state']} with revenue ${float(top['revenue']):,.2f}.",
            sql=generated_sql,
            result=data,
            insight = (f"{top['state']} contributes "f"{share:.1f}% of revenue among top states."),
            recommendation = (f"Expand marketing and fulfillment "f"capacity in {top['state']}."),
            chart_metadata=chart_metadata
        )
        # ======================================================
    # CATEGORY
    # ======================================================

    elif intent == "category":

        data = get_top_categories(
            state,
            category,
            payment,
        )

        if not data:
            return CopilotResponse(
                answer="No category revenue data is available.",
                sql=generated_sql,
                result=[],
                insight="No product category revenue data was found.",
                recommendation="Check the available category data.",
                chart_metadata=None
            )

        # Keep top 5 categories
        top_categories = data[:5]

        chart_metadata = {
            "chart_type": "bar",
            "x": [
                str(row["category"])
                .replace("_", " ")
                .title()
                for row in top_categories
            ],
            "y": [
                float(row["revenue"])
                for row in top_categories
            ],
            "title": "Top 5 Product Categories by Revenue"
        }

        # Build readable answer
        category_lines = []

        for index, row in enumerate(top_categories, start=1):

            category_name = (
                str(row["category"])
                .replace("_", " ")
                .title()
            )

            revenue = float(row["revenue"])

            category_lines.append(
                f"{index}. {category_name}: ${revenue:,.2f}"
            )

        answer = (
            "Top 5 product categories by revenue:\n"
            + "\n".join(category_lines)
        )

        total_revenue = sum(
            float(row["revenue"])
            for row in top_categories
        )

        top_revenue = float(
            top_categories[0]["revenue"]
        )

        share = (
            top_revenue / total_revenue * 100
            if total_revenue > 0
            else 0
        )

        top_name = (
            str(top_categories[0]["category"])
            .replace("_", " ")
            .title()
        )

        insight = (
            f"{top_name} is the highest-revenue category among "
            f"the top 5 categories, contributing approximately "
            f"{share:.1f}% of their combined revenue."
        )

        recommendation = (
            f"Protect performance in {top_name} while evaluating "
            f"the remaining top categories for additional growth opportunities."
        )

        return CopilotResponse(
            answer=answer,
            sql=generated_sql,
            result=top_categories,
            insight=insight,
            recommendation=recommendation,
            chart_metadata=chart_metadata
        )

    # ======================================================
    # PAYMENT
    # ======================================================

    elif intent == "payment":

        data = get_payment_types(
            state,
            category,
            payment,
        )

        if not data:
            return "No payment data is available."

        top = data[0]

        total_payments = sum(
            int(row["total_payments"])
            for row in data
        )

        share = (
            int(top["total_payments"])
            / total_payments
        ) * 100

        chart_metadata = {
            "chart_type": "pie",
            "labels": [row["payment_type"] for row in data],
            "values": [int(row["total_payments"]) for row in data],
            "title": "Payment Distribution"
        }

        payment_name = (
            str(top["payment_type"])
            .replace("_", " ")
            .title()
        )

        return CopilotResponse(
           answer=(
              f"Most used payment type is {payment_name} "
              f"with {int(top['total_payments']):,} payments."
            ),
           sql=generated_sql,
           result=data,
           insight = (f"{payment_name} accounts for {share:.1f}% of all transactions, making it the dominant payment channel."),
           recommendation = (f"Optimize checkout performance, approval rates, and payment reliability for {payment_name} transactions."),
           chart_metadata=chart_metadata
        )

    # ======================================================
    # CUSTOMER RATING
    # ======================================================

    elif intent == "rating":

        data = get_review_scores(
            state,
            category,
            payment,
        )

        rating = float(
            data.get("average_rating", 0)
        )

        if rating >= 4.5:

            insight = (
               "Customer satisfaction is excellent."
            )

            recommendation = (
               "Maintain service quality and customer engagement."
            )

        elif rating >= 4:

            insight = (
               "Customer satisfaction is healthy."
            )

            recommendation = (
               "Focus on converting satisfied customers into repeat buyers."
            )

        else:

            insight = (
               "Customer satisfaction requires attention."
            )

            recommendation = (
               "Analyze review feedback and improve customer experience."
            )

        chart_metadata = {
            "chart_type": "gauge",
            "value": rating,
            "max": 5,
            "title": "Customer Rating"
        }

        return CopilotResponse(
           answer=f"Average customer rating is {rating:.2f}/5.",
           sql=generated_sql,
           result=data,
           insight=insight,
           recommendation=recommendation,
           chart_metadata=chart_metadata
        )
    # ======================================================
    # FORECAST
    # ======================================================

    elif intent == "forecast":

        data = get_revenue_forecast(
            state,
            category,
            payment,
        )

        if not data or not data.get("forecast"):
            return "No revenue forecast data is available."

        next_month = data["forecast"][0]

        forecast_revenue = float(
            next_month["revenue"]
        )

        current_revenue = float(
            data["history"][-1]["revenue"]
        )

        forecast_change = (
            (
                forecast_revenue
                - current_revenue
            )
            / current_revenue
        ) * 100

        if forecast_change > 15:

            insight = (
                f"Strong growth momentum is expected with projected revenue growth of {forecast_change:.2f}% next month."
            )

            recommendation = (
                "Increase inventory capacity and marketing readiness to capture additional demand."
            )

        elif forecast_change > 0:

            insight = (
                f"Moderate growth of {forecast_change:.2f}% is forecasted for next month."
            )

            recommendation = (
                "Maintain current growth initiatives and monitor top-performing categories."
            )

        else:

            insight = (
                f"Revenue is projected to decline by {abs(forecast_change):.2f}% next month."
            )

            recommendation = (
                "Review pricing, customer retention, and demand-generation strategies."
            )

        chart_metadata = {
            "chart_type": "line",
            "x": [row["month"] for row in data["forecast"]],
            "y": [float(row["revenue"]) for row in data["forecast"]],
            "title": "Revenue Forecast"
        }

        return CopilotResponse(
           answer=(
              f"Expected revenue for {next_month['month']} "
              f"is ${float(next_month['revenue']):,.2f}."
            ),
            sql=generated_sql,
            result=data,
            insight=insight,
            recommendation=recommendation,
            chart_metadata=chart_metadata
        )

    # ======================================================
    # UNKNOWN
    # ======================================================

    return CopilotResponse(
        answer=(
           "I cannot answer this question yet. "
           "Try asking about revenue, orders, AOV, "
           "states, categories, payments, ratings, or forecasts."
        ),
        sql=generated_sql,
        result=None,
        insight="Intent not recognized.",
        recommendation="Use one of the supported business questions."
    )


# ==========================================================
# PUBLIC COPILOT ENGINE
# ==========================================================

def copilot_engine(question: str):

    result = _copilot_engine_raw(question)

    if isinstance(result, CopilotResponse):

        result.answer = generate_gemini_answer(
            question,
            result.answer
        )
    return result
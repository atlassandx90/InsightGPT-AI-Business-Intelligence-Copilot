import pandas as pd
from sklearn.linear_model import LinearRegression

from sqlalchemy import text

from app.database.connection import engine
from app.analytics.filters import build_filters


def get_revenue_forecast(
    state=None,
    category=None,
    payment_type=None
):
    where_clause, params, join_clause = build_filters(
        state,
        category,
        payment_type
    )

    with engine.connect() as conn:

        result = conn.execute(
            text(f"""
                SELECT
                    TO_CHAR(
                        o.order_purchase_timestamp::timestamp,
                        'YYYY-MM'
                    ) AS month,

                    ROUND(
                        SUM(p.payment_value)::numeric,
                        2
                    ) AS revenue

                FROM orders o

                JOIN customers c
                    ON o.customer_id = c.customer_id

                JOIN payments p
                    ON o.order_id = p.order_id

                {join_clause}

                {where_clause}

                GROUP BY month

                ORDER BY month;
            """),
            params
        ).mappings().all()

    df = pd.DataFrame(result)

    if df.empty:
        return {
            "history": [],
            "forecast": []
        }

    df["month_index"] = range(len(df))

    X = df[["month_index"]]
    y = df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    history = df[["month", "revenue"]].copy()

    # Keep the existing project's approach:
    # exclude the last two months from displayed history.
    history = history.iloc[:-2]

    if history.empty:
        return {
            "history": [],
            "forecast": []
        }

    future = pd.DataFrame({
        "month_index": range(
            len(history),
            len(history) + 6
        )
    })

    future["forecast"] = model.predict(
        future[["month_index"]]
    )

    last_month = pd.to_datetime(
        history["month"].iloc[-1]
    )

    future["month"] = pd.date_range(
        start=last_month + pd.DateOffset(months=1),
        periods=6,
        freq="MS"
    ).strftime("%Y-%m")

    future["forecast"] = future["forecast"].round(2)

    return {
        "history": history.to_dict(
            orient="records"
        ),

        "forecast": future[
            ["month", "forecast"]
        ].rename(
            columns={
                "forecast": "revenue"
            }
        ).to_dict(
            orient="records"
        )
    }
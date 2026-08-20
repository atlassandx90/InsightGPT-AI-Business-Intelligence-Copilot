import pandas as pd
from sqlalchemy import text
from app.database.connection import engine
from sklearn.linear_model import LinearRegression

from app.analytics.filters import build_filters

# ==========================================================
# KPI
# ==========================================================

def get_kpis(
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

        revenue = conn.execute(text(f"""
            SELECT
                SUM(p.payment_value)

            FROM orders o

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            {join_clause}

            {where_clause}

        """), params).scalar()

        orders = conn.execute(text(f"""
            SELECT
                COUNT(DISTINCT o.order_id)

            FROM orders o

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            {join_clause}

            {where_clause}

        """), params).scalar()

        avg_order = conn.execute(text(f"""
            SELECT

            ROUND(

            (

            SUM(p.payment_value)

            /

            NULLIF(COUNT(DISTINCT o.order_id),0)

            )::numeric,

            2

            )

            FROM orders o

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            {join_clause}

            {where_clause}

        """), params).scalar()

        status = conn.execute(text(f"""
            SELECT

                o.order_status,

                COUNT(*) AS total_orders

            FROM orders o

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            {join_clause}

            {where_clause}

            GROUP BY o.order_status

            ORDER BY total_orders DESC

        """), params).fetchall()

    return {

        "total_revenue": float(revenue or 0),

        "total_orders": int(orders or 0),

        "average_order_value": float(avg_order or 0),

        "order_status": [

            {

                "status": row.order_status,

                "total_orders": row.total_orders

            }

            for row in status

        ]

    }


# ==========================================================
# MONTHLY SALES
# ==========================================================

def get_monthly_sales(
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

        result = conn.execute(text(f"""
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

        """), params).mappings().all()

    return [dict(row) for row in result]


# ==========================================================
# STATE REVENUE
# ==========================================================

def get_state_revenue(
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

        result = conn.execute(text(f"""

            SELECT

                c.customer_state AS state,

                ROUND(
                    SUM(p.payment_value)::numeric,
                    2
                ) AS revenue

            FROM customers c

            JOIN orders o
                ON c.customer_id = o.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            {join_clause}

            {where_clause}

            GROUP BY c.customer_state

            ORDER BY revenue DESC

            LIMIT 10

        """), params).mappings().all()

    return [dict(row) for row in result]

def get_top_categories(
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

        result = conn.execute(text(f"""

            SELECT
                pr.product_category_name AS category,
                ROUND(SUM(p.payment_value)::numeric, 2) AS revenue

            FROM orders o

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            JOIN orderitems oi
                ON o.order_id = oi.order_id

            JOIN products pr
                ON oi.product_id = pr.product_id

            {join_clause}

            {where_clause}

            GROUP BY pr.product_category_name

            ORDER BY revenue DESC

            LIMIT 10

        """), params).mappings().all()

    return [dict(row) for row in result]


def get_payment_types(
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

        result = conn.execute(text(f"""

            SELECT

                p.payment_type,

                COUNT(*) AS total_payments

            FROM orders o

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            {join_clause}

            {where_clause}

            GROUP BY p.payment_type

            ORDER BY total_payments DESC

        """), params).mappings().all()

    return [dict(row) for row in result]


def get_review_scores(
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

        result = conn.execute(text(f"""

            SELECT

                r.review_score,

                COUNT(*) AS total_reviews

            FROM reviews r

            JOIN orders o
                ON r.order_id = o.order_id

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            {join_clause}

            {where_clause}

            GROUP BY r.review_score

            ORDER BY r.review_score

        """), params).mappings().all()

        avg = conn.execute(text(f"""

            SELECT

                ROUND(
                    AVG(r.review_score)::numeric,
                    2
                )

            FROM reviews r

            JOIN orders o
                ON r.order_id = o.order_id

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            {join_clause}
            {where_clause}

        """), params).scalar()

    return {

        "average_rating": float(avg or 0),

        "ratings": [dict(row) for row in result]

    }

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

        result = conn.execute(text(f"""

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

            ORDER BY month

        """), params).mappings().all()

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

    history = df[["month","revenue"]].copy()
    history = history.iloc[:-2]

    future = pd.DataFrame({
    "month_index": range(len(history), len(history)+6)
    })

    future["forecast"] = model.predict(future[["month_index"]])

    last_month = pd.to_datetime(history["month"].iloc[-1])

    future["month"] = pd.date_range(
    start=last_month + pd.DateOffset(months=1),
    periods=6,
    freq="MS"
    ).strftime("%Y-%m")

    future["forecast"] = future["forecast"].round(2)

    return {

    "history": history.to_dict(orient="records"),

    "forecast": future[
        ["month", "forecast"]
    ].rename(
        columns={"forecast": "revenue"}
    ).to_dict(orient="records")

    }

def get_ai_insights(
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

        revenue = conn.execute(text(f"""

            SELECT
                ROUND(SUM(p.payment_value)::numeric,2)

            FROM orders o

            JOIN customers c
                ON o.customer_id=c.customer_id

            JOIN payments p
                ON o.order_id=p.order_id

            {join_clause}

            {where_clause}

        """), params).scalar()

        top_state = conn.execute(text(f"""

            SELECT

                c.customer_state,

                ROUND(
                    SUM(p.payment_value)::numeric,
                    2
                ) revenue

            FROM customers c

            JOIN orders o
                ON c.customer_id=o.customer_id

            JOIN payments p
                ON o.order_id=p.order_id

            {join_clause}
            {where_clause}

            GROUP BY c.customer_state

            ORDER BY revenue DESC

            LIMIT 1

        """), params).first()

        top_category = conn.execute(text(f"""

            SELECT
                pr.product_category_name,
                ROUND(SUM(p.payment_value)::numeric, 2) revenue

            FROM orders o

            JOIN customers c
                ON o.customer_id = c.customer_id

            JOIN payments p
                ON o.order_id = p.order_id

            JOIN orderitems oi
                ON o.order_id = oi.order_id

            JOIN products pr
                ON oi.product_id = pr.product_id

            {where_clause}

            GROUP BY pr.product_category_name

            ORDER BY revenue DESC

            LIMIT 1

       """), params).first()

        payment = conn.execute(text(f"""

            SELECT

                p.payment_type,

                COUNT(*) total

            FROM orders o

            JOIN customers c
                ON o.customer_id=c.customer_id

            JOIN payments p
                ON o.order_id=p.order_id

            {join_clause}

            {where_clause}

            GROUP BY p.payment_type

            ORDER BY total DESC

            LIMIT 1

        """), params).first()

        rating = conn.execute(text(f"""

            SELECT

                ROUND(
                    AVG(r.review_score)::numeric,
                    2
                )

            FROM reviews r

            JOIN orders o
                ON r.order_id=o.order_id

            JOIN customers c
                ON o.customer_id=c.customer_id

            JOIN payments p
                ON o.order_id=p.order_id

            {join_clause}

            {where_clause}

        """), params).scalar()

    return {

        "revenue": float(revenue or 0),

        "top_state": top_state.customer_state if top_state else None,

        "top_category": top_category.product_category_name if top_category else None,

        "payment_type": payment.payment_type if payment else None,

        "rating": float(rating or 0)

    }


def get_dashboard_filters():

    with engine.connect() as conn:

        states = conn.execute(text("""
            SELECT DISTINCT customer_state
            FROM customers
            ORDER BY customer_state;
        """)).scalars().all()

        categories = conn.execute(text("""
            SELECT DISTINCT product_category_name
            FROM products
            WHERE product_category_name IS NOT NULL
            ORDER BY product_category_name;
        """)).scalars().all()

        payment_types = conn.execute(text("""
            SELECT DISTINCT payment_type
            FROM payments
            ORDER BY payment_type;
        """)).scalars().all()

        payment_types = [
        p for p in payment_types
        if p and p != "not_defined"
       ]

    return {
        "states": states,
        "categories": categories,
        "payment_types": payment_types
    }
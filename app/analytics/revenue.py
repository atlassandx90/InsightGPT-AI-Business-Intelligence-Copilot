from sqlalchemy import text

from app.database.connection import engine
from app.analytics.filters import build_filters


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

    return [dict(row) for row in result]


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

        result = conn.execute(
            text(f"""
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

                LIMIT 10;
            """),
            params
        ).mappings().all()

    return [dict(row) for row in result]


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

        revenue = conn.execute(
            text(f"""
                SELECT
                    SUM(p.payment_value)

                FROM orders o

                JOIN customers c
                    ON o.customer_id = c.customer_id

                JOIN payments p
                    ON o.order_id = p.order_id

                {join_clause}

                {where_clause}
            """),
            params
        ).scalar()

        orders = conn.execute(
            text(f"""
                SELECT
                    COUNT(DISTINCT o.order_id)

                FROM orders o

                JOIN customers c
                    ON o.customer_id = c.customer_id

                JOIN payments p
                    ON o.order_id = p.order_id

                {join_clause}

                {where_clause}
            """),
            params
        ).scalar()

        avg_order = conn.execute(
            text(f"""
                SELECT
                    ROUND(
                        (
                            SUM(p.payment_value)
                            /
                            NULLIF(
                                COUNT(DISTINCT o.order_id),
                                0
                            )
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
            """),
            params
        ).scalar()

        status = conn.execute(
            text(f"""
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
            """),
            params
        ).fetchall()

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
from sqlalchemy import text

from app.database.connection import engine
from app.analytics.filters import build_filters


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

        result = conn.execute(
            text(f"""
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

                ORDER BY total_payments DESC;
            """),
            params
        ).mappings().all()

    return [dict(row) for row in result]
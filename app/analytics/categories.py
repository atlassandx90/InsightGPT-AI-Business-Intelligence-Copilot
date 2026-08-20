from sqlalchemy import text

from app.database.connection import engine
from app.analytics.filters import build_filters


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

    # Category analytics always requires
    # orderitems and products.
    category_joins = """
        JOIN orderitems oi
            ON o.order_id = oi.order_id

        JOIN products pr
            ON oi.product_id = pr.product_id
    """

    # Avoid duplicate category joins when
    # build_filters() has already added them.
    if category:
        category_joins = ""

    with engine.connect() as conn:

        result = conn.execute(
            text(f"""
                SELECT
                    pr.product_category_name AS category,

                    ROUND(
                        SUM(p.payment_value)::numeric,
                        2
                    ) AS revenue

                FROM orders o

                JOIN customers c
                    ON o.customer_id = c.customer_id

                JOIN payments p
                    ON o.order_id = p.order_id

                {category_joins}

                {join_clause}

                {where_clause}

                GROUP BY pr.product_category_name

                ORDER BY revenue DESC

                LIMIT 10;
            """),
            params
        ).mappings().all()

    return [dict(row) for row in result]
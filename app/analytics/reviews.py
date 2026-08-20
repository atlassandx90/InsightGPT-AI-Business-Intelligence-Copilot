from sqlalchemy import text

from app.database.connection import engine
from app.analytics.filters import build_filters


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

        result = conn.execute(
            text(f"""
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

                ORDER BY r.review_score;
            """),
            params
        ).mappings().all()

        avg = conn.execute(
            text(f"""
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
            """),
            params
        ).scalar()

    return {
        "average_rating": float(avg or 0),

        "ratings": [
            dict(row)
            for row in result
        ]
    }
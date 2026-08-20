def build_filters(state=None, category=None, payment_type=None):

    where = []
    params = {}
    joins = []

    if state:
        where.append("c.customer_state = :state")
        params["state"] = state

    if payment_type:
        where.append("p.payment_type = :payment_type")
        params["payment_type"] = payment_type

    if category:
        joins.append(
            "JOIN orderitems oi ON o.order_id = oi.order_id"
        )
        joins.append(
            "JOIN products pr ON oi.product_id = pr.product_id"
        )

        where.append(
            "pr.product_category_name = :category"
        )

        params["category"] = category

    where_clause = (
        "WHERE " + " AND ".join(where)
        if where
        else ""
    )

    join_clause = " ".join(joins)

    return where_clause, params, join_clause
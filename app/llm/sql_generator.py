from app.llm.query_parser import parse_question


def generate_sql(question: str):

    parsed = parse_question(question)

    if parsed.intent == "total_revenue":
        return """
        SELECT SUM(payment_value)
        FROM payments
        """

    elif parsed.intent == "orders":
        return """
        SELECT COUNT(DISTINCT order_id)
        FROM orders
        """

    elif parsed.intent == "aov":
        return """
        SELECT
        SUM(payment_value) /
        COUNT(DISTINCT order_id)
        FROM payments
        """

    elif parsed.intent == "state":
        return """
        SELECT customer_state,
               SUM(payment_value)
        FROM customers
        GROUP BY customer_state
        """

    elif parsed.intent == "category":
        return """
        SELECT product_category_name,
               SUM(payment_value)
        FROM products
        GROUP BY product_category_name
        """

    elif parsed.intent == "payment":
        return """
        SELECT payment_type,
               COUNT(*)
        FROM payments
        GROUP BY payment_type
        """

    elif parsed.intent == "rating":
        return """
        SELECT AVG(review_score)
        FROM reviews
        """

    elif parsed.intent == "forecast":
        return """
        SELECT month,
               revenue
        FROM monthly_sales
        """

    return None
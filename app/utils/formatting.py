def format_currency(value):
    """
    Format a numeric value as USD currency.
    Example:
        16008872.12 -> $16,008,872.12
    """

    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return "$0.00"


def format_number(value):
    """
    Format a number with comma separators.
    Example:
        5466 -> 5,466
    """

    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "0"


def format_percentage(value):
    """
    Format a percentage with two decimal places.
    Example:
        12.3456 -> 12.35%
    """

    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return "0.00%"


def format_category_name(category):
    """
    Convert database category names into readable text.
    Example:
        furniture_decor -> Furniture Decor
    """

    if not category:
        return "Unknown"

    return str(category).replace("_", " ").title()


def format_payment_type(payment_type):
    """
    Convert payment type into readable text.
    Example:
        credit_card -> Credit Card
    """

    if not payment_type:
        return "Unknown"

    return str(payment_type).replace("_", " ").title()
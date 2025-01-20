from src.models import Check


def create_formatted_check(check: Check, line_width: int = 30) -> str:
    min_width = 15
    max_width = 120
    line_width = max(min_width, min(max_width, line_width))

    header = "ФОП Джонсонюк Борис"
    formatted_check = f"{header:^{line_width}}\n"
    formatted_check += "=" * line_width + "\n"

    for product in check.products:
        line_total = product.quantity * product.price
        quantity_price = f"{product.quantity:.2f} x {product.price:.2f}"
        product_line = f"{product.name:<{line_width - 10}}{line_total:>10.2f}"
        formatted_check += f"{quantity_price}\n"
        formatted_check += f"{product_line}\n"
        formatted_check += "-" * line_width + "\n"

    formatted_check += "=" * line_width + "\n"
    formatted_check += f"{'СУМА':<{line_width - 10}}{check.total_price:>10.2f}\n"
    formatted_check += f"{check.payment.type.capitalize():<{line_width - 10}}{check.payment.amount:>10.2f}\n"

    if check.payment.amount > check.total_price:
        change = check.payment.amount - check.total_price
        formatted_check += f"{'Решта':<{line_width - 10}}{change:>10.2f}\n"

    formatted_check += "=" * line_width + "\n"
    date_str = check.created_at.strftime('%d.%m.%Y %H:%M')
    formatted_check += f"{date_str:^{line_width}}\n"
    formatted_check += f"{'Дякуємо за покупку!':^{line_width}}\n"

    return formatted_check
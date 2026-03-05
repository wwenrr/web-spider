def calculate_discount(amount: float, percent: float) -> float:
    return max(0.0, amount - (amount * percent / 100.0))


def average(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)

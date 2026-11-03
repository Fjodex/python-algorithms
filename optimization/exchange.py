"""Dynamic programming for alternating currency exchange with a transaction fee."""
from math import floor


def maximize_final_currency(rates: list[float], initial: float = 1000.0, fee: float = 0.03) -> float:
    """Maximize final CAD balance; each conversion loses `fee` of converted value."""
    cad, usd = initial, 0.0
    for rate in rates:
        if rate <= 0 or not 0 <= fee < 1:
            raise ValueError("rates must be positive and fee must be in [0, 1)")
        next_usd = max(usd, floor(cad / rate * (1 - fee) * 100) / 100)
        next_cad = max(cad, floor(usd * rate * (1 - fee) * 100) / 100)
        cad, usd = next_cad, next_usd
    return cad

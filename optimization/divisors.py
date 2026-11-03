"""Find values one less than the proper divisors of an integer."""
from math import isqrt


def divisor_offsets(number: int) -> list[int]:
    if number <= 0:
        raise ValueError("number must be positive")
    result = set()
    for divisor in range(1, isqrt(number) + 1):
        if number % divisor == 0:
            other = number // divisor
            if divisor != number:
                result.add(divisor - 1)
            if other != number:
                result.add(other - 1)
    return sorted(result)

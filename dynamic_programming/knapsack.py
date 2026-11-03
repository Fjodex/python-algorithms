"""0/1 knapsack with reconstruction of selected item indices."""


def knapsack(capacity: int, items: list[tuple[int, int]]) -> list[int]:
    """Return indices of a maximum-value subset; items are (value, weight)."""
    if capacity < 0 or any(weight < 0 for _, weight in items):
        raise ValueError("capacity and weights must be non-negative")
    count = len(items)
    dp = [[0] * (capacity + 1) for _ in range(count + 1)]
    for i, (value, weight) in enumerate(items, start=1):
        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]
            if weight <= current_capacity:
                dp[i][current_capacity] = max(
                    dp[i][current_capacity],
                    dp[i - 1][current_capacity - weight] + value,
                )
    selected = []
    remaining = capacity
    for i in range(count, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            selected.append(i - 1)
            remaining -= items[i - 1][1]
    return selected[::-1]

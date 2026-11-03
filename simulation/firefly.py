"""Compute the minimum number of visible fireflies in a stalactite/stalagmite cave."""


def minimum_collisions(length: int, height: int, obstacles: list[int]) -> tuple[int, int]:
    if length != len(obstacles):
        raise ValueError("length must match the number of obstacles")
    if height <= 0 or any(not 1 <= size <= height for size in obstacles):
        raise ValueError("obstacle sizes must be between 1 and cave height")
    bottom = [0] * (height + 1)
    top = [0] * (height + 1)
    for index, size in enumerate(obstacles):
        (bottom if index % 2 == 0 else top)[size] += 1
    for level in range(height - 1, 0, -1):
        bottom[level] += bottom[level + 1]
        top[level] += top[level + 1]
    hits = [bottom[level] + top[height - level + 1] for level in range(1, height + 1)]
    minimum = min(hits)
    return minimum, hits.count(minimum)

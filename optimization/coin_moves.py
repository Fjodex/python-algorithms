"""BFS for the minimum number of integer-vector moves to a circle boundary."""
from collections import deque
from math import isqrt


def minimum_moves(radius: int, moves: list[tuple[int, int]]) -> int | None:
    if radius < 0:
        raise ValueError("radius must be non-negative")
    if radius == 0:
        return 0
    moves = list(dict.fromkeys((x, y) for x, y in moves if x or y))
    visited = {(0, 0)}
    queue = deque([(0, 0, 0)])
    radius_squared = radius * radius
    while queue:
        x, y, count = queue.popleft()
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            squared = nx * nx + ny * ny
            if squared == radius_squared:
                return count + 1
            if squared < radius_squared and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, count + 1))
    return None

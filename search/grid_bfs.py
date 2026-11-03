"""Breadth-first search for grid reachability problems."""
from collections import deque


def collect_reachable_gold(board: list[str], start: tuple[int, int]) -> int:
    """Collect reachable gold; cells adjacent to traps are dead ends."""
    if not board or not board[0] or any(len(row) != len(board[0]) for row in board):
        raise ValueError("board must be a non-empty rectangle")
    height, width = len(board), len(board[0])
    sx, sy = start
    if not (0 <= sx < width and 0 <= sy < height) or board[sy][sx] == '#':
        raise ValueError("start must be a walkable cell")
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    visited = {(sx, sy)}
    queue = deque([(sx, sy)])
    gold = 0
    while queue:
        x, y = queue.popleft()
        gold += board[y][x] == 'G'
        if any(0 <= x + dx < width and 0 <= y + dy < height and board[y + dy][x + dx] == 'T' for dx, dy in directions):
            continue
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and board[ny][nx] != '#' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return gold

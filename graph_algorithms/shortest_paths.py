"""Shortest-path algorithms for weighted graphs and grids."""
from __future__ import annotations
import heapq
from math import inf


def dijkstra(vertex_count: int, adjacency: list[list[tuple[int, int]]], source: int) -> list[float]:
    """Return shortest distances from source. Edge weights must be non-negative."""
    if not 0 <= source < vertex_count:
        raise ValueError("source is outside the graph")
    distances = [inf] * vertex_count
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        distance, vertex = heapq.heappop(queue)
        if distance != distances[vertex]:
            continue
        for neighbor, weight in adjacency[vertex]:
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heapq.heappush(queue, (candidate, neighbor))
    return distances


def minimum_cost_grid_path(grid: list[list[int]]) -> tuple[int, set[tuple[int, int]]]:
    """Find a minimum-cost top-to-bottom path; diagonal moves are allowed."""
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("grid must be a non-empty rectangle")
    height, width = len(grid), len(grid[0])
    if any(value < 0 for row in grid for value in row):
        raise ValueError("grid costs must be non-negative")
    dist = [[inf] * width for _ in range(height)]
    parent: list[list[tuple[int, int] | None]] = [[None] * width for _ in range(height)]
    queue = []
    for col in range(width):
        dist[0][col] = grid[0][col]
        heapq.heappush(queue, (grid[0][col], 0, col))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    while queue:
        cost, row, col = heapq.heappop(queue)
        if cost != dist[row][col]:
            continue
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width:
                candidate = cost + grid[nr][nc]
                if candidate < dist[nr][nc]:
                    dist[nr][nc] = candidate
                    parent[nr][nc] = (row, col)
                    heapq.heappush(queue, (candidate, nr, nc))
    end_col = min(range(width), key=lambda col: dist[-1][col])
    path = set()
    position: tuple[int, int] | None = (height - 1, end_col)
    while position is not None:
        path.add(position)
        row, col = position
        position = parent[row][col]
    return int(dist[-1][end_col]), path


def cave_escape_time(initial_water: int, top: list[list[int]], bottom: list[list[int]]) -> float:
    """Minimum travel time through a cave grid (10 units/sec water drop).

    Implements the standard cave-clearance rules: 50-unit clearance is required;
    the first move can be instantaneous when possible at time zero, otherwise
    movement takes 1 second in >=20 water units or 10 seconds in shallower water.
    """
    rows, cols = len(top), len(top[0])
    if not rows or not cols or len(bottom) != rows or any(len(r) != cols for r in top + bottom):
        raise ValueError("top and bottom must be equally sized non-empty grids")
    best = [[inf] * cols for _ in range(rows)]
    best[0][0] = 0.0
    queue = [(0.0, 0, 0)]
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    while queue:
        current, row, col = heapq.heappop(queue)
        if current != best[row][col]:
            continue
        if (row, col) == (rows - 1, cols - 1):
            return current
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            # Clearance constraints between both adjacent cells.
            if bottom[nr][nc] + 50 > top[nr][nc] or bottom[row][col] + 50 > top[nr][nc] or bottom[nr][nc] + 50 > top[row][col]:
                continue
            required_water = top[nr][nc] - 50
            wait_until = max(0.0, (initial_water - required_water) / 10.0)
            departure = max(current, wait_until)
            if current == 0.0 and wait_until == 0.0:
                arrival = 0.0
            else:
                water_now = max(0.0, initial_water - 10.0 * departure)
                movement = 1.0 if water_now >= bottom[row][col] + 20 else 10.0
                arrival = departure + movement
            if arrival < best[nr][nc]:
                best[nr][nc] = arrival
                heapq.heappush(queue, (arrival, nr, nc))
    return best[-1][-1]

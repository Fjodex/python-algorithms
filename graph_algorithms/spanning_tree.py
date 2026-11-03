"""Minimum spanning tree using Prim's algorithm."""
import heapq


def prim_mst(vertex_count: int, edges: list[tuple[int, int, int]]) -> tuple[int, list[tuple[int, int]]] | None:
    if vertex_count == 0:
        return 0, []
    adjacency = [[] for _ in range(vertex_count)]
    for u, v, weight in edges:
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))
    visited = [False] * vertex_count
    parent = [-1] * vertex_count
    best = [float("inf")] * vertex_count
    best[0] = 0
    queue = [(0, 0)]
    total = 0
    while queue:
        weight, u = heapq.heappop(queue)
        if visited[u]:
            continue
        visited[u] = True
        total += weight
        for v, cost in adjacency[u]:
            if not visited[v]:
                heapq.heappush(queue, (cost, v))
                if parent[v] == -1:
                    parent[v] = u
                # Keep the cheapest known edge to v.
                if cost < best[v]:
                    best[v] = cost
                    parent[v] = u
    if not all(visited):
        return None
    result = [(min(parent[v], v), max(parent[v], v)) for v in range(1, vertex_count)]
    return total, sorted(result)

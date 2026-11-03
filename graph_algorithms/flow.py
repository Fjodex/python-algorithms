"""Maximum-flow algorithms: Dinic and Edmonds-Karp."""
from collections import deque


class Dinic:
    def __init__(self, vertex_count: int):
        if vertex_count <= 0:
            raise ValueError("vertex_count must be positive")
        self.graph: list[list[list]] = [[] for _ in range(vertex_count)]

    def add_edge(self, source: int, target: int, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity cannot be negative")
        forward = [target, capacity, None]
        reverse = [source, 0, forward]
        forward[2] = reverse
        self.graph[source].append(forward)
        self.graph[target].append(reverse)

    def max_flow(self, source: int, sink: int) -> int:
        if source == sink:
            return 0
        total = 0
        size = len(self.graph)
        while True:
            level = [-1] * size
            level[source] = 0
            queue = deque([source])
            while queue:
                vertex = queue.popleft()
                for target, capacity, _ in self.graph[vertex]:
                    if capacity > 0 and level[target] < 0:
                        level[target] = level[vertex] + 1
                        queue.append(target)
            if level[sink] < 0:
                return total
            cursor = [0] * size

            def send(vertex: int, amount: int) -> int:
                if vertex == sink:
                    return amount
                while cursor[vertex] < len(self.graph[vertex]):
                    edge = self.graph[vertex][cursor[vertex]]
                    target, capacity, reverse = edge
                    if capacity > 0 and level[target] == level[vertex] + 1:
                        pushed = send(target, min(amount, capacity))
                        if pushed:
                            edge[1] -= pushed
                            reverse[1] += pushed
                            return pushed
                    cursor[vertex] += 1
                return 0

            while pushed := send(source, 10**30):
                total += pushed


def edmonds_karp(vertex_count: int, edges: list[tuple[int, int, int]], source: int, sink: int) -> tuple[int, list[int]]:
    """Return maximum flow and source-side vertices in the final residual graph."""
    capacity = [[0] * vertex_count for _ in range(vertex_count)]
    adjacency = [[] for _ in range(vertex_count)]
    for u, v, amount in edges:
        if amount < 0:
            raise ValueError("capacity cannot be negative")
        if v not in adjacency[u]:
            adjacency[u].append(v)
            adjacency[v].append(u)
        capacity[u][v] += amount
    total = 0
    while True:
        parent = [-1] * vertex_count
        parent[source] = source
        queue = deque([source])
        while queue and parent[sink] == -1:
            u = queue.popleft()
            for v in adjacency[u]:
                if parent[v] == -1 and capacity[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1:
            break
        pushed = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            pushed = min(pushed, capacity[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= pushed
            capacity[v][u] += pushed
            v = u
        total += int(pushed)
    reachable = {source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in reachable and capacity[u][v] > 0:
                reachable.add(v)
                queue.append(v)
    return total, sorted(reachable)


def minimum_grid_cut(costs: list[list[int]], start: tuple[int, int]) -> int:
    """Minimum vertex-capacity cut separating a cell from the grid boundary."""
    rows, cols = len(costs), len(costs[0])
    if not rows or not cols or any(len(row) != cols for row in costs):
        raise ValueError("cost grid must be a non-empty rectangle")
    if any(value < 0 for row in costs for value in row):
        raise ValueError("cell costs cannot be negative")
    sr, sc = start
    if not (0 <= sr < rows and 0 <= sc < cols):
        raise ValueError("start cell is outside the grid")
    infinity = sum(map(sum, costs)) + 1
    outside = rows * cols * 2
    flow = Dinic(outside + 1)
    def inside(r, c): return (r * cols + c) * 2
    def out(r, c): return inside(r, c) + 1
    for r in range(rows):
        for c in range(cols):
            flow.add_edge(inside(r, c), out(r, c), costs[r][c])
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    flow.add_edge(out(r, c), inside(nr, nc), infinity)
            if r in (0, rows - 1) or c in (0, cols - 1):
                flow.add_edge(out(r, c), outside, infinity)
    return flow.max_flow(inside(sr, sc), outside)

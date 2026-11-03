"""Bipartite matching with DFS-based augmenting paths (Kuhn's algorithm)."""


def maximum_bipartite_matching(adjacency: list[list[int]], right_size: int | None = None) -> list[int] | None:
    left_size = len(adjacency)
    if right_size is None:
        right_size = left_size
    match_right = [-1] * right_size

    def augment(left: int, seen: list[bool]) -> bool:
        for right in adjacency[left]:
            if not 0 <= right < right_size:
                raise ValueError("right-side vertex index out of range")
            if seen[right]:
                continue
            seen[right] = True
            if match_right[right] == -1 or augment(match_right[right], seen):
                match_right[right] = left
                return True
        return False

    matched = 0
    for left in range(left_size):
        if augment(left, [False] * right_size):
            matched += 1
    if matched != left_size:
        return None
    result = [-1] * left_size
    for right, left in enumerate(match_right):
        if left != -1:
            result[left] = right
    return result

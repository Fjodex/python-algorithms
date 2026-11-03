"""Greedy two-person-per-day scheduler with load balancing improvements."""
from __future__ import annotations
import random


def schedule_workers(availability: dict[str, list[bool]], workday_counts: dict[str, int] | None = None,
                     seed: int = 0) -> tuple[dict[int, list[str]], int]:
    """Assign up to two available workers per day, balancing total assignments.

    This is a heuristic, not an optimal solver. Days are zero-indexed in the result.
    """
    if not availability:
        return {}, 0
    days = len(next(iter(availability.values())))
    if any(len(values) != days for values in availability.values()):
        raise ValueError("all availability lists must have equal length")
    counts = {name: 0 for name in availability}
    tie_counts = workday_counts or {name: sum(days) for name, days in availability.items()}
    rng = random.Random(seed)
    assignments: dict[int, list[str]] = {}
    for day in range(days):
        candidates = [name for name, dates in availability.items() if dates[day]]
        rng.shuffle(candidates)
        candidates.sort(key=lambda name: (counts[name], tie_counts.get(name, 0)))
        chosen = candidates[:2]
        assignments[day] = chosen
        for name in chosen:
            counts[name] += 1
    # Repeatedly move an assignment from a most-loaded worker to a least-loaded
    # worker who is available that day and is not already assigned that day.
    while counts and max(counts.values()) - min(counts.values()) > 1:
        high = max(counts.values())
        low = min(counts.values())
        changed = False
        for day, workers in assignments.items():
            for outgoing in list(workers):
                if counts[outgoing] != high:
                    continue
                replacements = [name for name in availability
                                 if counts[name] == low and availability[name][day] and name not in workers]
                if replacements:
                    incoming = min(replacements, key=lambda name: name)
                    workers[workers.index(outgoing)] = incoming
                    counts[outgoing] -= 1
                    counts[incoming] += 1
                    changed = True
                    break
            if changed:
                break
        if not changed:
            break
    return assignments, max(counts.values(), default=0)

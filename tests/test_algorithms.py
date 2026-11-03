import unittest
from math import isinf

from graph_algorithms.shortest_paths import dijkstra, minimum_cost_grid_path, cave_escape_time
from graph_algorithms.flow import Dinic, edmonds_karp, minimum_grid_cut
from graph_algorithms.spanning_tree import prim_mst
from graph_algorithms.matching import maximum_bipartite_matching
from dynamic_programming.knapsack import knapsack
from search.grid_bfs import collect_reachable_gold
from search.wildcard import wildcard_match, search_files
from optimization.coin_moves import minimum_moves
from optimization.exchange import maximize_final_currency
from optimization.scheduling import schedule_workers
from optimization.divisors import divisor_offsets
from simulation.firefly import minimum_collisions


class GraphTests(unittest.TestCase):
    def test_dijkstra(self):
        graph = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 5)], []]
        self.assertEqual(dijkstra(4, graph, 0), [0, 3, 1, 4])
        self.assertTrue(isinf(dijkstra(3, [[], [], []], 0)[2]))

    def test_dijkstra_rejects_negative_weight(self):
        with self.assertRaises(ValueError):
            dijkstra(2, [[(1, -1)], []], 0)

    def test_grid_path(self):
        cost, path = minimum_cost_grid_path([[1, 9], [2, 3]])
        self.assertEqual(cost, 3)
        self.assertIn((0, 0), path)
        self.assertEqual(max(r for r, _ in path), 1)

    def test_dinic(self):
        graph = Dinic(4)
        for edge in [(0, 1, 3), (0, 2, 2), (1, 2, 1), (1, 3, 2), (2, 3, 3)]:
            graph.add_edge(*edge)
        self.assertEqual(graph.max_flow(0, 3), 5)

    def test_edmonds_karp(self):
        value, reachable = edmonds_karp(4, [(0, 1, 3), (0, 2, 2), (1, 2, 1), (1, 3, 2), (2, 3, 3)], 0, 3)
        self.assertEqual(value, 5)
        self.assertEqual(reachable, [0])

    def test_grid_cut(self):
        self.assertEqual(minimum_grid_cut([[5, 5, 5], [5, 1, 5], [5, 5, 5]], (1, 1)), 1)

    def test_prim(self):
        result = prim_mst(3, [(0, 1, 2), (1, 2, 1), (0, 2, 5)])
        self.assertEqual(result, (3, [(0, 1), (1, 2)]))
        self.assertIsNone(prim_mst(3, [(0, 1, 1)]))

    def test_matching(self):
        self.assertEqual(maximum_bipartite_matching([[0, 1], [0]]), [1, 0])
        self.assertIsNone(maximum_bipartite_matching([[0], [0]]))

    def test_cave_start_is_instant_when_clear(self):
        self.assertEqual(cave_escape_time(0, [[100, 100]], [[0, 0]]), 0.0)

    def test_cave_waits_for_water_to_drop(self):
        self.assertEqual(cave_escape_time(100, [[100, 100]], [[0, 0]]), 6.0)


class OtherAlgorithmTests(unittest.TestCase):
    def test_knapsack(self):
        items = [(6, 4), (4, 3), (5, 2)]
        chosen = knapsack(5, items)
        self.assertEqual(sum(items[i][0] for i in chosen), 9)
        self.assertLessEqual(sum(items[i][1] for i in chosen), 5)
        self.assertEqual(knapsack(10, []), [])

    def test_gold_bfs(self):
        board = ["#####", "#P.G#", "#####"]
        self.assertEqual(collect_reachable_gold(board, (1, 1)), 1)

    def test_wildcard(self):
        self.assertTrue(wildcard_match("abc", "abc"))
        self.assertFalse(wildcard_match("abc", "xabc"))
        self.assertTrue(wildcard_match("a*c", "abbbc"))
        self.assertTrue(wildcard_match("*abc*", "xxabczz"))
        self.assertFalse(wildcard_match("a*d", "abbbc"))
        self.assertTrue(wildcard_match("a**c", "abc"))
        self.assertTrue(wildcard_match("*", "anything"))
        self.assertEqual(search_files(["alpha", "beta", "alphabet"], "*pha*"), ["alpha", "alphabet"])

    def test_coin_moves(self):
        self.assertEqual(minimum_moves(5, [(3, 4), (0, 1)]), 1)
        self.assertIsNone(minimum_moves(2, [(2, 2)]))

    def test_exchange(self):
        self.assertEqual(maximize_final_currency([]), 1000.0)
        self.assertEqual(maximize_final_currency([2.0]), 1000.0)

    def test_scheduler(self):
        availability = {"A": [True, True], "B": [True, True], "C": [True, True]}
        assignments, maximum = schedule_workers(availability, seed=1)
        self.assertTrue(all(len(day) == 2 for day in assignments.values()))
        self.assertEqual(maximum, 2)
        self.assertEqual(len({worker for day in assignments.values() for worker in day}), 3)

    def test_divisors(self):
        self.assertEqual(divisor_offsets(12), [0, 1, 2, 3, 5])

    def test_firefly(self):
        self.assertEqual(minimum_collisions(4, 5, [1, 3, 2, 4]), (2, 5))


if __name__ == "__main__":
    unittest.main()

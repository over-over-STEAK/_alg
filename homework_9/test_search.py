import unittest
from itertools import product
from grid_search import search
from river_bfs import solve as river, safe
from queens_dfs import solve as queens
from ic_routing import GRID, START, GOAL

class SearchTests(unittest.TestCase):
    def test_river(self):
        path = river()
        self.assertEqual(path[0], (0,0,0,0))
        self.assertEqual(path[-1], (1,1,1,1))
        self.assertEqual(len(path)-1, 7)
        for s in path:
            self.assertTrue(safe(s))
        for a, b in zip(path, path[1:]):
            self.assertNotEqual(a[0], b[0])
            passengers = [i for i in (1,2,3) if a[i] != b[i]]
            self.assertLessEqual(len(passengers), 1)
            for i in passengers:
                self.assertEqual(a[i], a[0])
                self.assertEqual(b[i], b[0])

    def test_queens(self):
        results = queens()
        self.assertEqual(len({tuple(p) for p in results}), 92)
        for p in results:
            self.assertEqual(len(set(p)), 8)
            self.assertEqual(len({r-c for r,c in enumerate(p)}), 8)
            self.assertEqual(len({r+c for r,c in enumerate(p)}), 8)
        self.assertEqual(queens(2), [])
        self.assertEqual(queens(3), [])
        self.assertEqual(queens(1), [[0]])

    def test_weighted(self):
        for method, expected in (("bfs", 46), ("dijkstra", 10), ("astar", 10)):
            result = search(GRID, START, GOAL, method)
            self.assertEqual(result["cost"], expected)
            self.check_path(GRID, result["path"], START, GOAL)

    def check_path(self, grid, path, start, goal):
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        for r,c in path:
            self.assertGreater(grid[r][c], 0)
        for a,b in zip(path, path[1:]):
            self.assertEqual(abs(a[0]-b[0])+abs(a[1]-b[1]), 1)

    def test_small_maps_exhaustive(self):
        # 窮舉 3×3 的其餘七格障礙配置，交叉比對最短步數與可達性。
        for bits in product((0,1), repeat=7):
            flat = [1, *bits, 1]
            grid = [flat[i:i+3] for i in range(0,9,3)]
            baseline = search(grid, (0,0), (2,2), "bfs")
            for method in ("dfs", "dijkstra", "astar"):
                result = search(grid, (0,0), (2,2), method)
                self.assertEqual(bool(result["path"]), bool(baseline["path"]))
                if result["path"]:
                    self.check_path(grid, result["path"], (0,0), (2,2))
                if method != "dfs":
                    self.assertEqual(result["cost"], baseline["cost"])

    def test_edges(self):
        for method in ("dfs", "bfs", "dijkstra", "astar"):
            self.assertEqual(search([[1]], (0,0), (0,0), method)["cost"], 0)
            self.assertEqual(search([[1,0,1]], (0,0), (0,2), method)["path"], [])
        with self.assertRaises(ValueError):
            search([[0]], (0,0), (0,0))
        with self.assertRaises(ValueError):
            search([[1], [1,1]], (0,0), (1,0))

if __name__ == "__main__":
    unittest.main(verbosity=2)

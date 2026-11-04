"""四方向格點搜尋；正整數為進入格子的成本，0 為障礙。"""
from collections import deque
from heapq import heappop, heappush


def search(grid, start, goal, method="astar"):
    if method not in {"dfs", "bfs", "dijkstra", "astar"}:
        raise ValueError("未知搜尋方法")
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("地圖必須是非空矩形")
    if any(not isinstance(v, int) or v < 0 for row in grid for v in row):
        raise ValueError("成本必須是非負整數")
    rows, cols = len(grid), len(grid[0])
    def valid(p):
        return 0 <= p[0] < rows and 0 <= p[1] < cols and grid[p[0]][p[1]] > 0
    if not valid(start) or not valid(goal):
        raise ValueError("起點、終點必須在可通行的格子")
    minimum = min(v for row in grid for v in row if v > 0)
    def h(p):
        return minimum * (abs(p[0] - goal[0]) + abs(p[1] - goal[1])) if method == "astar" else 0
    parent, costs = {start: None}, {start: 0}
    queue = deque([start])
    heap = [(h(start), 0, start)]
    expanded = 0
    weighted = method in {"dijkstra", "astar"}
    while heap if weighted else queue:
        if weighted:
            _, g, current = heappop(heap)
            if g != costs[current]:
                continue  # 捨棄被更短路徑取代的舊項目
        else:
            current = queue.pop() if method == "dfs" else queue.popleft()
        expanded += 1
        if current == goal:
            path, node = [], goal
            while node is not None:
                path.append(node)
                node = parent[node]
            return {"path": path[::-1], "cost": costs[goal], "expanded": expanded}
        r, c = current
        for nxt in ((r-1, c), (r, c+1), (r+1, c), (r, c-1)):
            if not valid(nxt):
                continue
            new_cost = costs[current] + grid[nxt[0]][nxt[1]]
            if (weighted and new_cost < costs.get(nxt, float("inf"))) or (not weighted and nxt not in parent):
                parent[nxt], costs[nxt] = current, new_cost
                if weighted:
                    heappush(heap, (new_cost + h(nxt), new_cost, nxt))
                else:
                    queue.append(nxt)
    return {"path": [], "cost": None, "expanded": expanded}


def show(grid, path):
    """終端機文字地圖，S 起點、G 終點、* 路徑、# 障礙。"""
    cells = [["#" if v == 0 else "." for v in row] for row in grid]
    for r, c in path:
        cells[r][c] = "*"
    if path:
        cells[path[0][0]][path[0][1]] = "S"
        cells[path[-1][0]][path[-1][1]] = "G"
    print("\n".join(" ".join(row) for row in cells))

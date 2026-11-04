"""教學用單層雙端點繞線：比較步數與帶權成本。"""
from grid_search import search, show

GRID = [[1,1,1,1,1,1,1], [1,0,0,0,0,0,1], [1,9,9,9,9,9,1], [1,0,0,0,0,0,1], [1,1,1,1,1,1,1]]
START, GOAL = (2,0), (2,6)

def main():
    print("IC 繞線：中央捷徑成本高，外圍繞路成本低。")
    for method in ("bfs", "dijkstra", "astar"):
        result = search(GRID, START, GOAL, method)
        print(f"{method}: 步數={len(result['path'])-1}, 成本={result['cost']}, 展開={result['expanded']}")
        show(GRID, result["path"])

if __name__ == "__main__":
    main()

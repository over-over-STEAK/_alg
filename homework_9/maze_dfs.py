"""老鼠走迷宮：使用堆疊進行 DFS。"""
from grid_search import search, show

GRID = [[1,1,0,1,1], [0,1,0,1,0], [1,1,1,1,1], [1,0,0,0,1], [1,1,1,0,1]]

def main():
    result = search(GRID, (0,0), (4,4), "dfs")
    print("老鼠迷宮 DFS:", result)
    show(GRID, result["path"])

if __name__ == "__main__":
    main()

"""靜態四方向地圖中的 NPC 尋路；修改 GOAL 可模擬玩家移動後重新規劃。"""
from grid_search import search, show

GRID = [[1,1,1,1,1,1], [1,0,0,0,0,1], [1,1,1,1,0,1], [1,0,0,1,1,1], [1,1,1,1,0,1]]
START, GOAL = (0,0), (4,5)

def main():
    result = search(GRID, START, GOAL, "astar")
    print("NPC A*:", result)
    show(GRID, result["path"])

if __name__ == "__main__":
    main()

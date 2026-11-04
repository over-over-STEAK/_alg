"""狀態順序：(農夫、狼、羊、甘藍菜)，0 左岸、1 右岸。"""
from collections import deque

def safe(s):
    farmer, wolf, sheep, cabbage = s
    return not ((wolf == sheep != farmer) or (sheep == cabbage != farmer))

def solve():
    start, goal = (0,0,0,0), (1,1,1,1)
    queue, parent = deque([start]), {start: None}
    while queue:
        state = queue.popleft()
        if state == goal:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1]
        for passenger in (None, 1, 2, 3):
            if passenger is not None and state[passenger] != state[0]:
                continue
            nxt = list(state)
            nxt[0] ^= 1
            if passenger is not None:
                nxt[passenger] ^= 1
            nxt = tuple(nxt)
            if safe(nxt) and nxt not in parent:
                parent[nxt] = state
                queue.append(nxt)
    return []

def main():
    path = solve()
    print("狼羊甘藍菜 BFS，最少過河次數:", len(path)-1)
    print("初始:", path[0])
    names = {1: "狼", 2: "羊", 3: "甘藍菜"}
    for step, (a, b) in enumerate(zip(path, path[1:]), 1):
        changed = [i for i in (1,2,3) if a[i] != b[i]]
        action = "帶" + names[changed[0]] if changed else "獨自"
        print(f"{step}. 農夫{action}到{'右' if b[0] else '左'}岸：{b}")

if __name__ == "__main__":
    main()

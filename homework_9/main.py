"""一次執行全部示範，或以 --problem 選擇題目。"""
import argparse
import maze_dfs, river_bfs, queens_dfs, npc_astar, ic_routing

def main():
    demos = {"maze": maze_dfs, "river": river_bfs, "queens": queens_dfs, "npc": npc_astar, "routing": ic_routing}
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", choices=["all", *demos], default="all")
    args = parser.parse_args()
    for name, module in demos.items():
        if args.problem in ("all", name):
            print(f"\n=== {name} ===")
            module.main()

if __name__ == "__main__":
    main()

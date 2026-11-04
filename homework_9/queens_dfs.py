"""逐列 DFS 回溯，使用集合剪枝，列舉所有 N 皇后解。"""
def solve(n=8):
    if not isinstance(n, int) or n < 1:
        raise ValueError("n 必須為正整數")
    answers, placement = [], []
    columns, descending, ascending = set(), set(), set()
    def dfs(row):
        if row == n:
            answers.append(placement.copy())
            return
        for col in range(n):
            if col in columns or row-col in descending or row+col in ascending:
                continue
            placement.append(col)
            columns.add(col)
            descending.add(row-col)
            ascending.add(row+col)
            dfs(row+1)
            placement.pop()
            columns.remove(col)
            descending.remove(row-col)
            ascending.remove(row+col)
    dfs(0)
    return answers

def main():
    answers = solve()
    print("八皇后 DFS，解的數量:", len(answers))
    print("第一組解（各列的欄索引）:", answers[0])
    for col in answers[0]:
        print(" ".join("Q" if c == col else "." for c in range(8)))

if __name__ == "__main__":
    main()

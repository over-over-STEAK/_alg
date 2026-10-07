def hanoi_recursive(n, source="A", auxiliary="B", target="C"):
    if n < 0:
        raise ValueError("圓盤數不能是負數")

    if n == 0:
        return

    hanoi_recursive(n - 1, source, target, auxiliary)
    print(f"圓盤 {n}：{source} → {target}")
    hanoi_recursive(n - 1, auxiliary, source, target)


hanoi_recursive(3)
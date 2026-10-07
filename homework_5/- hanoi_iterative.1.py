def hanoi_iterative(n, source="A", auxiliary="B", target="C"):
    if n < 0:
        raise ValueError("圓盤數不能是負數")

    stack = [("solve", n, source, auxiliary, target)]

    while stack:
        action, disks, src, aux, dst = stack.pop()

        if disks == 0:
            continue

        if action == "move":
            print(f"圓盤 {disks}：{src} → {dst}")
        else:
            # 堆疊後放先取，因此反向放入三個工作
            stack.append(("solve", disks - 1, aux, src, dst))
            stack.append(("move", disks, src, aux, dst))
            stack.append(("solve", disks - 1, src, dst, aux))


hanoi_iterative(3)
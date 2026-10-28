# -*- coding: utf-8 -*-
import argparse
import math
import random
import time
from pathlib import Path

import numpy as np


def make_problem(count=20, seed=42):
    """產生固定城市資料，並建立對稱距離矩陣。"""
    rng = random.Random(seed)
    cities = []
    for _ in range(count):
        x = rng.uniform(0, 100)
        y = rng.uniform(0, 100)
        cities.append((x, y))
    distances = np.zeros((count, count))
    for i in range(count):
        for j in range(i + 1, count):
            distance = math.dist(cities[i], cities[j])
            distances[i, j] = distance
            distances[j, i] = distance
    return cities, distances


def route_length(route, distances):
    """逐段累加，最後補上回到起點的距離。"""
    total = 0.0
    for position in range(len(route) - 1):
        total += distances[route[position], route[position + 1]]
    total += distances[route[-1], route[0]]
    return float(total)


def reverse_segment(route, left, right):
    """複製路線並反轉指定區段，不修改原路線。"""
    candidate = route.copy()
    segment = candidate[left:right + 1]
    segment.reverse()
    candidate[left:right + 1] = segment
    return candidate


def greedy(distances, start=0):
    """5. 貪婪法：用迴圈找最近的未訪問城市。"""
    count = len(distances)
    visited = [False] * count
    route = [start]
    visited[start] = True
    while len(route) < count:
        nearest = None
        shortest = float('inf')
        for city in range(count):
            if visited[city]:
                continue
            distance = distances[route[-1], city]
            if distance < shortest:
                nearest = city
                shortest = distance
        route.append(nearest)
        visited[nearest] = True
    return route


def best_two_opt_move(route, distances):
    """完整檢查 2-opt 鄰域，回傳改善最多的反轉範圍。"""
    count = len(route)
    best_change = -1e-9
    best_move = None
    for first in range(count - 1):
        for second in range(first + 2, count):
            if first == 0 and second == count - 1:
                continue
            a, b = route[first], route[first + 1]
            c, d = route[second], route[(second + 1) % count]
            change = (distances[a, c] + distances[b, d]
                      - distances[a, b] - distances[c, d])
            if change < best_change:
                best_change = change
                best_move = (first + 1, second)
    return best_move


def improvement(distances):
    """1. 改良法：從貪婪解開始，反覆採用最佳 2-opt 改善。"""
    route = greedy(distances)
    while True:
        move = best_two_opt_move(route, distances)
        if move is None:
            return route
        route = reverse_segment(route, move[0], move[1])


def hill_climbing(distances, iterations=20000, seed=1):
    """2. 爬山法：隨機交換兩城市，只接受更短的候選路線。"""
    rng = random.Random(seed)
    route = list(range(len(distances)))
    rng.shuffle(route)
    current_length = route_length(route, distances)
    for _ in range(iterations):
        first, second = rng.sample(range(len(route)), 2)
        candidate = route.copy()
        candidate[first], candidate[second] = candidate[second], candidate[first]
        candidate_length = route_length(candidate, distances)
        if candidate_length < current_length:
            route = candidate
            current_length = candidate_length
    return route


def simulated_annealing(distances, initial_temperature=100.0,
                        end_temperature=0.001, cooling=0.995,
                        trials=100, seed=1):
    """3. 模擬退火：反轉區段，並以 exp(-差值/溫度) 接受較差解。"""
    rng = random.Random(seed)
    route = list(range(len(distances)))
    rng.shuffle(route)
    current_length = route_length(route, distances)
    best_route = route.copy()
    best_length = current_length
    temperature = initial_temperature
    while temperature > end_temperature:
        for _ in range(trials):
            left, right = sorted(rng.sample(range(len(route)), 2))
            candidate = reverse_segment(route, left, right)
            candidate_length = route_length(candidate, distances)
            change = candidate_length - current_length
            if change < 0 or rng.random() < math.exp(-change / temperature):
                route = candidate
                current_length = candidate_length
                if current_length < best_length:
                    best_route = route.copy()
                    best_length = current_length
        temperature *= cooling
    return best_route


def row_softmax(weights):
    """每一列轉為總和等於 1 的權重，減去最大值避免溢位。"""
    shifted = weights - weights.max(axis=1, keepdims=True)
    exponentials = np.exp(shifted)
    return exponentials / exponentials.sum(axis=1, keepdims=True)


def decode_assignment(probabilities):
    """逐次挑最高權重配對，確保位置及城市都不重複。"""
    remaining = probabilities.copy()
    route = [-1] * len(remaining)
    for _ in range(len(route)):
        position, city = np.unravel_index(np.argmax(remaining), remaining.shape)
        route[position] = int(city)
        remaining[position, :] = -1
        remaining[:, city] = -1
    return route


def gradient_descent(distances, steps=3000, learning_rate=0.05,
                     penalty=30.0, seed=1):
    """4. 梯度下降：優化連續權重，再解碼成合法城市排列。

    目標 = 相鄰位置的加權距離 + penalty * 各城市總權重偏離 1 的平方和。
    softmax 保證每列總和為 1；懲罰項鼓勵每欄總和接近 1。
    連續目標下降並不保證解碼後的實際路線更短。
    """
    count = len(distances)
    rng = np.random.default_rng(seed)
    weights = rng.normal(0, 0.1, (count, count))
    normalized = distances / distances.mean()
    for step in range(steps):
        probabilities = row_softmax(weights)
        following = np.roll(probabilities, -1, axis=0)
        preceding = np.roll(probabilities, 1, axis=0)
        # 本題距離矩陣對稱，因此前後兩項皆可右乘 normalized。
        gradient_p = following @ normalized + preceding @ normalized
        column_error = probabilities.sum(axis=0) - 1.0
        gradient_p += 2 * penalty * column_error[None, :]
        weighted_mean = (gradient_p * probabilities).sum(axis=1, keepdims=True)
        gradient_w = probabilities * (gradient_p - weighted_mean)
        rate = learning_rate * (1 - 0.9 * step / steps)
        weights -= rate * gradient_w * 10
    return decode_assignment(row_softmax(weights))


def plot_results(cities, results, show=True):
    """有中文字型時顯示中文，否則使用英文標題，避免缺字。"""
    try:
        import matplotlib
        if not show:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
    except ImportError:
        print('未安裝 matplotlib，略過繪圖；可執行 python -m pip install matplotlib')
        return
    installed = {font.name for font in font_manager.fontManager.ttflist}
    chinese_font = None
    for name in ('Microsoft JhengHei', 'Noto Sans CJK TC', 'Noto Sans CJK SC',
                 'PingFang TC', 'Arial Unicode MS', 'SimHei'):
        if name in installed:
            chinese_font = name
            break
    if chinese_font:
        plt.rcParams['font.sans-serif'] = [chinese_font]
    plt.rcParams['axes.unicode_minus'] = False
    english_titles = ['1. Improvement (2-opt)', '2. Hill climbing',
                      '3. Simulated annealing', '4. Gradient descent', '5. Greedy']
    figure, axes = plt.subplots(2, 3, figsize=(15, 9))
    for index, result in enumerate(results):
        axis = axes.flat[index]
        closed_route = result['route'] + [result['route'][0]]
        xs, ys = [], []
        for city in closed_route:
            xs.append(cities[city][0])
            ys.append(cities[city][1])
        axis.plot(xs, ys, '-o', markersize=5)
        title = result['name'] if chinese_font else english_titles[index]
        axis.set_title(f"{title}  L={result['length']:.2f}")
        axis.set_aspect('equal', adjustable='box')
        axis.grid(alpha=0.2)
    axes.flat[-1].axis('off')
    figure.tight_layout()
    destination = Path(__file__).resolve().parent / 'tsp_results.png'
    figure.savefig(destination, dpi=150)
    print(f'\n比較圖片已儲存：{destination}')
    if show:
        plt.show()
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description='旅行推銷員問題：五種方法比較')
    parser.add_argument('--no-show', action='store_true', help='儲存圖片但不開啟視窗')
    args = parser.parse_args()
    cities, distances = make_problem()
    methods = [
        ('1.改良法（2-opt）', improvement),
        ('2.爬山演算法', hill_climbing),
        ('3.模擬退火法', simulated_annealing),
        ('4.梯度下降法', gradient_descent),
        ('5.貪婪演算法', greedy),
    ]
    results = []
    print(f'城市數量：{len(cities)}；城市編號：0～{len(cities) - 1}')
    print('所有距離均包含返回起點；耗時依電腦而異。\n')
    for name, solve in methods:
        started = time.perf_counter()
        route = solve(distances)
        elapsed = time.perf_counter() - started
        if sorted(route) != list(range(len(cities))):
            raise ValueError(f'{name} 產生不合法的路線')
        length = route_length(route, distances)
        results.append(dict(name=name, route=route, length=length, seconds=elapsed))
        print(f'{name}：距離={length:.2f}，耗時={elapsed:.4f} 秒')
        closed_route = route + [route[0]]
        print('路線：' + ' → '.join(map(str, closed_route)) + '\n')
    shortest = min(result['length'] for result in results)
    print('本次最短結果（不代表已證明全域最佳）：')
    for result in results:
        if math.isclose(result['length'], shortest, rel_tol=0, abs_tol=1e-8):
            print(f"  {result['name']}：{result['length']:.2f}")
    plot_results(cities, results, show=not args.no_show)


if __name__ == '__main__':
    main()

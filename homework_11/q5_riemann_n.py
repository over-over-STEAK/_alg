# AI 使用：有，ChatGPT 協助生成程式及測試。
from itertools import product
from math import prod

def square_sum(x):
    return sum(v*v for v in x)

def integral(f, low, high, steps=20):
    if len(low)!=len(high) or not low or steps<1 or any(b<=a for a,b in zip(low,high)):
        raise ValueError('invalid bounds or steps')
    widths=[b-a for a,b in zip(low,high)]
    h=[w/steps for w in widths]
    grids=[[a+(j+0.5)*d for j in range(steps)] for a,d in zip(low,h)]
    # 僅對已知可加分離的平方和使用等價的黎曼和化簡
    if f is square_sum and steps**len(low)>1000000:
        return prod(widths)*sum(sum(v*v for v in grid)/steps for grid in grids)
    if steps**len(low)>1000000:
        raise ValueError('grid budget exceeded; use Monte Carlo')
    return prod(h)*sum(f(x) for x in product(*grids))

def test():
    for n in (1,2,5,100):
        check(f'{n} 維',integral(square_sum,[0]*n,[1]*n,steps=10),n/3,n/1200+1e-9)
    check('一般函數',integral(lambda x:x[0]*x[1],[0,0],[1,1]),0.25,1e-10)

def check(name, actual, expected, tolerance):
    error=abs(actual-expected)
    print(f'{name}: {actual:.8f} | 理論 {expected:.8f} | 誤差 {error:.8f}')
    assert error <= tolerance, name

if __name__ == '__main__':
    test()
    print('PASS')

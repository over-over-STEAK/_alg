# AI 使用：有，ChatGPT 協助生成程式及測試。
import random
from math import prod

def integral(f, low, high, samples=50000, seed=42):
    if len(low)!=len(high) or not low or samples<1 or any(b<=a for a,b in zip(low,high)):
        raise ValueError('invalid bounds or samples')
    rng=random.Random(seed)
    return prod(b-a for a,b in zip(low,high))*sum(f([rng.uniform(a,b) for a,b in zip(low,high)]) for _ in range(samples))/samples

def test():
    for n in (1,2,5,100):
        check(f'{n} 維',integral(lambda x:sum(v*v for v in x),[0]*n,[1]*n),n/3,0.01*n**0.5)
    check('一般函數',integral(lambda x:x[0]*x[1],[0,0],[1,1]),0.25,0.01)

def check(name, actual, expected, tolerance):
    error=abs(actual-expected)
    print(f'{name}: {actual:.8f} | 理論 {expected:.8f} | 誤差 {error:.8f}')
    assert error <= tolerance, name

if __name__ == '__main__':
    test()
    print('PASS')

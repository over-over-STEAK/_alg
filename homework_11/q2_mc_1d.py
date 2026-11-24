# AI 使用：有，ChatGPT 協助生成程式及測試。
import random

def integral(f, low, high, samples=50000, seed=42):
    rng=random.Random(seed)
    return (high-low)*sum(f(rng.uniform(low,high)) for _ in range(samples))/samples

def test():
    check('x² 積分', integral(lambda x:x*x,0,1),1/3,0.01)
    check('常數積分', integral(lambda x:2,0,3),6,1e-10)

def check(name, actual, expected, tolerance):
    error=abs(actual-expected)
    print(f'{name}: {actual:.8f} | 理論 {expected:.8f} | 誤差 {error:.8f}')
    assert error <= tolerance, name

if __name__ == '__main__':
    test()
    print('PASS')

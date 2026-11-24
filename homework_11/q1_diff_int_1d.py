# AI 使用：有，ChatGPT 協助生成程式及測試。
def diff(f, x, h=1e-5):
    return (f(x+h)-f(x-h))/(2*h)

def integral(f, low, high, steps=1000):
    h=(high-low)/steps
    return h*(0.5*f(low)+sum(f(low+i*h) for i in range(1,steps))+0.5*f(high))

def test():
    f=lambda x:x*x
    check('微分', diff(f,2),4,1e-6)
    check('積分', integral(f,0,1),1/3,1e-6)

def check(name, actual, expected, tolerance):
    error=abs(actual-expected)
    print(f'{name}: {actual:.8f} | 理論 {expected:.8f} | 誤差 {error:.8f}')
    assert error <= tolerance, name

if __name__ == '__main__':
    test()
    print('PASS')

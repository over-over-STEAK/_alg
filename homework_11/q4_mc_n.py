# AI 使用：有，ChatGPT 協助生成程式及測試。
from q6_mc_generic import integral

def test():
    check('三維超體積',integral(lambda x:sum(v*v for v in x),[0]*3,[1]*3),1,0.02)
    check('常數超體積',integral(lambda x:2,[0,0],[2,3]),12,1e-10)

def check(name, actual, expected, tolerance):
    error=abs(actual-expected)
    print(f'{name}: {actual:.8f} | 理論 {expected:.8f} | 誤差 {error:.8f}')
    assert error <= tolerance, name

if __name__ == '__main__':
    test()
    print('PASS')

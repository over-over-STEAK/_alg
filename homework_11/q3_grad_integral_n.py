# AI 使用：有，ChatGPT 協助生成程式及測試。
from q5_riemann_n import integral

def gradient(f,x,h=1e-5):
    g=[]
    for i in range(len(x)):
        a,b=list(x),list(x)
        a[i]+=h; b[i]-=h
        g.append((f(a)-f(b))/(2*h))
    return g

def minimize(f,x,lr=0.1,steps=500,tol=1e-8):
    x=list(x)
    for _ in range(steps):
        g=gradient(f,x)
        if sum(v*v for v in g)**0.5<tol:
            break
        x=[v-lr*d for v,d in zip(x,g)]
    return x,f(x)

def test():
    f=lambda x:sum(v*v for v in x)
    for i,v in enumerate(gradient(f,[1,2,3])):
        check(f'偏微分 {i+1}',v,2*(i+1),1e-6)
    x,value=minimize(f,[3,-2,1])
    check('最小值',value,0,1e-10)
    print('最小值位置:',x)
    check('二維超體積',integral(f,[0,0],[1,1],steps=100),2/3,0.001)

def check(name, actual, expected, tolerance):
    error=abs(actual-expected)
    print(f'{name}: {actual:.8f} | 理論 {expected:.8f} | 誤差 {error:.8f}')
    assert error <= tolerance, name

if __name__ == '__main__':
    test()
    print('PASS')

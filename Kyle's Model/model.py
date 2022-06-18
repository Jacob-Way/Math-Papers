from matplotlib import pyplot as plt
import numpy as np
import sys

def main():
    test = np.zeros(1000)
    for i in range(len(test)):
        test[i] = simulate(1,0.1,2,1,100)[3][100]
    plt.hist(test,bins=100)
    plt.show()

def showsimulation():
    print('hi')

def multisim(p0,s0,p1,p2,su,N1,N2):
    '''
    p0: expected price
    s0: expected volatility (1-period)
    p1: insider price 1
    su: initial volatility of noise position
    N1: Number of steps to reach p1
    p2: insider price 2
    N2: Number of steps to each p2
    '''

    #define processes
    p = np.zeros(N2+1)
    pi1 = np.zeros(N2+1)
    pi2 = np.zeros(N2+1)
    u = np.zeros(N2+1)
    x1 = np.zeros(N2+1)
    x2 = np.zeros(N2+1)
    
    #Define strategies
    X1,P = getStrategies(p0,s0,p1,su,N1)
    X2,P = getStrategies(p0,s0,p2,su,N2)
    
    #Set initial values
    p[0] = p0
    u[0] = np.random.normal(0,su*N2**(-0.5),1)
    x1[0] = 0
    x2[0] = 0
    
    #Run process
    for i in range(1,N2+1):
        du = np.random.normal(0,su*N2**(-0.5),1)
        if(i<=N1): dx1 = X1(p[i-1],i)
        else: dx1 = 0
        dx2 = X2(p[i-1],i)
        dp = P(dx1+dx2,du)
        u[i] = du+u[i-1]
        x1[i] = dx1+x1[i-1]
        x2[i] = dx2+x2[i-1]
        p[i] = dp+p[i-1]
        if(i<=N1):pi1[i] = x1[i-1]*(p[i]-p[i-1])+pi1[i-1]
        else: pi1[i] = pi1[i-1]
        pi2[i] = x2[i-1]*(p[i]-p[i-1])+pi2[i-1]
    #return([u,x,p])
    return(u,x1,x2,p,pi1,pi2)
def simulate(p0,s0,p1,su,N):
    '''
    p0: expected price
    s0: expected volatility (1-period)
    p1: insider price
    su: initial volatility of noise position
    N: Number of steps
    '''

    #define processes
    p = np.zeros(N+1)
    pi = np.zeros(N+1)
    u = np.zeros(N+1)
    x = np.zeros(N+1)

    #Define strategies
    X,P = getStrategies(p0,s0,p1,su,N)

    #Set initial values
    p[0] = p0
    u[0] = np.random.normal(0,su*N**(-0.5),1)
    x[0] = 0
    
    #Run process
    for i in range(1,N+1):
        
        du = np.random.normal(0,su*N**(-0.5),1)
        dx = X(p[i-1],i)
        dp = P(dx,du)
        u[i] = du+u[i-1]
        x[i] = dx+x[i-1]
        p[i] = dp+p[i-1]
        pi[i] = x[i-1]*(p[i]-p[i-1])+pi[i-1]
    #return([u,x,p])
    return(u,x,p,pi)

def simulateV(p0,s0,p1,su,N,v):
    '''
    p0: expected price
    s0: expected volatility (1-period)
    p1: insider price
    su: initial volatility of noise position
    N: Number of steps
    v: volatility of noise volatility
    '''

    #define processes
    p = np.zeros(N+1)
    pi = np.zeros(N+1)
    u = np.zeros(N+1)
    s = np.zeros(N+1)
    x = np.zeros(N+1)

    #Define strategies
    X,P = getStrategies(p0,s0,p1,su,N)

    #Set initial values
    p[0] = p0
    s[0] = su
    u[0] = np.random.normal(0,su*N**(-0.5),1)
    x[0] = 0
    
    #Run process
    for i in range(1,N+1):
        
        du = np.random.normal(0,s[i-1]*N**(-0.5),1)
        dx = X(p[i-1],i)
        dp = P(dx,du)
        ds = np.random.normal(0,v*N**(-0.5),1)
        u[i] = du+u[i-1]
        x[i] = dx+x[i-1]
        p[i] = dp+p[i-1]
        s[i] = ds+s[i-1]
        pi[i] = x[i-1]*(p[i]-p[i-1])+pi[i-1]
    #return([u,x,p])
    return(u,x,p,pi,s)

def simulate2(p0,s0,p1,su,t0,t1,t2):
    #define processes
    p = np.zeros(t2)
    x = np.zeros(t2)
    u = np.zeros(t2)
    pi = np.zeros(t2)

    #Define strategies
    X,P = getStrategies(p0,s0,p1,su,t1-t0)
    
    #Set initial values
    u[0] = np.random.normal(0,su*(t1-t0)**(-0.5),1)
    x[0] = 0
    p[0] = p0

    #simulate start
    for i in range(1,t0):
        du = np.random.normal(0,su*(t1-t0)**(-0.5),1)
        dx = 0
        dp = P(dx,du)
        u[i] = du+u[i-1]
        x[i] = dx+x[i-1]
        p[i] = dp+p[i-1]
        pi[i] = x[i-1]*(p[i]-p[i-1])+pi[i-1]

    #Define strategies
    X,P = getStrategies(p[t0-1],s0,p1,su,t1-t0)

    #simulate middle
    for j in range(t1-t0):
        i = j+t0
        du = np.random.normal(0,su*(t1-t0)**(-0.5),1)
        dx = X(p[i-1],j)
        dp = P(dx,du)
        u[i] = du+u[i-1]
        x[i] = dx+x[i-1]
        p[i] = dp+p[i-1]
        pi[i] = x[i-1]*(p[i]-p[i-1])+pi[i-1]
    
    #simulate end
    for j in range(t2-t1):
        i=j+t1
        du = np.random.normal(0,su*(t1-t0)**(-0.5),1)
        dx = 0
        dp = P(dx,du)
        u[i] = du+u[i-1]
        x[i] = dx+x[i-1]
        p[i] = dp+p[i-1]
        pi[i] = pi[i-1]
    
    return(u,x,p,pi)

def getNoise(vol,vol_):
    dv = np.random.normal(0,vol_,1)
    du = np.random.normal(0,vol+dv,1)
    return dv,du

def getStrategies(p0,s0,p1,su,N):
    '''
    p0: expected price
    s0: expected volatility (entire period)
    p1: insider price
    su: realized volatility of noise position
    N: Number of steps
    '''
    
    #Define equilibrium variables
    a = 0.5*(su**2/s0)**0.5
    b = np.zeros(N+1)
    d = np.zeros(N+1)
    l = (s0/su**2)**0.5
    s = np.zeros(N+1)

    d[0] = 0.5*(su**2*s0)**0.5
    s[0] = s0
    b[0] = su**2*l/s0
    
    #Assign values to equilibrium variables
    for i in range(1,N+1):
        t = i/N
        if(t<1):
            s[i] = (1-t)*s0
            b[i] = su**2*l/s[i]
        else:
            b[i]=0
        d[i] = 0.5*(su**2*s0)**0.5*(1-t)

    #Define strategies
    def X(price,t):
        return b[t]*(p1-price)/N
    def P(dx,du):
        return l*(dx+du)
    
    return(X,P)

def plot(rows,columns,simulation):
    labels=["noise position","insider 1 position","insider 2 position","price","insider 1 profit","insider 2 profit"]
    for i in range(len(simulation)):
        plt.subplot(rows,columns,i+1)
        plt.plot(simulation[i])
        plt.title(labels[i])
    plt.show()
#plot(2,3,multisim(1,0.1,1,1,100,1000,1000))
trials = np.zeros(1000)
for i in range(1000):
    trials[i] = simulate(1,0.1,1,100,2000)[3][-1]
    if(i%50==0): print(i)
plt.hist(trials,bins=100)
plt.show()

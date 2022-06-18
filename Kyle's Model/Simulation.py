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
def simulate(p0,s0,p1,su,N):
    '''
    p0: expected price
    s0: expected volatility (1-period)
    p1: insider price
    su: realized volatility of noise position
    N: Number of steps
    '''

    #define processes
    p = np.zeros(N+1)
    x = np.zeros(N+1)
    u = np.zeros(N+1)
    pi = np.zeros(N+1)

    #define equilibrium variables
    a = 0.5*(su**2/s0)**0.5
    b = np.zeros(N+1)
    d = np.zeros(N+1)
    l = (s0/su**2)**0.5
    s = np.zeros(N+1)

    d[0] = 0.5*(su**2*s0)**0.5
    s[0] = s0
    b[0] = su**2*l/s0

    u[0] = np.random.normal(0,su*N**(-0.5),1)
    x[0] = 0
    p[0] = p0

    for i in range(1,N+1):
        #Assign values to equilibrium variables
        t = i/N
        if(t<1):
            s[i] = (1-t)*s0
            b[i] = su**2*l/s[i]
        else:
            b[i]=0
        d[i] = 0.5*(su**2*s0)**0.5*(1-t)
        #Calculate differences
        du = np.random.normal(0,su*N**(-0.5),1)
        dx = b[i]*(p1-p[i-1])/N
        dp = l*(dx+du)
        #Assign values to processes
        u[i] = u[i-1]+du
        x[i] = dx+x[i-1]
        p[i] = dp+p[i-1]
        pi[i] = x[i-1]*(p[i]-p[i-1])+pi[i-1]
    #return([u,x,p])
    return(u,x,p,pi)

def plot(rows,columns,simulation):
    labels=["noise position","insider position","price","insider profit"]
    for i in range(len(simulation)):
        plt.subplot(rows,columns,i+1)
        plt.plot(simulation[i])
        plt.title(labels[i])
    plt.show()
def main2():
    ##while(1==1):
    ##    if(input()=="x"):
    ##        break
    ##    else:
    ##        plot(2,2,simulate(1,0.1,1,1,100))
    tests = np.zeros(1000)
    for i in range(1000):
        tests[i]=simulate(1,0.1,1.1,1,100)[3][100]
plot(2,2,simulate(1,0.1,1.1,1,100))

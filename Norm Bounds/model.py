from matplotlib import pyplot as plt
import numpy as np
import sys

def spectralNorm(M):
    return np.linalg.svd(M)[1][0]
def suBound(M):
    #Lower bound 2.4
    return ((np.matmul(np.transpose(np.conjugate(M)),M)).sum()/len(M))**0.5
def colBound(M):
    n = len(M[0])
    bound = 0
    for i in range(n):
        for j in range(n):
            ai = M[:,i]
            aj = M[:,j]
            if(j!=i):
                bound = max(bound,eNorm(ai)**2+eNorm(aj)**2+((eNorm(ai)**2-eNorm(aj)**2)**2+4*np.abs(np.matmul(np.conjugate(np.transpose(ai)),aj))**2)**0.5)
    return bound**0.5/2**0.5
def eNorm(v):
    return sum(np.power(v,2))**0.5
diffs = np.zeros(10000)
for i in range(10000):
    M = np.random.normal(0,1,[10,10])
    diffs[i]=spectralNorm(M)-suBound(M)
plt.hist(diffs,bins = 100)
plt.show()

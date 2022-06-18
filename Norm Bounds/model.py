from matplotlib import pyplot as plt
import numpy as np
import sys

def spectralNorm(M):
    return np.linalg.svd(M)[1][0]
def suBound(M):
    #Lower bound 2.4
    return ((np.matmul(np.transpose(np.conjugate(M)),M)).sum()/len(M))**0.5
diffs = np.zeros(10000)
for i in range(10000):
    M = np.random.normal(0,1,[10,10])
    diffs[i]=spectralNorm(M)-suBound(M)
plt.hist(diffs,bins = 100)
plt.show()

from matplotlib import pyplot as plt
import numpy as np
import sys

def testMatrix(m,n):
    return np.random.uniform(0,1,[m,n])+1j*np.random.uniform(0,1,[m,n])
def energy(M):
    svd = np.linalg.svd(M)[1]
    return svd.sum()
def norm(M,n):
    return np.power(np.absolute(M),n).sum()**(1/n)
def trace(M):
    m = len(M)
    s = 0
    for i in range(m):
        s=s+M[i,i]
    return s
def bounds(M):
    m=len(M)
    n=len(M[0])
    upper = norm(M,1)/(m*n)**0.5 + ((m-1)*(trace(np.matmul(M,np.transpose(np.conjugate(M))))-norm(M,1)**2/m/n))**0.5
    return abs(upper)



def testEnergies():
    tests = np.zeros(1000)
    for i in range(1000):
        tests[i] = energy(testMatrix(10,10))
    plt.hist(tests,bins=100)
    plt.show()
testBounds = np.zeros(1000)
testEnergies = np.zeros(1000)
for i in range(1000):
    M = testMatrix(10,10)
    testBounds[i]=bounds(M)
    testEnergies[i] = energy(M)
plt.hist(testBounds-testEnergies,bins=100)
plt.show()

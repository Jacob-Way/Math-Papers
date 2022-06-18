from matplotlib import pyplot as plt
import numpy as np
import sys

def testMatrix(m,n):
    return np.random.uniform(0,1,[m,n])+1j*np.random.uniform(0,1,[m,n])
def energy(M):
    svd = np.linalg.svd(M)[1]
    return svd.sum()
def norm(M):
    m = 0
    for i in range(len(M[0])):
        m = max(m,sum(abs(M[:,i])))
    return m
def trace(M):
    m = len(M)
    s = 0
    for i in range(m):
        s=s+M[i,i]
    return s
def bounds(M):
    m=len(M)
    n=len(M[0])
    upper = norm(M)/(m*n)**0.5 + ((m-1)*(trace(np.matmul(M,np.transpose(np.conjugate(M))))-norm(M)**2/m/n))**0.5
    sigs = np.linalg.svd(M)[1]
    sig1 = sigs[0]
    sig2 = sigs[1]
    lower = sig1 + (trace(np.matmul(M,np.transpose(np.conjugate(M))))-sig1**2)/sig2
    return abs(lower),abs(upper)

def testEnergies(n):
    tests = np.zeros(n)
    for i in range(n):
        tests[i] = energy(testMatrix(10,10))
    plt.hist(tests,bins=100)
    plt.show()
def testBounds(n):
    testBounds = np.zeros(n)
    testEnergies = np.zeros(n)
    for i in range(n):
        M = testMatrix(10,10)
        testBounds[i]=bounds(M)[1]
        testEnergies[i] = energy(M)
    plt.hist(testBounds-testEnergies,bins=100)
    plt.show()
def allBounds(n):
    lowers = np.zeros(n)
    actuals = np.zeros(n)
    uppers = np.zeros(n)
    for i in range(n):
        M = np.random.normal(0,1,[20,20])
        l,u = bounds(M)
        lowers[i] = l
        actuals[i] = energy(M)
        uppers[i] = u
    plt.subplot(3,1,1)
    plt.hist(lowers,bins=100)
    plt.hist(actuals,bins=100)
    plt.hist(uppers,bins=100)
    plt.subplot(3,1,2)
    plt.hist(uppers-actuals,bins=100)
    plt.subplot(3,1,3)
    plt.hist(actuals-lowers,bins=100)
    plt.show()
allBounds(10000)

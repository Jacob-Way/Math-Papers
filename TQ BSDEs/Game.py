from matplotlib import pyplot as plt
import numpy as np
import sys
#step 1
#insider and noise traders simultaniously choose orders
    #insider knows his own previous trades and true liquidation value, nothing else
    #quantity traded by noise traders is independent of previous and current trades by either party
    #insider wants to maximize total profit over the whole time he is trading
# Market maker sets a price, trades enough to make the markets clear
    #market makers have information about current, past aggregate quantities traded ("order flow")
    #price fluctuations are due to order flow changes
    #prices are equal to expected liquidation value conditioned on current information
#other
    # prices and quantities are linear functions of observations at equilibrium
    # quantity traded by noise traders follows bm -> price does, too
    # doubling of noise doubles the volume traded by all parties, and therefore benefits the insider
    # tightness: cost of turning around a position in short time
    # depth: size of an order flow change needed to change prices
    # resiliency: speed at which prices recover from random shocks
#Notation
    #v_ is ex-post liquidation value of a risky asset. it is normally distributed with mean p0, variance S0
    #Quantity traded by noise traders u_ is normally distributed with mean 0 and variance su
    #v_ and u_ are independent
    #quantity traded by insider is x_ and price is p_
    #step 1: v_, u_ realized, x_ is determined by insider observing v_ and not u_
    #X is the insider's strategy, assigning each quantity traded to a probability distribution of v_
    #x_ = X(v_)
    #step 2: p_ determined to satisfy u_ + x_
    #pricing rule P is a meas. real func p_ = P(x_+u_)
    #pi_ is profits of insider, pi_ = (v_-p_)x_.
    #p_ and pi_ are functions of both X and P.
    #equilibrium is a pair X and P s.t.
        #X is the best trading strategy given P and v
        #p_ is equal to the expectation of v_ given volume information
    #X and P being linear functions is an equilibrium
#asset true value, mean and standard deviation:
##v_=110
##p0=100
##S0=10
###standard deviation of noise trading orders:
##su=100
###Other constants
##b=(su**2/S0)**0.5
##l=2*(su**2/S0)**(-0.5)
###equilibrium functions
##def P(phist,i,volume):
##    return p0+l*(volume)
##def X(vhist,i):
##    return b*(v_-p0)
##N = 100

p_0=100
v_=110
su=10
N=100
#processes
p_ = np.zeros(N)
x_ = np.zeros(N)
u_ = np.zeros(N)
X = np.zeros(N)
P = np.zeros(N)

l = np.random.random(N)*10
b = np.random.random(N)*10
a = np.random.random(N)*10
d = np.random.random(N)*10
S = np.random.random(N)*10
#assign values to b,l,a,d,S
for iteration in range(10000):
    for n in range(N):
        if(n>0):
            a[n-1]=min(1000,1/(4*l[n]*(1-a[n]*l[n])))
            d[n-1]=max(0.01,min(1000,d[n]+a[n]*l[n]**2*su**2/N))
            S[n]=max(1,min(1000,(1-b[n]*l[n]/N)*S[n-1]))
        b[n]=min(1000,(1-2*a[n]*l[n])/(2*l[n]*(1-a[n]*l[n]))/N)
        l[n]=min(1000,b[n]*S[n]/su**2)
        if(n==N-1):
            a[n]=0
            d[n]=0
        #if(iteration%10000==0):
            #print(l[n]*(1-a[n]*l[n]))
aerror = 0
derror = 0
Serror = 0
berror = 0
lerror = 0
for n in range(N):
    if(n>0):
        aerror = abs(a[n-1]-1/(4*l[n]*(1-a[n]*l[n])))
        derror = abs(d[n-1]-d[n]+a[n]*l[n]**2*su**2/N)
        Serror = abs(S[n]-(1-b[n]*l[n]/N)*S[n-1])
    berror = abs(b[n]-(1-2*a[n]*l[n])/(2*l[n]*(1-a[n]*l[n]))/N)
    lerror = abs(l[n]-b[n]*S[n]/su**2)
##for i in range(N):
##    #assign noise actions
##    du_ = np.random.normal(0,su*(N)**(-0.5),1)
##    if(i==0):u_[0]=du_
##    else:u_[i]=u[i-1]+du_
##    #assign insider actions
##    if(i==0):
##        dx_ = b[i]*(v_-p_0)
##        x_[i]=dx_
##    else:
##        dx_ = b[i]*(v_-p_[i-1])
##        x_[i]=dx_+x[i-1]
##    #assign pricing actions
##    dp_ = l[i]*(dx_+du_)
##    if(i==0):
##        p_[i] = dp_
##    else:
##        p_[i] = dp_+p_[i-1]
print(lerror)
print(berror)
print(aerror)
print(derror)
print(Serror)
    
plt.plot(l)
plt.show()
plt.plot(b)
plt.show()
plt.plot(a)
plt.show()
plt.plot(d)
plt.show()
plt.plot(S)
plt.show()











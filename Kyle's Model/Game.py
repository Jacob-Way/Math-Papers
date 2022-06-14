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

p0=3749
S0=400
v_=3750
su=2950000
N=500
#processes
p_ = np.zeros(N)
p_[0]=p0
x_ = np.zeros(N)
u_ = np.zeros(N)
X = np.zeros(N)
P = np.zeros(N)
#equilibrium variables
l=np.ones(N)*(S0/su**2)**0.5
b=np.zeros(N)
a=np.zeros(N)
d=np.zeros(N)
S=np.zeros(N)
#assign values to b,l,a,d,S
for i in range(N):
    t=i/N
    S[i]=(1-t)*S0
    b[i]=su**2*l[i]/S[i]
    a[i]=0.5*(su**2*S0)**0.5
    d[i]=a[i]*(1-t)
#Carry out simulation
for i in range(N):
    #assign noise actions
    du_ = np.random.normal(0,su*(N)**(-0.5),1)
    if(i==0):u_[0]=du_
    else:u_[i]=u_[i-1]+du_
    #assign insider actions
    if(i==0):
        dx_ = b[i]*(v_-p0)/N
        x_[i]=dx_
    else:
        dx_ = b[i]*(v_-p_[i-1])/N
        x_[i]=dx_+x_[i-1]
    #assign pricing actions
    dp_ = l[i]*(dx_+du_)
    if(i==0):
        p_[i] = dp_+p_[0]
    else:
        p_[i] = dp_+p_[i-1]
dx_ = np.zeros(N)
pi_ = np.zeros(N)
pr = np.zeros(N)
for i in range(N):
    if(i==0):
        pi_[0]=0
        dx_[0]=x_[0]
    else:
        pi_[i]=x_[i-1]*(p_[i]-p_[i-1])+pi_[i-1]
        dx_[i]=x_[i]-x_[i-1]
plt.subplot(2,2,1)
plt.plot(x_,label="insider position (# of stocks)")
plt.legend()
plt.subplot(2,2,2)
plt.plot(u_,label="noise position (# of stocks)")
plt.legend()
plt.subplot(2,2,3)
plt.plot(p_,label="price ($)")
plt.legend()
plt.subplot(2,2,4)
plt.plot(pi_,label="insider profit ($)")
plt.legend()
plt.show()









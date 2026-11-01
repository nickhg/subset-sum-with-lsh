import sys; sys.path.insert(0,'/home/claude/work')
import numpy as np
from scipy.optimize import minimize
from bcj_lsf import lp, tree
k=int(sys.argv[1]) if len(sys.argv)>1 else 3
def f(z):
    eps=list(np.abs(z[:k])); fl=[z[k+8*j:k+8*(j+1)] for j in range(k)]
    return lp(eps,fl)[0]
rng=np.random.default_rng(int(sys.argv[2]) if len(sys.argv)>2 else 0)
best=(9,None)
base=[0.0267,0.0169,0.0029,0.0005,0.0001][:k]
for t in range(int(sys.argv[3]) if len(sys.argv)>3 else 8):
    e0=np.array(base)*rng.uniform(0.7,2.2,k)
    z0=np.concatenate([e0,rng.normal(0,0.3,8*k)])
    r=minimize(f,z0,method='Powell',options=dict(maxiter=60000,xtol=1e-7,ftol=1e-10))
    r=minimize(f,r.x,method='Nelder-Mead',options=dict(maxiter=20000,xatol=1e-8,fatol=1e-11))
    if r.fun<best[0]: best=(r.fun,r.x)
    print(t,round(r.fun,5),np.round(np.abs(r.x[:k]),4),flush=True)
np.save(f'best_bcj_{k}.npy',best[1]); print("BEST",round(best[0],5))

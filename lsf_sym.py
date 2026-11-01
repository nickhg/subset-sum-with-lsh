import sys; sys.path.insert(0,'/home/claude/work')
import numpy as np
from scipy.optimize import minimize
from lsf_types import *
import lsf_types as LT

def sm(v): e=np.exp(v-np.max(v)); return e/e.sum()
def build(z,m):
    if m==3:   # labels N,L,R ; mirror swaps L,R
        pi=sm(np.array([z[0],z[1],z[1]])); q00=sm(np.array([z[2],z[3],z[3]]))
        q10=sm(np.array([z[4],z[5],z[6]])); q01=q10[[0,2,1]]
    else:      # labels N,L,R,B
        pi=sm(np.array([z[0],z[1],z[1],z[2]])); q00=sm(np.array([z[3],z[4],z[4],z[5]]))
        q10=sm(np.array([z[6],z[7],z[8],z[9]])); q01=q10[[0,2,1,3]]
    # pack into evaluate's format (log-probs)
    return np.concatenate([np.log(pi),np.log(q00),np.log(q10),np.log(q01)])
def f(z,m,ks): return evaluate(build(z,m),m,ks=ks)
rng=np.random.default_rng(0)
ks_c=np.linspace(0.0005,W*W*1.6,9); ks_f=np.linspace(0.0002,W*W*1.8,40)
for m,npar in ((4,10),):
    best=(9,None)
    for t in range(12):
        r=minimize(f,rng.normal(0,1.5,npar),args=(m,ks_c),method='Nelder-Mead',options=dict(maxiter=1500,xatol=1e-5,fatol=1e-7))
        if r.fun<best[0]: best=(r.fun,r.x); print(m,t,round(r.fun,5),flush=True)
    r=minimize(f,best[1],args=(m,ks_f),method='Nelder-Mead',options=dict(maxiter=4000,xatol=1e-8,fatol=1e-10))
    c,terms,wk,(pi,cond)=evaluate(build(r.x,m),m,ks=ks_f,detail=True)
    print(f"labels={m}: cost {c:.5f} {{ {', '.join(f'{k}:{v:.5f}' for k,v in terms.items())} }} worst k={wk:.4f}",flush=True)
    print("  pi",np.round(pi,3),"Q|00",np.round(cond[0],3),"Q|10",np.round(cond[1],3),flush=True)

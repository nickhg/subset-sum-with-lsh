"""usage: gen_opt.py DIGITS(e.g. -2,-1,0,1,2) depth seed p|f  [init.npy]"""
import sys; sys.path.insert(0,'/home/claude/work')
import numpy as np, warnings; warnings.filterwarnings("ignore")
from scipy.optimize import minimize
from gen_lsf import Model
D=[int(x) for x in sys.argv[1].split(',')]; k=int(sys.argv[2]); seed=int(sys.argv[3]); use_f=sys.argv[4]=='f'
M=Model(D); rng=np.random.default_rng(seed); ns=M.nsplit; nf=M.nfilt
tag=f"{''.join('m' if d<0 else '' for d in D)}{len(D)}_{k}_{sys.argv[4]}_{seed}"
def unpack(z):
    P=z[:k*ns].reshape(k,ns); F=[z[k*ns+nf*j:k*ns+nf*(j+1)] for j in range(k)] if use_f else None
    return P,F
f=lambda z: M.lp(*unpack(z))[0]
if len(sys.argv)>5:
    z0=np.load(sys.argv[5]); 
    if len(z0)<k*ns+(nf*k if use_f else 0): z0=np.concatenate([z0,rng.normal(0,0.3,k*ns+(nf*k if use_f else 0)-len(z0))])
else:
    z0=rng.normal(-3,1,k*ns)
    if use_f: z0=np.concatenate([z0,rng.normal(0,0.3,nf*k)])
best=(f(z0),z0); print(tag,"splits/level",ns,"filter params/level",nf,"start",round(best[0],5),flush=True)
for t in range(200):
    z=best[1]+(np.concatenate([rng.normal(0,0.3,k*ns),rng.normal(0,0.3,len(z0)-k*ns)]) if t>0 else 0)
    r=minimize(f,z,method='Powell',options=dict(maxiter=40000,xtol=1e-7,ftol=1e-11))
    r=minimize(f,r.x,method='Nelder-Mead',options=dict(maxiter=10000,xatol=1e-8,fatol=1e-12))
    if r.fun<best[0]-1e-9: best=(r.fun,r.x); np.save(f'gen_{tag}.npy',best[1])
    print(t,round(r.fun,5),"best",round(best[0],5),flush=True)

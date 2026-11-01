"""Add multi-table / local-rerun freedom: t_j >= 0 = log2(#independent tables at level j),
allowing l_j <= rho_j + t_j. Every cost at level i is paid once per table of every
ancestor level m <= i, i.e. gets + sum_{m<=i} t_m."""
import sys; sys.path.insert(0,'/home/claude/work')
import itertools, numpy as np
from scipy.optimize import linprog, minimize
from hgj_multi import levels, lp_solve

def lp_tables(cs):
    k=len(cs); H,rho,p=levels(cs)
    # vars: l_1..l_k (0..k-1), t_1..t_k (k..2k-1), T (2k)
    nv=2*k+1; T=2*k; A=[];b=[]
    def row(d,rhs):
        v=np.zeros(nv)
        for i,x in d: v[i]+=x
        A.append(v); b.append(rhs)
    tsum=lambda i:[(k+m-1,-1) for m in range(1,i+1)]   # -sum t_m (moved to lhs as -T - ... )
    for j in range(1,k+1):
        if j>=2: row([(j-1,1),(j-2,-1)],0)
        row([(j-1,1),(k+j-1,-1)],rho[j])
        # T >= H_j - l_j + sum t  ->  -l_j + sum t - T <= -H_j
        row([(j-1,-1),(T,-1)]+[(i,-c) for i,c in tsum(j)],-H[j])
        d=[(j-1,-1),(T,-1)]+[(i,-c) for i,c in tsum(j)]; rhs=-2*H[j]
        if j==1: rhs+=1.0
        else: d.append((j-2,-1))
        row(d,rhs)
    row([(T,-1)]+[(i,-c) for i,c in tsum(k)],-0.5*H[k])
    res=linprog(np.eye(nv)[T],A_ub=np.array(A),b_ub=np.array(b),bounds=[(0,1)]*k+[(0,1)]*k+[(0,1)],method='highs')
    return res.fun, res.x

for k,grid in [(2,41),(3,15),(4,9)]:
    g=np.linspace(0.05,1.0,grid)
    top=min((lp_tables(list(cs))[0],cs) for cs in itertools.product(g,repeat=k))
    r=minimize(lambda v: lp_tables(list(np.clip(v,0.02,1)))[0], np.array(top[1]), method='Nelder-Mead',options=dict(xatol=1e-5,fatol=1e-7,maxiter=3000))
    cs=list(np.clip(r.x,0.02,1)); Tt,x=lp_tables(cs)
    print(f"depth {k}: with tables {Tt:.4f}  (no tables {lp_solve(cs)[0]:.4f})  c={np.round(cs,3)}  t={np.round(x[k:2*k],4)}")

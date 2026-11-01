import sys; sys.path.insert(0,'/home/claude/work')
import numpy as np, warnings; warnings.filterwarnings("ignore")
from bbss_lsf import *
k=3; z=np.load(sys.argv[1]); params=[tuple(r) for r in z[:9].reshape(3,3)]
fl=[z[9+NPAR*j:9+NPAR*(j+1)] for j in range(k)]
T,x=lp2(params,fl); lev=tree(params); c=[1.0]+list(x[:3]); L=list(x[3:6])
Tp,_=lp2(params,None)
print(f"T with filters {T:.5f} | same digit params without filters {Tp:.5f}")
for j in range(1,k+1):
    ch=lev[j]['child']; e,f,g=lev[j]['efg']
    print(f" level {j}: digits -1:{ch[-1]:.4f} 0:{ch[0]:.4f} 1:{ch[1]:.4f} 2:{ch[2]:.4f}  (e,f,g)=({e:.4f},{f:.4f},{g:.4f})  reps {lev[j]['rho']:.4f}  c_j {c[j]:.4f}  list {L[j-1]:.4f}")
for j in range(1,k+1):
    pairs=2*L[j-1]-(c[j-1]-c[j]); r12,r1,r2,ex=filter_terms(lev[j],fl[j-1])
    pi,cond=filt(fl[j-1]); tau=lev[j]['tau']; Ql=(tau[:,None]*cond).sum(0)
    eff=sum(tau[t]*kl(cond[t],Ql) for t in range(NT) if tau[t]>0)
    out = L[j-2] if j>=2 else 2*L[0]-(1-c[1])+lev[1]['Hpar']+lev[1]['rho']-2*lev[1]['H']
    print(f" merge of level-{j} lists: unfiltered pairs {pairs:.4f} | LSF entries {L[j-1]+r12-min(r1,r2):.4f} passing {pairs+ex:.4f} | output {out:.4f} | log2 tables {eff:.4f}")
print(" base half-lists", round(0.5*lev[k]['H'],4), "| top expected #solutions (log)", round(2*L[0]-(1-c[1])+lev[1]['Hpar']+lev[1]['rho']-2*lev[1]['H'],5))
print(" checks: L_j + c_j <= H_j:", [round(L[j-1]+c[j]-lev[j]['H'],5) for j in range(1,k+1)])

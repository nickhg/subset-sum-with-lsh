import sys; sys.path.insert(0,'/home/claude/work')
import numpy as np
from gen_lsf import Model
M4=Model([-1,0,1,2]); M5=Model([-2,-1,0,1,2]); k=3
def emb(z4, filt):
    out=[]
    for j in range(k):
        r4=dict(zip([p for d in M4.D for p in M4.upairs[d][1:]], z4[j*M4.nsplit:(j+1)*M4.nsplit]))
        out+= [r4.get(p,-30.0) for d in M5.D for p in M5.upairs[d][1:]]
    if filt:
        for j in range(k):
            f4=z4[k*M4.nsplit+j*M4.nfilt:k*M4.nsplit+(j+1)*M4.nfilt]
            sym4={M4.types[t]:f4[1+i] for i,t in enumerate(M4.sym)}
            asy4={M4.types[t]:f4[1+len(M4.sym)+2*i:3+len(M4.sym)+2*i] for i,t in enumerate(M4.asym)}
            f5=[f4[0]]+[sym4.get(M5.types[t],0.0) for t in M5.sym]
            for t in M5.asym: f5+=list(asy4.get(M5.types[t],[0.0,0.0]))
            out+=f5
    return np.array(out)
z4=np.load(sys.argv[1]); z5=emb(z4, sys.argv[3]=='f'); np.save(sys.argv[2],z5)
from gen_lsf import Model as _
P4=z4[:k*M4.nsplit].reshape(k,-1); P5=z5[:k*M5.nsplit].reshape(k,-1)
F4=[z4[k*M4.nsplit+M4.nfilt*j:k*M4.nsplit+M4.nfilt*(j+1)] for j in range(k)] if sys.argv[3]=='f' else None
F5=[z5[k*M5.nsplit+M5.nfilt*j:k*M5.nsplit+M5.nfilt*(j+1)] for j in range(k)] if sys.argv[3]=='f' else None
print("4-digit",round(M4.lp(P4,F4)[0],5)," embedded 5-digit",round(M5.lp(P5,F5)[0],5))

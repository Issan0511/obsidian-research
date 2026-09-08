from pathlib import Path
import numpy as np, itertools, json
import argparse
parser=argparse.ArgumentParser(description="Descriptive c=0 moment audit; no training.")
parser.add_argument("--data-root",type=Path,default=Path("/home/issan/Projects/obsidian-research-data/act_offset_review_0908"))
parser.add_argument("--out",type=Path,default=Path(__file__).with_name("moment_balance_c0.json"))
args=parser.parse_args()
root=args.data_root
bits=np.array(list(itertools.product([-.5,.5],repeat=5)))
records=[]; collected={k:[] for k in ["P","N","v","cross","zbar","logged_moment","time"]}
for f in sorted((root/"tail/logs_tail").glob("LRoff0_1216_seed*.npz")):
    with np.load(f,allow_pickle=False) as d:
        idx=np.flatnonzero((d["step"]>=4510000)&(d["step"]%10000==0))
        widx=np.searchsorted(d["layer1_w_free_step"],d["step"][idx])
        zbar=d["layer1_zbar"][idx].astype(float)
        z=zbar[:,:,None]+np.einsum("tuj,pj->tup",d["layer1_w_free"][widx].astype(float),bits)
        P=np.maximum(z,0).mean(-1); N=np.maximum(-z,0).mean(-1)
        cross=(d["layer1_zmin"][idx]<=0)&(d["layer1_zmax"][idx]>0)
        v=d["layer1_v_unit"][idx].astype(float)
        values={"P":P,"N":N,"v":v,"cross":cross,"zbar":zbar,"logged_moment":d["layer1_m_phidphi"][idx],"time":d["step"][idx]}
        for k,val in values.items():collected[k].append(val)
        seedrow={"file":f.name,"phi_mean_mean":float(np.mean(P-.1*N)),"phidphi_mean":float(np.mean(P-.01*N)),
                 "weighted_phidphi_mean":float(np.mean(v*v*(P-.01*N))),
                 "positive_share":float((z>0).mean()),
                 "max_moment_error":float(np.max(np.abs(P-.01*N-d["layer1_m_phidphi"][idx])))}
        records.append(seedrow)
assert len(records)==10, "Expected ten seeds"
assert all(len(x)==50 for x in collected["time"]), "Expected fifty endpoints per seed"
assert max(r["max_moment_error"] for r in records)<2e-6, "Support/moment mismatch"
a={k:np.stack(v) for k,v in collected.items()}
result={"scope":"c=0, a=0.1, 10 seeds, last 50 task endpoints 4.51M..5M, 100 units","by_seed":records,"groups":{}}
for name,mask in [("all",np.ones_like(a["cross"],bool)),("crossing",a["cross"]),("all_negative",(a["P"]==0)&(a["N"]>0))]:
    P=a["P"][mask]; N=a["N"][mask]; v=a["v"][mask]
    result["groups"][name]={"events":len(P),"P_mean":float(P.mean()),"N_mean":float(N.mean()),
       "mean_balance_ratio_P_over_aN":float(P.sum()/(.1*N.sum())),
       "self_moment_balance_ratio_P_over_a2N":float(P.sum()/(.01*N.sum())),
       "weighted_self_balance_ratio":float(np.sum(v*v*P)/np.sum(v*v*.01*N)),
       "phi_mean_median":float(np.median(P-.1*N)),
       "phidphi_median":float(np.median(P-.01*N)),
       "fraction_self_up":float(np.mean(P-.01*N<0)),
       "zbar_mean":float(a["zbar"][mask].mean())}
args.out.write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

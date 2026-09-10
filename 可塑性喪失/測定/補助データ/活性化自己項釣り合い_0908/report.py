#!/usr/bin/env python3
"""Derived summaries/figures for audit.py. Existing checkpoint data only."""
from pathlib import Path
import csv,json,hashlib,subprocess
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path('/home/issan/Projects/obsidian-research-data/activation_self_balance_0908')
rows=list(csv.DictReader((P/'units.csv').open()))
summ=json.loads((P/'summary.json').read_text())
seeds=list(csv.DictReader((P/'seed_summary.csv').open()))
wins=list(csv.DictReader((P/'animation_windows.csv').open()))
def get(label,step=5000000):
 return [r for r in rows if r['label']==label and int(r['step'])==step]
def vals(r,k):return np.array([float(x[k]) for x in r])
extra=[]
for s in summ:
 r=get(s['label'],s['step']); ratios=[]
 v=vals(r,'v');mp=vals(r,'m_positive');mn=vals(r,'m_negative_abs')
 weighted=abs(np.sum(v*v*(mp-mn)))/max(np.sum(v*v*(mp+mn)),1e-300)
 for seed in sorted(set(x['seed'] for x in r),key=int):
  t=[x for x in r if x['seed']==seed];vv=vals(t,'v');pp=vals(t,'m_positive');nn=vals(t,'m_negative_abs')
  ratios.append(abs(np.sum(vv*vv*(pp-nn)))/max(np.sum(vv*vv*(pp+nn)),1e-300))
 rates=[float(x['near_balance_0.1_frac']) for x in seeds if x['label']==s['label'] and int(x['step'])==s['step']]
 item={'label':s['label'],'step':s['step'],'pooled_v2_imbalance':weighted,
       'seed_v2_imbalance_q25_median_q75':np.percentile(ratios,[25,50,75]).tolist(),
       'seed_near_balance_q25_median_q75':np.percentile(rates,[25,50,75]).tolist(),
       'zero_moment_frac':float(np.mean(mp+mn==0))}
 extra.append(item)
(P/'aggregation_audit.json').write_text(json.dumps(extra,indent=2))
# SiLU duplicate source must not count as independent replicate.
si=get('silu100');sg=get('silu100_gd')
duplicate=all(a[k]==b[k] for a,b in zip(si,sg) for k in a if k!='label')
assert duplicate
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
labels=['leaky100','elu100','silu100','gelu100','snake_075','snake_10']
names=['Leaky 0.1 / width 100','ELU / width 100','SiLU / width 100','GELU / width 100','Snake 0.75 / width 5','Snake 1.0 / width 5']
fig,axes=plt.subplots(2,3,figsize=(13,8),layout='constrained')
for ax,label,name in zip(axes.flat,labels,names):
 r=get(label); mp=vals(r,'m_positive');mn=vals(r,'m_negative_abs')
 quiet=mp+mn<=1e-8
 floor=1e-16
 ax.scatter(np.maximum(mn[~quiet],floor),np.maximum(mp[~quiet],floor),s=11,alpha=.38,c='#2467aa',rasterized=True)
 ax.scatter(np.maximum(mn[quiet],floor),np.maximum(mp[quiet],floor),s=11,alpha=.35,c='#aaa',rasterized=True)
 xx=np.geomspace(floor,1e2,500)
 ax.plot(xx,xx,color='#222',lw=1)
 ax.fill_between(xx,xx*.9/1.1,xx*1.1/.9,color='#5db99b',alpha=.3)
 ax.set(xscale='log',yscale='log',xlim=(floor/3,1e2),ylim=(floor/3,1e2),
        xlabel='Negative self moment (magnitude)',ylabel='Positive self moment')
 s=next(s for s in summ if s['label']==label and s['step']==5000000)
 ax.set_title(name+'\nnear balance %.1f%%; tiny moment %.1f%%'%(100*s['near_balance_0.1_frac'],100*s['quiet_moment_frac']))
 ax.set_xticks([1e-16,1e-12,1e-8,1e-4,1]);ax.set_yticks([1e-16,1e-12,1e-8,1e-4,1])
 ax.grid(alpha=.12)
fig.suptitle("5M checkpoints: each dot is ONE unit over all 32 inputs\nBand: imbalance <= 0.1. Gray: total absolute moment <= 1e-8. Display values below 1e-16 are clipped.",fontsize=12)
fig.savefig(P/'self_moment_balance.png',dpi=150)
fig.savefig(P/'self_moment_balance.pdf')
plt.close(fig)
labels=['leaky100','elu100','silu100','gelu100','snake_025','snake_075','snake_10','snake_80']
names=['Leaky 0.1 / width 100','ELU / width 100','SiLU / width 100','GELU / width 100','Snake 0.25 / width 5','Snake 0.75 / width 5','Snake 1.0 / width 5','Snake 8.0 / width 5']
fig,axes=plt.subplots(2,4,figsize=(15,7),layout='constrained')
for ax,label,name in zip(axes.flat,labels,names):
 r=[x for x in wins if x['label']==label]
 t=vals(r,'task_end');med=vals(r,'z_q50')
 ax.fill_between(t,vals(r,'z_q10'),vals(r,'z_q90'),color='#2467aa',alpha=.18)
 ax.plot(t,med,color='#2467aa',lw=1.5)
 for task in [100,500]:ax.axvline(task,color='#777',ls=':',lw=.8)
 ax.set_title(name);ax.set_xlabel('Task (window end)');ax.set_ylabel('Mean preactivation z')
 ax.grid(alpha=.15);ax.axhline(0,color='#888',lw=.6)
fig.suptitle('Animation distributions: pooled 10-task endpoints, median and 10-90% range\nDotted lines mark checkpoint anchors; no self-moment history is inferred from these trajectories.',fontsize=12)
fig.savefig(P/'animation_trajectories.png',dpi=150);plt.close(fig)
source_paths=[
 '/home/issan/Projects/claude/snake_out_0904/src/nets.py',
 '/tmp/claude-1000/-home-issan-Projects-claude/5144225e-c906-48ea-af81-1e2c8a536462/scratchpad/actanim_smooth_0904.py',
 '/tmp/claude-1000/-home-issan-Projects-claude/5144225e-c906-48ea-af81-1e2c8a536462/scratchpad/actplot_smooth_0904.py',
 '/tmp/claude-1000/-home-issan-Projects-claude/44dd8ade-4c36-41aa-a180-d37f33fd34e9/scratchpad/asweep_anim.py']
v=json.loads((P/'verification.json').read_text())
meta={'status':'post-hoc descriptive analysis; no intervention or training',
 'anchors':[0,1000000,5000000],'unit_checkpoint_rows':len(rows),'seed_checkpoint_checks':v['n_checks'],
 'z_max_abs_error':v['max_z_error'],'exact_loss_max_abs_error':v['max_loss_error'],
 'silu_duplicate_identical_at_5m':duplicate,'moment_dtype':'float64',
 'force_units':'gradient-flow direction; learning rate not multiplied; support and centering frozen',
 'quiet_total_moment_threshold':1e-8,'near_balance_relative_threshold':.1,
 'definition':'m+=E[max(phi phi_prime,0)]; m-=E[max(-phi phi_prime,0)]; rho=abs(m+-m-)/(m++m-)',
 'zero_denominator_policy':'ratio set to 1 as non-cancellation sentinel; classify as quiet, not balanced',
 'animation_window':'10 endpoint distributions pooled; Snake original also has first 10 singleton frames',
 'source_code':[{'path':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in source_paths]}
(P/'methods_and_verification.json').write_text(json.dumps(meta,indent=2))
print(json.dumps(meta,indent=2))

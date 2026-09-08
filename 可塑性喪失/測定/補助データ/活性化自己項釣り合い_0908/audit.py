#!/usr/bin/env python3
"""Post-hoc audit of existing animation checkpoints. No training or parameter changes.
Primary descriptive criterion: per-unit M=E[phi phi'] over exact 32 inputs.
Report signed components separately. Relative imbalance |M|/E|phi phi'|
is descriptive, not a statistical test. "Near balance" uses <=0.1, both signs,
and E|phi phi'|>1e-8; report threshold sensitivity and quiet cases separately.
Checkpoint anchors 0/1M/5M are not sliding-window moment measurements.
"""
import csv, hashlib, itertools, json, math, sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import torch
torch.set_num_threads(1)
REPO=Path('/home/issan/Projects/claude/proj_004_drift')
SNAKE=Path('/home/issan/Projects/claude/snake_out_0904')
OUT=Path('/home/issan/Projects/obsidian-research-data/activation_self_balance_0908')
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(SNAKE))
from src.nets import VecMLPL
ARMS=[
 ('leaky100',REPO/'results/p3_extend_0902','LR_1216'),
 ('elu100',REPO/'results/p3_extend_0902','E_1216'),
 ('silu100',REPO/'results/p3_extend_0902','S_b1_1216'),
 ('silu100_gd',REPO/'results/gate_dial_0902','S_b1_1216'),
 ('gelu100',REPO/'results/gate_dial_0902','G_b1_1216'),
 ('leaky5',REPO/'results/width5_gate_b_0901','LR5')]
for suffix in ['025','05','075','10','15','20','30','40','60','80']:
 ARMS.append(('snake_'+suffix,SNAKE/'results/_diag_w5_snake_0905'/('asweep_a'+suffix),'SN5_a1'))
for suffix in ['0002','00037']:
 ARMS.append(('leaky5x_'+suffix,SNAKE/'results/_diag_w5_snake_0905'/('LR5x_lr'+suffix),'LR5x'))
def arr(t): return t.detach().cpu().numpy()
def apg(z,act,a):
 obj=object.__new__(VecMLPL)
 obj.act=act;obj.act_alpha=a;obj.act_grad_form='alpha_exp'
 p=VecMLPL.act_fn(obj,z)
 g=VecMLPL.act_grad(obj,z,p)
 return p,g
def write_csv(name,rows):
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def fmean(x):return float(np.mean(x))
def stats(rows):
 a={k:np.array([r[k] for r in rows]) for k in rows[0] if isinstance(rows[0][k],(int,float,bool))}
 abs_m=a['m_positive']+a['m_negative_abs']; net=a['m_net']
 both=(a['m_positive']>0)&(a['m_negative_abs']>0)
 ratio=np.divide(abs(net),abs_m,out=np.ones_like(abs_m),where=abs_m>0)
 active=abs_m>1e-8
 out={'n':len(rows),'zmean_median':float(np.median(a['zmean'])),
 'm_positive_mean':fmean(a['m_positive']),'m_negative_abs_mean':fmean(a['m_negative_abs']),
 'm_net_mean':fmean(net),'m_abs_median':float(np.median(abs_m)),
 'imbalance_median':float(np.median(ratio)),
 'both_signs_frac':fmean(both),'quiet_moment_frac':fmean(~active),
 'self_b_up_frac':fmean(net<0),'self_b_down_frac':fmean(net>0),
 'all_z_negative_frac':fmean(a['zmax']<0),
 'all_g_negative_frac':fmean(a['gmax']<0),
 'gabs_mean_median':float(np.median(a['gabs_mean'])),
 'abs_v_median':float(np.median(abs(a['v']))),
 'self_b_force_abs_median':float(np.median(abs(a['self_b_force']))),
 'full_b_force_abs_median':float(np.median(abs(a['full_b_force']))),
 'self_meanz_up_frac':fmean(a['self_meanz_force']>0),
 'full_meanz_up_frac':fmean(a['full_meanz_force']>0),
 'whole_shift_slope_positive_frac':fmean(a['m_shift_slope']>0),
 'near_balance_stable_frac':fmean(active&both&(ratio<=.1)&(a['m_shift_slope']>0))}
 for th in [.05,.1,.2]:
  out['near_balance_'+str(th)+'_frac']=fmean(active&both&(ratio<=th))
 for floor in [1e-12,1e-8,1e-4]:
  out['quiet_'+str(floor)+'_frac']=fmean(abs_m<=floor)
 out['pooled_imbalance']=abs(fmean(net))/max(fmean(abs_m),1e-300)
 return out
unitrows=[];summaries=[];seedrows=[];validations=[];manifest=[];trajectories=[]
for label,directory,arm in ARMS:
 print('PROCESS',label,flush=True)
 logcache={}
 for step in [0,1000000,5000000]:
  cp=directory/'ckpts'/f'{arm}_step{step}.pt'
  ck=torch.load(cp,map_location='cpu',weights_only=True)
  manifest.append({'label':label,'step':step,'path':str(cp),'sha256':hashlib.sha256(cp.read_bytes()).hexdigest()})
  n=ck['net'];R,H,D=n['W'].shape
  bits=torch.tensor(list(itertools.product([0.,1.],repeat=5)),dtype=torch.float64)
  raw=torch.cat([ck['env']['flip_state'].double()[None,:,:].expand(32,-1,-1),bits[:,None,:].expand(-1,R,-1)],dim=2)
  x=raw-(ck['layer_means'][0].double()[None,:,:] if ck['centered_layers'][0] else 0)
  z=torch.einsum('rhd,prd->prh',n['W'].double(),x)+n['b'].double()
  act=ck['activation'];alpha=float(ck['act_alpha'])
  phi,g=apg(z,act,alpha);q=phi*g
  v=n['v'].double()
  t=ck['teacher'];tpre=torch.einsum('rhd,prd->prh',t['W'].double(),raw)+t['b'].double()
  y=((tpre>=t['tau'].double()).double()*t['v'].double()).sum(-1)+t['cout'].double()
  pred=(phi*v).sum(-1)+n['c'].double();err=pred-y
  loss=(err*err).mean(0)
  K=1+(x*x.mean(0)[None,:,:]).sum(-1)
  plus=torch.clamp(q,min=0).mean(0);minus=torch.clamp(-q,min=0).mean(0)
  eps=1e-4
  phip,gp=apg(z+eps,act,alpha);phim,gm=apg(z-eps,act,alpha)
  slope=((phip*gp-phim*gm)/(2*eps)).mean(0)
  metrics={
   'zmean':z.mean(0),'zmin':z.min(0).values,'zmax':z.max(0).values,
   'zstd':z.std(0,unbiased=False),'v':v,
   'm_positive':plus,'m_negative_abs':minus,'m_net':q.mean(0),
   'gmean':g.mean(0),'gabs_mean':g.abs().mean(0),'gmin':g.min(0).values,'gmax':g.max(0).values,
   'phi_mean':phi.mean(0),'phi_abs_mean':phi.abs().mean(0),
   'm_zpositive':torch.where(z>0,q,0).mean(0),
   'm_znegative':torch.where(z<0,q,0).mean(0),
   'm_shift_slope':slope,
   'self_b_force':-2*v*v*q.mean(0),
   'full_b_force':-2*v*(err[:,:,None]*g).mean(0),
   'self_meanz_force':-2*v*v*(q*K[:,:,None]).mean(0),
   'full_meanz_force':-2*v*(err[:,:,None]*g*K[:,:,None]).mean(0),
  }
  # force values omit learning rate; mean-z directions freeze input support and centering.
  vals={k:arr(tens) for k,tens in metrics.items()}
  local=[]
  for r,run in enumerate(ck['runs']):
   seed=int(run['seed'])
   if seed not in logcache:
    file=directory/'logs'/f'{arm}_seed{seed}.npz'
    with np.load(file) as data:
     want=['step','task_period','layer1_zmean','layer1_zbar','layer1_M','layer1_B','layer1_denom','layer1_mob','layer1_absmob','layer1_mobility','eval_loss_exact','unfit']
     logcache[seed]={k:data[k] for k in want if k in data.files}
   log=logcache[seed]; idx=int(np.flatnonzero(log['step']==step)[0])
   zkey='layer1_zmean' if 'layer1_zmean' in log else 'layer1_zbar'
   dz=float(np.max(abs(vals['zmean'][r]-log[zkey][idx])))
   dl=float(abs(float(loss[r])-float(log['eval_loss_exact'][idx])))
   assert np.allclose(vals['zmean'][r],log[zkey][idx],rtol=2e-5,atol=5e-6),(label,step,seed,'z',dz)
   assert np.isclose(float(loss[r]),float(log['eval_loss_exact'][idx]),rtol=1e-4,atol=2e-5),(label,step,seed,'loss',dl,float(loss[r]),float(log['eval_loss_exact'][idx]))
   vg={'label':label,'step':step,'seed':seed,'z_max_abs_error':dz,'loss_abs_error':dl}
   if 'layer1_mob' in log:
    dg=float(np.max(abs(vals['gmean'][r]-log['layer1_mob'][idx])))
    assert np.allclose(vals['gmean'][r],log['layer1_mob'][idx],rtol=2e-5,atol=5e-7),(label,step,seed,'g',dg)
    vg['g_max_abs_error']=dg
   validations.append(vg)
   for h in range(H):
    row={'label':label,'activation':act,'alpha':alpha,'width':H,'step':step,'seed':seed,'unit':h,
         'lr':float(run['lr']),'centered':bool(ck['centered_layers'][0])}
    row.update({k:float(a[r,h]) for k,a in vals.items()})
    local.append(row)
   ss=stats(local[-H:]);ss.update({'label':label,'step':step,'seed':seed})
   seedrows.append(ss)
  s=stats(local);s.update({'label':label,'step':step,'activation':act,'alpha':alpha,'width':H,'seeds':R,
                         'lr':float(ck['runs'][0]['lr']),'centered':bool(ck['centered_layers'][0])})
  summaries.append(s);unitrows.extend(local)
 # Preserve animation's pooled 10-task endpoint distribution; never infer q from mean z.
 Z=[];U=[]
 for seed,log in sorted(logcache.items()):
  ids=np.flatnonzero((log['step']>0)&(log['step']<=5000000)&(log['step']%10000==0))
  assert len(ids)==500
  key='layer1_zmean' if 'layer1_zmean' in log else 'layer1_zbar'
  Z.append(log[key][ids]);U.append(log['unfit'][ids])
  if 'layer1_M' in log:
   zformula=(log['layer1_M'][ids].astype(float)+log['layer1_B'][ids].astype(float))*log['layer1_denom'][ids]
   finite=np.isfinite(zformula)
   assert np.allclose(zformula[finite],log[key][ids][finite],rtol=1e-4,atol=2e-5),(label,'M+B reconstruct')
 Z=np.concatenate(Z,axis=1);U=np.stack(U,axis=1)
 for start in range(1,492):
  pool=Z[start-1:start+9].ravel()
  lo,med,hi=np.percentile(pool,[10,50,90])
  trajectories.append({'label':label,'task_start':start,'task_end':start+9,'z_q10':float(lo),
                       'z_q50':float(med),'z_q90':float(hi),'unfit_seed_median_end':float(np.median(U[start+8]))})
write_csv('units.csv',unitrows);write_csv('seed_summary.csv',seedrows);write_csv('summary.csv',summaries)
write_csv('animation_windows.csv',trajectories)
(OUT/'summary.json').write_text(json.dumps(summaries,indent=2),encoding='utf-8')
(OUT/'verification.json').write_text(json.dumps({'n_checks':len(validations),'max_z_error':max(v['z_max_abs_error'] for v in validations),
 'max_loss_error':max(v['loss_abs_error'] for v in validations),'checks':validations},indent=2),encoding='utf-8')
(OUT/'sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('COMPLETE',len(unitrows),'units',len(validations),'checks',flush=True)
for s in summaries:
 if s['step']==5000000:
  print(json.dumps({k:s[k] for k in ['label','alpha','lr','zmean_median','m_positive_mean','m_negative_abs_mean','imbalance_median','near_balance_0.1_frac','quiet_moment_frac','self_b_up_frac','all_z_negative_frac','gabs_mean_median']}),flush=True)

#!/usr/bin/env python3
"""Reproduce the predeclared numerical validation protocol.

See experiments/empirical-2026-10-16.md. Simulation code never calls the
analytical majority recurrence to update a physical state.
"""

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'work/mpl-cache'))
import numpy as np
import scipy
from scipy.stats import beta, binom, t as student_t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fresh_qubits_memory.majority import majority_error
from fresh_qubits_memory.validation import (
    repetition_permutation, repetition_step, bit_channel,
    quantum_step, normalized_purity, trace_distance,
    bound_constants, common_norm, cooling_step,
)

SEED = 20261016
BLUE, GOLD, RED, GRAY = '#2368A2', '#B78325', '#B94749', '#535D68'


def save_csv(out, name, rows):
    with (out / (name + '.csv')).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def interval(success, total, level=.99):
    alpha = (1 - level) / 2
    lo = 0.0 if success == 0 else float(beta.ppf(alpha, success, total - success + 1))
    hi = 1.0 if success == total else float(beta.ppf(1 - alpha, success + 1, total - success))
    return lo, hi


def half_life(p):
    if p <= 0:
        return math.inf
    if p >= .5:
        return 0.0
    return -math.log(2) / math.log1p(-2 * p)


def full_channel(out):
    rng = np.random.default_rng(SEED + 1)
    rows, checks = [], []
    for r in (1, 3, 5, 7):
        n, dim = 2 * r + 2, 1 << (2 * r + 2)
        perm = repetition_permutation(r)
        assert len(np.unique(perm)) == dim
        # Independently apply classical controlled XOR, followed by a swap.
        independent = []
        for label in range(dim):
            bits = [(label >> j) & 1 for j in range(n - 1, -1, -1)]
            a, c, b, x = bits[:r], bits[r], bits[r+1], bits[r+2:]
            decision = b if c else int(sum(x) > r // 2)
            a = [v ^ decision for v in a]
            output = x + [c, b] + a
            independent.append(sum(v << (n-1-j) for j, v in enumerate(output)))
        assert np.array_equal(perm, independent)
        z = 1 - 2 * (np.arange(dim) & 1)
        initial = rng.random(dim)
        initial /= initial.sum()
        worst = 0.0
        for q in (.5, .7, .9):
            p = float(majority_error(str(q), r))
            states = [repetition_step(initial, r, q, 1, b, perm) for b in (0, 1)]
            for t in range(31):
                values = [float(z @ state) for state in states]
                expected = q * math.exp(t * math.log1p(-2 * p))
                err = max(abs(values[0] - expected), abs(values[1] + expected))
                worst = max(worst, err)
                tv = float(np.abs(states[0] - states[1]).sum() / 2)
                rows.append(dict(r=r, k=r+2, n=n, q=q, delay=t, z0=values[0], z1=values[1], prediction=expected, trace_distance=tv, absolute_error=err))
                for state in states:
                    assert abs(state.sum()-1) < 1e-10 and state.min() >= -1e-14
                if t < 30:
                    states = [repetition_step(s, r, q, 0, 0, perm) for s in states]
        assert worst < 1e-10
        checks.append(dict(r=r, basis_states=dim, permutation=True, independent_gate_match=True, max_error=worst))
    save_csv(out, 'full_channel', rows)
    return dict(checks=checks, max_absolute_error=max(x['max_error'] for x in checks))


def sampling(out):
    rng = np.random.default_rng(SEED + 2)
    rows = []
    samples = 1_000_000
    for r in range(1, 16, 2):
        failures = 0
        for start in range(0, samples, 50_000):
            errors = rng.random((min(50_000, samples-start), r)) < .05
            failures += int(np.count_nonzero(errors.sum(axis=1) > r // 2))
        lo, hi = interval(failures, samples)
        exact = float(majority_error('0.9', r))
        rows.append(dict(r=r, k=r+2, q=.9, trials=samples, failures=failures,
                         p_hat=failures/samples, p_lo_99=lo, p_hi_99=hi, p_exact=exact,
                         half_exact=half_life(exact), half_estimate=half_life(failures/samples) if failures else '',
                         half_lo_99=half_life(hi), half_hi_99=half_life(lo) if lo else '',
                         half_upper_unresolved=(lo==0),
                         reference_in_interval=bool(lo <= exact <= hi)))
    save_csv(out, 'physical_errors', rows)
    trajectories = []
    samples, n, q = 12_000, 32, .9
    for r in (1, 3, 5):
        ref_half = half_life(float(majority_error('0.9', r)))
        stop = int(math.ceil(2*ref_half))
        keep = set(np.linspace(0, stop, 41, dtype=int))
        # Full n-bit physical trajectory: input [a,c,b], memory, spectators.
        bits = rng.integers(0, 2, size=(samples, n), dtype=np.int8)
        for t in range(stop+1):
            bits[:, :r+2] = 0
            bits[:, r] = int(t == 0)
            vote = np.zeros(samples, dtype=np.int8) if t == 0 else (bits[:, r+2:2*r+2].sum(axis=1) > r//2).astype(np.int8)
            ancilla = bits[:, :r].copy()
            old_memory = bits[:, r+2:2*r+2].copy()
            bits[:, :r] = old_memory
            bits[:, r+2:2*r+2] = ancilla ^ vote[:, None]
            bits ^= (rng.random(bits.shape) < (1-q)/2).astype(np.int8)
            if t in keep:
                ones = int(bits[:, r+2].sum())
                lo, hi = interval(ones, samples, .95)
                predicted = q * math.exp(t * math.log1p(-2*float(majority_error('0.9', r))))
                trajectories.append(dict(r=r,k=r+2,n=n,delay=t,trials=samples,z=1-2*ones/samples,z_lo_95=1-2*hi,z_hi_95=1-2*lo,prediction=predicted))
    save_csv(out, 'physical_trajectories', trajectories)
    return dict(trials_per_error_rate=1_000_000, covered_99=sum(x['reference_in_interval'] for x in rows), rows=len(rows), zero_counts=[x['r'] for x in rows if x['failures']==0], trajectory_rows=len(trajectories))


def rare_events(out):
    """Follow-up experiment: independent likelihood-weighted bit samples.

    We sample errors at rate 1/2, then restore the target p=0.05 measure.
    This is importance sampling, not a direct natural-noise trajectory.
    """
    rng=np.random.default_rng(SEED+5)
    rows,replicates=[],[]
    batches,per_batch=64,50_000
    for r in (9,15,31):
        means=[]
        for batch in range(batches):
            errors=rng.integers(0,2,size=(per_batch,r),dtype=np.int8)
            counts=errors.sum(axis=1)
            log_weights=counts*np.log(.05/.5)+(r-counts)*np.log(.95/.5)
            estimates=np.where(counts>r//2,np.exp(log_weights),0.)
            value=float(estimates.mean())
            means.append(value)
            replicates.append(dict(r=r,batch=batch,trials=per_batch,estimate=value))
        mean=float(np.mean(means));se=float(np.std(means,ddof=1)/np.sqrt(batches))
        width=float(student_t.ppf(.995,batches-1))*se
        lo,hi=mean-width,mean+width
        exact=float(majority_error('0.9',r))
        rows.append(dict(r=r,k=r+2,q=.9,target_error_rate=.05,proposal_error_rate=.5,batches=batches,trials=batches*per_batch,p_estimate=mean,p_lo_99=lo,p_hi_99=hi,p_exact=exact,reference_in_interval=bool(lo<=exact<=hi),half_estimate=half_life(mean),half_lo_99=half_life(hi),half_hi_99=half_life(lo),half_reference=half_life(exact)))
    save_csv(out,'importance_sampling',rows)
    save_csv(out,'importance_replicates',replicates)
    return dict(method='likelihood-weighted physical error patterns; 99% Student-t intervals across 64 independent batches',rows=rows)


def passive_distance(r, q, delay):
    # After a write and delay hold cycles, both hypotheses are product states.
    bias = q ** (delay+1)
    return float(2 * binom.cdf(r//2, r, (1-bias)/2) - 1)


def size_controls(out):
    rows=[]
    for r in range(1, 52, 2):
        t=0
        while passive_distance(r,.9,t) >= .45:
            t+=1
        rows.append(dict(r=r,k=r+2,n_active=2*r+2,q=.9,
                         active_one_qubit_half_life=half_life(float(majority_error('0.9',r))),
                         passive_optimal_last_delay=t-1,passive_distance_threshold=.45))
    save_csv(out,'active_passive',rows)
    shift=[]
    for n in (2,4,8,16,24,32,64):
        for delay in range(41):
            # Explicit one-bit marginals under reset + cyclic permutation.
            # This product family is closed under the exact quantum channel.
            biases=np.zeros(n)
            biases[0]=1.0
            biases=np.roll(biases,1)*.9
            for _ in range(delay):
                biases[0]=0.0
                biases=np.roll(biases,1)*.9
            distance=float(np.max(np.abs(biases)))
            shift.append(dict(n=n,k=1,q=.9,delay=delay,pulse_trace_distance=distance,epsilon=.1))
    save_csv(out,'shift_register',shift)
    return dict(shift_last_delay={str(n):max(x['delay'] for x in shift if x['n']==n and x['pulse_trace_distance']>.1) for n in (2,4,8,16,24,32,64)})


def haar(rng, dim):
    z=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
    unitary, triangular=np.linalg.qr(z)
    phases=np.diag(triangular)
    return unitary * (phases/np.abs(phases)).conj()[None,:]


def quantum(out):
    rng=np.random.default_rng(SEED+3)
    curves, checks, witnesses=[],[],[]
    for n in (2,3,4,5):
        for k in (x for x in (1,2) if x<n):
            dim, inp=1<<n,1<<k
            v0=np.zeros(inp);v0[0]=1
            vp=np.ones(inp)/np.sqrt(inp)
            enc=[np.outer(v0,v0),np.outer(vp,vp)]
            for q in (.5,.9):
                theta,log2r,loginv=bound_constants(q,k)
                C=2**(theta*k/2)
                for sample in range(4):
                    U=haar(rng,dim)
                    states=[np.diag(np.eye(dim)[i]).astype(complex) for i in (0,dim-1)]
                    cap_max=0.0
                    for burn in range(1,401):
                        eta=enc[int(rng.integers(2))]
                        old=states
                        states=[quantum_step(s,eta,k,U,q,n) for s in old]
                        for before,after in zip(old,states):
                            cap_max=max(cap_max,normalized_purity(after)/(C*normalized_purity(before)**theta))
                        if trace_distance(*states)<1e-12:
                            break
                    initialization_residual=trace_distance(*states)
                    assert initialization_residual<1e-12
                    # Different input pulse, followed by identical subsequent maps.
                    anchor=(states[0]+states[1])/2
                    pair=[quantum_step(anchor,eta,k,U,q,n) for eta in enc]
                    max_contraction=0.0
                    max_trace_error=0.0
                    min_eigenvalue=1.0
                    for delay in range(41):
                        dist=trace_distance(*pair)
                        curves.append(dict(n=n,k=k,q=q,unitary=sample,delay=delay,trace_distance=dist))
                        for s in pair:
                            max_trace_error=max(max_trace_error,float(abs(np.trace(s)-1)))
                            min_eigenvalue=min(min_eigenvalue,float(np.linalg.eigvalsh(s).min()))
                        if delay==40:
                            break
                        eta=enc[int(rng.integers(2))]
                        before=pair
                        pair=[quantum_step(s,eta,k,U,q,n) for s in before]
                        for s,t in zip(before,pair):
                            cap_max=max(cap_max,normalized_purity(t)/(C*normalized_purity(s)**theta))
                        oldv=common_norm(before[0]-before[1],log2r)
                        if oldv>1e-10:
                            ratio=common_norm(pair[0]-pair[1],log2r)/oldv
                            max_contraction=max(max_contraction,ratio)
                    # Independent signed Hermitian inputs to the same linear map.
                    for _ in range(6):
                        X=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
                        X=(X+X.conj().T)/2
                        X-=np.trace(X)/dim*np.eye(dim)
                        Y=quantum_step(X,enc[int(rng.integers(2))],k,U,q,n)
                        ratio=common_norm(Y,log2r)/common_norm(X,log2r)
                        witnesses.append(dict(n=n,k=k,q=q,unitary=sample,ratio=ratio,bound=1-2**(-loginv)))
                    checks.append(dict(n=n,k=k,q=q,unitary=sample,burn_cycles=burn,initialization_residual=initialization_residual,purity_ratio=cap_max,max_common_norm_ratio=max_contraction,contraction_bound=1-2**(-loginv),log2_inverse_delta=loginv,max_trace_error=max_trace_error,min_eigenvalue=min_eigenvalue))
    save_csv(out,'quantum_curves',curves)
    save_csv(out,'quantum_checks',checks)
    save_csv(out,'quantum_signed_operators',witnesses)
    assert max(x['purity_ratio'] for x in checks)<=1+1e-10
    assert all(x['ratio']<=x['bound']+1e-10 for x in witnesses)
    assert all(x['max_common_norm_ratio']<=x['contraction_bound']+1e-10 for x in checks)
    assert max(x['max_trace_error'] for x in checks)<1e-10
    assert min(x['min_eigenvalue'] for x in checks)>-1e-10
    return dict(reservoirs=len(checks),signed_operators=len(witnesses),max_purity_ratio=max(x['purity_ratio'] for x in checks),max_contraction_ratio=max(x['ratio'] for x in witnesses),max_burn_cycles=max(x['burn_cycles'] for x in checks),max_initialization_residual=max(x['initialization_residual'] for x in checks),max_trace_error=max(x['max_trace_error'] for x in checks))


def noise_controls(out):
    r=3;dim=1<<(2*r+2);perm=repetition_permutation(r)
    start=np.ones(dim)/dim
    z=1-2*(np.arange(dim)&1)
    rows=[]
    for label,q,extra in [('depolarizing',.9,None),('extra_bit_flips',.9,.1),('extra_full_depolarization',.9,.5),('pure_dephasing_only',1.,None)]:
        states=[start.copy(),start.copy()]
        for t in range(101):
            states=[repetition_step(s,r,q,int(t==0),b if t==0 else 0,perm) for b,s in enumerate(states)]
            if extra is not None:
                states=[bit_channel(s,2*r+2,extra,1-extra) for s in states]
            rows.append(dict(channel=label,delay=t,z_gap_half=float(z@(states[0]-states[1])/2),trace_distance=float(np.abs(states[0]-states[1]).sum()/2)))
    save_csv(out,'noise_controls',rows)
    correlated=[]
    for t in range(1,21):
        # Enumerate the fixed Pauli label. X,Y flip a computational-basis bit.
        weights=[(1+3*.9)/4]+[(1-.9)/4]*3
        sign=sum(w*((-1)**t if i in (1,2) else 1) for i,w in enumerate(weights))
        correlated.append(dict(noise_cycles=t,markov_signal=.9**t,fixed_pauli_signal=sign))
    save_csv(out,'correlated_noise',correlated)
    return dict(extra_full_depolarization_max_distance=max(x['trace_distance'] for x in rows if x['channel']=='extra_full_depolarization'),pure_dephasing_min_distance=min(x['trace_distance'] for x in rows if x['channel']=='pure_dephasing_only'))


def cooling(out):
    rng=np.random.default_rng(SEED+4)
    rows=[]
    trials=3000
    for gamma,rgrid in ((.3,(3,7,15,31,63,127)),(0.,(31,))):
        q,s=.9,4
        a,d=(1-q)/2,q*(1-gamma)
        pstar=a/(1-d)
        c=d*d*(.5-pstar)**2/2
        for r in rgrid:
            state=[rng.binomial(r,pstar,size=(trials,s+1)) for _ in (0,1)]
            last_half=-1
            for t in range(601):
                state=[cooling_step(x,r,q,gamma,rng,write=b if t==0 else None) for b,x in enumerate(state)]
                if t<=30 or t%10==0:
                    ones=[int(np.count_nonzero(x[:,0]>=(a+d/2)*r)) for x in state]
                    cis=[interval(v,trials,.975) for v in ones]
                    # Bonferroni combination of two 97.5% intervals => >=95% gap coverage.
                    gap=(ones[1]-ones[0])/trials
                    lower=max(-1.,cis[1][0]-cis[0][1]);upper=min(1.,cis[1][1]-cis[0][0])
                    if gap>.5:
                        last_half=t
                    bound=1-2*(t+1)*math.exp(-c*r)
                    rows.append(dict(gamma=gamma,q=q,s=s,r=r,n=2+(s+1)*r,k=2,delay=t,trials_per_bit=trials,pstar=pstar,gap=gap,gap_lo_95=lower,gap_hi_95=upper,union_bound_gap=max(-1.,bound),bound_nonvacuous=bound>0))
            print(f'  cooling gamma={gamma}, r={r}, n={2+(s+1)*r}: last sampled gap > 0.5 at {last_half}',flush=True)
    save_csv(out,'cooling',rows)
    endpoints=[x for x in rows if x['delay']==600]
    return dict(trials_per_bit=trials,max_delay=600,endpoints=[dict(r=x['r'],n=x['n'],gamma=x['gamma'],gap=x['gap'],ci=[x['gap_lo_95'],x['gap_hi_95']]) for x in endpoints],nonvacuous_bound_rows=sum(x['bound_nonvacuous'] for x in rows))


def read_csv(out,name):
    with (out/(name+'.csv')).open() as f:
        return list(csv.DictReader(f))


def plots(out):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#222222','text.color':'#222222','axes.titleweight':'bold','figure.facecolor':'white','savefig.facecolor':'white'})
    fig,axs=plt.subplots(2,2,figsize=(12.5,9),layout='constrained')
    data=read_csv(out,'physical_trajectories')
    for r,color in zip((1,3,5),(BLUE,GOLD,RED)):
        rr=[x for x in data if int(x['r'])==r]
        t=np.array([float(x['delay']) for x in rr]);z=np.array([float(x['z']) for x in rr])
        lo=np.array([float(x['z_lo_95']) for x in rr]);hi=np.array([float(x['z_hi_95']) for x in rr])
        pred=[float(x['prediction']) for x in rr]
        axs[0,0].plot(t,pred,color=color,lw=1.6,label=f'k={r+2}, r={r}')
        axs[0,0].errorbar(t,z,yerr=[z-lo,hi-z],fmt='o',ms=2.4,color=color,elinewidth=.6,alpha=.6)
    axs[0,0].set(xscale='symlog',xlim=(0,620),ylim=(-.02,1),xlabel='Hold cycles since write (symlog)',ylabel='Measured one-qubit Z',title='A  Full physical trajectories at fixed n = 32')
    axs[0,0].legend(fontsize=9)
    data=read_csv(out,'physical_errors')
    ks=[int(x['k']) for x in data]
    exact=[float(x['p_exact']) for x in data]
    axs[0,1].plot(ks,exact,color=BLUE,label='Exact reference',lw=1.6)
    for x in data:
        k=int(x['k']);p=float(x['p_hat']);lo=float(x['p_lo_99']);hi=float(x['p_hi_99'])
        if p>0:
            axs[0,1].errorbar(k,p,yerr=[[p-lo],[hi-p]],fmt='o',color=RED,capsize=3)
        else:
            axs[0,1].scatter(k,hi,marker='v',color=RED)
            axs[0,1].annotate('0 failures; upper bound',(k,hi),xytext=(-7,22),textcoords='offset points',ha='right',fontsize=8,arrowprops={'arrowstyle':'-','color':RED,'lw':.8})
    axs[0,1].plot([],[],marker='o',color=RED,ls='',label='Sampling + 99% intervals')
    axs[0,1].set(yscale='log',xlabel='Fresh input qubits k = r + 2',ylabel='Logical error probability per hold cycle',title='B  One million independent trials per point')
    axs[0,1].legend(fontsize=9)
    data=read_csv(out,'active_passive')
    rr=[x for x in data if int(x['r'])<=15]
    axs[1,0].plot([int(x['k']) for x in rr],[float(x['active_one_qubit_half_life']) for x in rr],'o-',color=BLUE,label='Active repair: one-qubit readout')
    axs[1,0].plot([int(x['k']) for x in rr],[max(.5,float(x['passive_optimal_last_delay'])) for x in rr],'s--',color=GOLD,label='Passive copies: optimal full-state readout')
    axs[1,0].set(yscale='log',xlabel='k = r + 2 for active reservoir',ylabel='Cycles above distinguishability 0.45',title='C  Exact model values; q = 0.9')
    axs[1,0].legend(fontsize=8)
    data=read_csv(out,'shift_register')
    ns=sorted({int(x['n']) for x in data})
    last=[max(int(x['delay']) for x in data if int(x['n'])==n and float(x['pulse_trace_distance'])>.1) for n in ns]
    axs[1,1].plot(ns,last,'o-',color=BLUE)
    axs[1,1].axhline(20,color=GRAY,ls='--',lw=1,label='Pulse threshold from q^(L+1) > 0.1')
    axs[1,1].set(xlabel='Total qubits n; fixed k = 1',ylabel='Last pulse delay with trace distance > 0.1',title='D  Size can help below a uniform ceiling',ylim=(-1,24))
    axs[1,1].legend(fontsize=8)
    for ax in axs.flat:
        ax.grid(alpha=.18)
    fig.suptitle('Independent numerical validation of noisy-reservoir memory',fontsize=16)
    fig.savefig(out/'validation_overview.png',dpi=180)
    fig.savefig(out/'validation_overview.pdf')
    plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(15,4.6),layout='constrained')
    data=read_csv(out,'quantum_curves')
    for q,color in ((.5,GOLD),(.9,BLUE)):
        for n in (2,3,4,5):
            for k in (1,2):
                for u in range(4):
                    rr=[x for x in data if float(x['q'])==q and int(x['n'])==n and int(x['k'])==k and int(x['unitary'])==u]
                    if rr:
                        axs[0].plot([int(x['delay']) for x in rr],np.maximum(1e-14,[float(x['trace_distance']) for x in rr]),color=color,alpha=.22,lw=.8)
        axs[0].plot([],[],color=color,label=f'q={q}')
    axs[0].set(yscale='log',xlabel='Common-input suffix length',ylabel='Trace distance of pulse histories',ylim=(1e-13,1),title='Quantum channels: 56 reservoirs')
    axs[0].legend(fontsize=9)
    data=read_csv(out,'noise_controls')
    styles=[('depolarizing','Depolarizing only',BLUE,'-'),('extra_bit_flips','Plus unital bit flips',GOLD,'--'),('extra_full_depolarization','Plus complete depolarization',RED,':'),('pure_dephasing_only','Pure dephasing (outside model)',GRAY,'-.')]
    for key,label,color,style in styles:
        rr=[x for x in data if x['channel']==key]
        axs[1].plot([int(x['delay']) for x in rr],[float(x['z_gap_half']) for x in rr],color=color,ls=style,label=label)
    axs[1].set(xlabel='Hold cycles',ylabel='One-qubit signal contrast',title='Unital noise preserves only the upper bound',ylim=(-.04,1.05))
    axs[1].legend(fontsize=7.5)
    data=read_csv(out,'cooling')
    colors=['#B94749','#B78325','#8A8D45','#2368A2','#74639B','#313B46']
    for r,color in zip((3,7,15,31,63,127),colors):
        rr=[x for x in data if float(x['gamma'])==.3 and int(x['r'])==r]
        ts=[int(x['delay']) for x in rr]
        axs[2].plot(ts,[float(x['gap']) for x in rr],color=color,label=f'n={2+5*r}')
        axs[2].fill_between(ts,[float(x['gap_lo_95']) for x in rr],[float(x['gap_hi_95']) for x in rr],color=color,alpha=.1)
    rr=[x for x in data if float(x['gamma'])==0]
    axs[2].plot([int(x['delay']) for x in rr],[float(x['gap']) for x in rr],ls='--',color='black',label='No damping; n=157')
    axs[2].set(xscale='symlog',xlabel='Hold cycles (symlog)',ylabel='Threshold decoding probability gap',ylim=(-.1,1.05),title='Cooling pipeline: fixed k = 2')
    axs[2].legend(fontsize=7.5,ncol=2)
    for ax in axs:
        ax.grid(alpha=.18)
    fig.savefig(out/'quantum_and_noise.png',dpi=180)
    fig.savefig(out/'quantum_and_noise.pdf')
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,default=ROOT/'results/empirical-2026-10-16')
    args=parser.parse_args()
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    summary={}
    for label,fn in [('full_channel',full_channel),('sampling',sampling),('size_controls',size_controls),('quantum',quantum),('noise_controls',noise_controls),('cooling',cooling),('importance_sampling',rare_events)]:
        start=time.perf_counter()
        print(f'Running {label}',flush=True)
        summary[label]=fn(out)
        summary[label]['seconds']=round(time.perf_counter()-start,3)
        print(json.dumps(summary[label]),flush=True)
    plots(out)
    files=['paper/source/memory_limits.tex','src/fresh_qubits_memory/validation.py','scripts/validate_empirical.py','experiments/empirical-2026-10-16.md']
    metadata=dict(seed=SEED,child_seeds={'full_channel':SEED+1,'sampling':SEED+2,'quantum':SEED+3,'cooling':SEED+4,'importance_sampling':SEED+5},precision='float64 / complex128; exact Fraction reference majority tails',python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,git_base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),command='MPLCONFIGDIR=work/mpl-cache OPENBLAS_NUM_THREADS=1 python3 scripts/validate_empirical.py --output-dir results/empirical-2026-10-16',source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},summary=summary)
    (out/'metadata.json').write_text(json.dumps(metadata,indent=2,allow_nan=False)+'\n')
    print('All experiments complete; outputs in '+str(out),flush=True)


if __name__=='__main__':
    main()

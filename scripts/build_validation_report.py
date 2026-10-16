#!/usr/bin/env python3
"""Build a reviewable validation report from saved, seeded experiment rows."""

import csv
import hashlib
import json
import math
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/empirical-2026-10-16'


def read(name):
    return list(csv.DictReader((OUT/(name+'.csv')).open()))


def main():
    meta=json.loads((OUT/'metadata.json').read_text())
    direct=read('physical_errors')
    rare=read('importance_sampling')
    traj=read('physical_trajectories')
    cooling=read('cooling')
    coverage=sum(float(x['z_lo_95'])<=float(x['prediction'])<=float(x['z_hi_95']) for x in traj)
    maxz=max(abs(float(x['z'])-float(x['prediction']))/math.sqrt((1-float(x['prediction'])**2)/int(x['trials'])) for x in traj)
    boundrows=[x for x in cooling if x['bound_nonvacuous']=='True']
    above=sum(float(x['union_bound_gap'])>float(x['gap_hi_95']) for x in boundrows)
    checks=dict(trajectory_pointwise_95_coverage=coverage,trajectory_points=len(traj),maximum_marginal_standardized_residual=maxz,cooling_nonvacuous_bound_rows=len(boundrows),cooling_bounds_above_upper_95_interval=above,unit_tests_passed=12,original_baseline_csv_identical=True)
    (OUT/'analysis_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    verdict='The explicit memory construction is strongly supported by independent numerical simulation within the stipulated model. No violation of the tested upper-bound ingredients was found. The experiments do not prove the universal theorem, establish asymptotic optimality, or validate a hardware implementation.'
    intro='Scope: The Memory Limits of Noisy Quantum Reservoirs, manuscript revision 3, 16 October 2026. Base commit 77cd7a3. All cycles contain an ideal unitary followed by independent physical noise; they are not elementary gate cycles. This report records successful checks, statistical misses, and limitations.'
    full='The complete reversible map was enumerated for r = 1, 3, 5, 7 (n = 4, 8, 12, 16). All four maps are permutations and agree with a separately implemented controlled-XOR-then-swap circuit. Complete diagonal probability distributions were propagated through discard, preparation, the unitary, and physical noise at q = 0.5, 0.7, 0.9, for both written bits and 30 hold cycles. Across 372 time points, the largest discrepancy from Eq. (14) was 2.10e-14. Diagonal dynamics are the exact quantum dynamics of this particular construction.'
    sampling=f'At fixed total n = 32, 12,000 explicit bit trajectories per setting reproduced the decay for k = 3, 5, 7. The formula lies in {coverage} of {len(traj)} pointwise 95% intervals; the largest residual is {maxz:.2f} marginal standard deviations. The nine misses are retained. Points along a trajectory are correlated, and the intervals are not a simultaneous confidence band. Independent one-step sampling used one million physical error patterns for each odd r from 1 to 15. All eight reference probabilities lie inside the exact 99% Clopper-Pearson intervals.'
    raretext='Direct sampling recorded zero majority failures at r = 15. It gives a 99% upper error-probability bound of 5.30e-6 and only a lower half-life bound of 65,412 cycles; it cannot resolve 1.89 million cycles precisely. A separately declared follow-up used importance sampling: explicit error patterns at proposal probability 1/2, reweighted to target probability 0.05. Each r uses 64 independent batches of 50,000 patterns. The approximate 99% Student-t intervals below use the variation of those batch means. These are model-based rare-event estimates, not direct million-cycle observations.'
    quantum='Fifty-six reservoirs with n = 2..5, k = 1 or 2 < n, q = 0.5 or 0.9, fixed Haar unitaries, and nonorthogonal input states were simulated as complex density matrices. Initialization pairs converged to trace distance below 1e-12 within at most 60 warmup steps. Differing input pulses were then followed by 40 common inputs. The largest observed purity-recursion ratio was 0.9304 (bound 1). All common-norm checks passed; for 336 independent traceless Hermitian operators the largest contraction ratio was 0.6843. Density-matrix traces stayed within 2.99e-14 of one. These selected histories do not exhaust the supremum defining memory depth.'
    cooltext='Appendix C was implemented as an exact block-count Markov process: block rotation, XOR, and independent physical bit transitions. Correlations between all cooling blocks are retained. With q = 0.9, gamma = 0.3, s = 4, only k = 2 control qubits are reset. There are 3,000 trajectories per written bit and 600 hold cycles. The initial distribution is the exact stationary echo state for an infinite all-store-zero prefix, avoiding an initialization-purity benefit. The reported gap is P(threshold=1 | write 1) minus P(threshold=1 | write 0), a lower witness for trace distance. The intervals combine two exact 97.5% binomial intervals, yielding at least 95% pointwise coverage. None of the 17 nonvacuous analytical bound values exceeded the corresponding upper confidence endpoint.'
    coolinglimit='At n = 317 and 637 the gap remains above 0.5 at 600 cycles; these lifetimes are right-censored. The gamma = 0 control starts from its corresponding maximally mixed echo state and carries no resolvable input information. These finite-size results support the cooling mechanism and a size benefit at fixed k. They do not determine its asymptotic exponent or validate the separate approximately 1,100-qubit numerical example.'
    wording1='The conclusion says that additional qubits cannot extend the memory of new inputs. Taken literally, this is too strong. A legal cyclic-shift reservoir with k = 1 and q = 0.9 has pulse trace distance q^(L+1) for L < n, and zero after overwrite. At accuracy 0.1 the last retained delay grows from 1 (n = 2) to 15 (n = 16), then saturates at 20 for n >= 24. This is a counterexample to the blanket wording, not to a size-independent universal upper bound. Suggested wording: "At fixed reset width and noise strength, increasing the reservoir size cannot make driven memory grow without bound, although particular architectures can improve below this ceiling."'
    wording2='The abstract says that unital noise leaves the limit unchanged, and the discussion says the theorem holds verbatim. The upper bound survives extra unital layers; a matching lower bound need not survive a prescribed layer. Complete depolarization is unital and erased all memory in the control simulation (residual <= 1.12e-16). Even additional bit flips shortened the r = 3 readout markedly. Suggested wording: "Additional unital noise does not relax the upper bound, whereas non-unital noise can provide an additional entropy sink." The existing appendix already notes that the lower construction uses identity additional layers. Maximizing over the enlarged channel class is different from fixing arbitrary extra noise.'
    caveats='No finite experiment can establish a bound for every unitary, encoding, system size, or input history. At q = 0.9 and accuracy 0.45 the stated upper bound is roughly 10^143 cycles for k = 3 and 10^504 cycles for k = 17, so absence of an upper-bound violation is weak evidence for its constants. The main theorem still needs independent proof review. No test here addresses gate compilation, noise per elementary gate, reset infidelity, hardware data, nonlinear task performance, classical hardness, novelty, or quantum advantage. Pure dephasing and time-correlated Pauli errors reproduced the expected outside-model preservation and revival controls.'
    reproduce='Reproduce with: python -m pip install -e ".[validation]"; PYTHONPATH=src python -m unittest discover -s tests -v; MPLCONFIGDIR=work/mpl-cache OPENBLAS_NUM_THREADS=1 python scripts/validate_empirical.py; python scripts/build_validation_report.py. Twelve tests passed, including independent Kraus checks, Bell-state reset, physical-noise equivalence, and a joint cooling-transition check. The original Table I baseline was regenerated and is byte-identical. Seeds, versions, source hashes, all CSV rows, and the before-run protocol are preserved. The importance-sampling follow-up is explicitly dated after the first run in the protocol. No paper text or figure was changed by this validation.'

    raretable=[['k','Rare-event half-life estimate','Approx. 99% interval','Exact reference']]
    def number(value):
        value=float(value)
        return f'{value:.5g}' if value>=1e9 else f'{value:,.0f}'
    for x in rare:
        raretable.append([x['k'],number(x['half_estimate']),number(x['half_lo_99'])+' - '+number(x['half_hi_99']),number(x['half_reference'])])
    directtable=[['k','Failures / 1,000,000','Reference probability','Inside 99% interval']]
    for x in direct:
        directtable.append([x['k'],f"{int(x['failures']):,}",f"{float(x['p_exact']):.4g}",'Yes' if x['reference_in_interval']=='True' else 'No'])
    cooltable=[['n','gamma','Decoding gap at 600 cycles','Pointwise 95% interval']]
    for x in cooling:
        if int(x['delay'])==600:
            cooltable.append([x['n'],x['gamma'],f"{float(x['gap']):.4f}",f"{float(x['gap_lo_95']):.4f} to {float(x['gap_hi_95']):.4f}"])
    def mdtable(table):
        return '\n'.join(['| '+' | '.join(table[0])+' |','| '+' | '.join(['---']*len(table[0]))+' |']+['| '+' | '.join(row)+' |' for row in table[1:]])
    md='\n\n'.join(['# Independent numerical validation - 16 October 2026',intro,'**Assessment.** '+verdict,'## Full channel and physical sampling',full,sampling,mdtable(directtable),'![Overview](validation_overview.png)','## Rare-event follow-up',raretext,mdtable(raretable),'## General quantum channels and cooling',quantum,cooltext,mdtable(cooltable),coolinglimit,'![Quantum channels and noise controls](quantum_and_noise.png)','## Two wording corrections recommended',wording1,wording2,'## What remains unvalidated',caveats,'## Reproduction and evidence',reproduce,'[Protocol](../../experiments/empirical-2026-10-16.md) | [Metadata](metadata.json) | [Derived checks](analysis_checks.json) | [PDF report](validation_report.pdf)'])+'\n'
    (OUT/'REPORT.md').write_text(md)

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BodyCustom',fontName='Helvetica',fontSize=9.5,leading=13,spaceAfter=9,textColor=colors.HexColor('#23303C')))
    styles.add(ParagraphStyle(name='SmallCustom',fontName='Helvetica',fontSize=8,leading=10.5,spaceAfter=6,textColor=colors.HexColor('#536271')))
    styles.add(ParagraphStyle(name='TitleCustom',fontName='Helvetica-Bold',fontSize=23,leading=27,spaceAfter=14,textColor=colors.HexColor('#174E75')))
    styles.add(ParagraphStyle(name='HeadingCustom',fontName='Helvetica-Bold',fontSize=13,leading=17,spaceBefore=7,spaceAfter=9,textColor=colors.HexColor('#174E75')))
    story=[]
    def p(text,style='BodyCustom'):
        text=text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        story.append(Paragraph(text,styles[style]))
    def heading(text):p(text,'HeadingCustom')
    def table(data,widths):
        converted=[[Paragraph(cell,styles['SmallCustom']) for cell in row] for row in data]
        t=Table(converted,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E9F1F7')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#92A9BA')),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#DCE3E9'))]))
        story.append(t);story.append(Spacer(1,8))
    p('Independent numerical validation','TitleCustom')
    p(intro,'SmallCustom')
    heading('Assessment')
    p(verdict)
    heading('A complete implementation of the memory construction')
    p(full)
    p(sampling)
    heading('Rare errors: a separate sampling test')
    p(raretext)
    table(raretable,[25,130,215,120])
    p('Half-lives are continuous crossings of one-half initial signal. The paper lists their integer floors. Intervals concern the sampling error under the assumed model, not uncertainty in hardware parameters.','SmallCustom')
    story.append(PageBreak())
    heading('Reset width, physical sampling, and the size control')
    story.append(Image(str(OUT/'validation_overview.png'),width=490,height=490*9/12.5))
    p('A: complete 32-bit trajectories; lines are the analytical prediction and bars are pointwise 95% intervals. B: natural-noise trials with exact 99% intervals; the triangle denotes an upper bound from zero failures. C: deterministic active one-qubit and passive optimal-decoder calculations, explicitly different observables. D: an input-pulse witness, not the full worst-case memory depth W.','SmallCustom')
    table(directtable,[25,150,150,165])
    p('Passive redundancy improves lifetime only modestly in this range. Active repair yields much longer retention, at the cost of resetting r + 2 input qubits each cycle. Panel D shows why a uniform ceiling must not be presented as a statement that every architecture has the same memory at every size.','SmallCustom')
    story.append(PageBreak())
    heading('Quantum channels and the cooling construction')
    p(quantum)
    story.append(Image(str(OUT/'quantum_and_noise.png'),width=490,height=490*4.6/15))
    p(cooltext)
    table(cooltable,[45,45,190,210])
    p(coolinglimit,'SmallCustom')
    story.append(PageBreak())
    heading('Two wording changes supported by the controls')
    p(wording1)
    p(wording2)
    heading('Limits of this validation')
    p(caveats)
    heading('Reproduction and evidence')
    p(reproduce)
    p('Versions: Python '+meta['python']+', NumPy '+meta['numpy']+', SciPy '+meta['scipy']+', Matplotlib '+meta['matplotlib']+'. Master seed: '+str(meta['seed'])+'. All evidence is in results/empirical-2026-10-16/; the protocol is experiments/empirical-2026-10-16.md.','SmallCustom')
    def footer(canvas,doc):
        canvas.setStrokeColor(colors.HexColor('#DCE3E9'))
        canvas.line(18*mm,16*mm,A4[0]-18*mm,16*mm)
        canvas.setFont('Helvetica',8)
        canvas.setFillColor(colors.HexColor('#536271'))
        canvas.drawString(18*mm,11*mm,'Fresh-qubits memory | Numerical evidence | 16 October 2026')
        canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page))
    doc=SimpleDocTemplate(str(OUT/'validation_report.pdf'),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=17*mm,bottomMargin=22*mm,title='Independent numerical validation of noisy-reservoir memory',author='Numerical validation report')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='sha256.json'}
    for name in ('scripts/validate_empirical.py','scripts/build_validation_report.py','src/fresh_qubits_memory/validation.py','tests/test_validation.py','experiments/empirical-2026-10-16.md'):
        manifest[name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    (OUT/'sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(OUT/'validation_report.pdf')


if __name__=='__main__':
    main()

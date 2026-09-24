#!/usr/bin/env python3
"""Quick Verification of all headline numerical values from archived result CSVs.
"""
from pathlib import Path
import json, math, pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[1]

def close(a,b,tol=0.015):
    if not np.isfinite(a) or abs(float(a)-float(b))>tol:
        raise AssertionError(f'{a} != {b} (tol={tol})')

def one(df, **kw):
    x=df
    for k,v in kw.items(): x=x[x[k]==v]
    if len(x)!=1: raise AssertionError(f'Expected one row for {kw}, got {len(x)}')
    return x.iloc[0]

# Table 1 headline values
T=pd.read_csv(ROOT/'results/paper_tables/table1_retrieval_metrics.csv')
checks=[
 ('EigenPlaces','amstertime','Full PWF',44.35,65.64),('EigenPlaces','msls','Full PWF',85.33,91.31),
 ('EigenPlaces','nordland','Full PWF',50.50,78.75),('CosPlace','amstertime','Full PWF',35.58,54.75),
 ('CosPlace','msls','Full PWF',80.50,85.14),('CosPlace','nordland','Full PWF',55.75,81.00)]
for bb,ds,m,r1,r5 in checks:
    r=one(T,backbone=bb,dataset=ds,method=m); close(r.R1,r1); close(r.R5,r5)

# Six inferential families = exactly 90 tests
A=pd.read_csv(ROOT/'results/inferential_families/all_confirmatory_tests_90.csv')
expected={'EP_original_main_27':27,'EP_original_component_21':21,'EP_original_conditional_LU_6':6,
          'EP_reviewer_fair_controls_12':12,'CP_reviewer_controls_18':18,'CP_reviewer_LU_increment_6':6}
assert len(A)==90
assert A.groupby('family').size().to_dict()==expected

# EigenPlaces fair-control significant claims
E=pd.read_csv(ROOT/'results/inferential_families/eigenplaces_fair_controls_BH12.csv')
r=one(E,dataset='amstertime',comparison='TunedConstTop10_fine',metric='R@5'); close(r.diff_pp,1.05605); close(r.q_BH12,.031994,1e-5)
r=one(E,dataset='amstertime',comparison='TunedSG_fine',metric='R@5'); close(r.diff_pp,2.19334); close(r.q_BH12,.004799,1e-5)
r=one(E,dataset='nordland',comparison='TunedConstTop10_fine',metric='R@5'); close(r.diff_pp,2.75); close(r.q_BH12,.031994,1e-5)
assert not (E[E.metric=='R@1'].q_BH12 < .05).any()

# CosPlace family significant claims
C=pd.read_csv(ROOT/'results/inferential_families/cosplace_controls_BH18.csv')
for comp,metric,diff,q in [('PWF - Visual-only','R@1',1.94963,.007199),('PWF - Visual-only','R@5',1.62470,.007199),('PWF - Tuned-ConstTop10','R@1',-1.54346,.014397)]:
    r=one(C,dataset='amstertime',comparison=comp,metric=metric); close(r.difference_pp,diff); close(r.BH_FDR_q_18,q,1e-5)
assert int(C['significant_BH_0.05'].sum())==3

# LU increment
L=pd.read_csv(ROOT/'results/inferential_families/cosplace_LU_increment_BH6.csv')
r=one(L,dataset='nordland',metric='R@5'); close(r.difference_pp,-1.5); close(r.BH_FDR_q_6,.031194,1e-5)
assert int(L['significant_BH_0.05'].sum())==1

# Oracle examples
O=pd.read_csv(ROOT/'results/diagnostics/adaptive_vs_oracle_constant_envelope.csv')
r=one(O,backbone='EigenPlaces',dataset='amstertime',method='Full PWF'); close(r.method_minus_best_constant_R1,-.73111)
r=one(O,backbone='EigenPlaces',dataset='nordland',method='Full PWF'); close(r.method_minus_best_constant_R5,.25)
r=one(O,backbone='CosPlace',dataset='amstertime',method='Full PWF'); close(r.method_minus_best_constant_R5,-1.8684)

# Alpha means
AD=pd.read_csv(ROOT/'results/diagnostics/alpha_distribution_all_settings.csv')
for bb,lo,hi in [('EigenPlaces',.71,.73),('CosPlace',.85,.87)]:
    vals=AD[(AD.backbone==bb)&(AD.method=='Full PWF')]['mean']; assert ((vals>=lo)&(vals<=hi)).all()

# LU validity / conditional OR directions
V=pd.read_csv(ROOT/'results/paper_tables/table2_lu_validity.csv')
for bb in ['EigenPlaces','CosPlace']:
    for ds in ['AmsterTime','MSLS held-out']:
        r=one(V,backbone=bb,dataset=ds); assert r.OR_CI_low>1.0
    r=one(V,backbone=bb,dataset='Nordland-aligned'); assert r.OR_CI_low<1.0<r.OR_CI_high

print('PASS: all frozen headline numerical claims and family counts verified.')

#!/usr/bin/env python3
"""Build the final six inferential families and the canonical 90-test audit table.

Historical EigenPlaces CSVs under archive/legacy predate the final exclusion of
structurally deterministic R@10 contrasts. The submitted manuscript defines:
  * 27-test original main family
  * 21-test original component family
  * 6-test original conditional-LU family
  * 12-test EigenPlaces reviewer fair-control family
  * 18-test CosPlace reviewer control family
  * 6-test CosPlace reviewer LU-increment family
This script makes the filtering and BH-FDR recomputation explicit and then joins
all six families into all_confirmatory_tests_90.csv.
"""
from pathlib import Path
import sys, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.stats_utils import bh_fdr
legacy=ROOT/'archive/legacy'; out=ROOT/'results/inferential_families'

# Final 27-test EigenPlaces main family.
m=pd.read_csv(legacy/'main_comparisons_bh_fdr_correction_36.csv')
m=m[(m.Metric.isin(['R@1','R@5'])) | ((m.Metric=='R@10') & m.Comparison.str.contains('B2_fixed_0.5'))].copy()
assert len(m)==27
m['BH_FDR_q_value_final27']=bh_fdr(m.bootstrap_p_two_sided)
m['Significant_after_BH_FDR_final27']=m.BH_FDR_q_value_final27 < .05
m.to_csv(out/'eigenplaces_original_main_BH27.csv',index=False)

# Final 21-test EigenPlaces component family.
c=pd.read_csv(legacy/'final_component_ablation_bootstrap_bh_27.csv')
c=c[(c.Mechanism=='Pool restriction') | c.Metric.isin(['R@1','R@5'])].copy()
assert len(c)==21
c['BH_FDR_q_value_final21']=bh_fdr(c.bootstrap_p_two_sided)
c['Significant_after_BH_FDR_final21']=c.BH_FDR_q_value_final21 < .05
c.to_csv(out/'eigenplaces_original_component_BH21.csv',index=False)

# Standardise all six families.
def frame(family,stage,backbone,dataset,comparison,metric,diff,lo,hi,p,q,sig,source):
    return pd.DataFrame({'family':family,'stage':stage,'backbone':backbone,'dataset':dataset,
        'comparison':comparison,'metric':metric,'difference_pp':diff,'CI_low':lo,'CI_high':hi,
        'p_raw':p,'q_BH':q,'significant_BH_0.05':sig,'source_file':source})
parts=[]
parts.append(frame('EP_original_main_27','original_v6','EigenPlaces',m.Dataset,m.Comparison,m.Metric,m.Difference_pp,m.CI_low,m.CI_high,m.bootstrap_p_two_sided,m.BH_FDR_q_value_final27,m.Significant_after_BH_FDR_final27,'results/inferential_families/eigenplaces_original_main_BH27.csv'))
parts.append(frame('EP_original_component_21','original_v6','EigenPlaces',c.Dataset,c.Comparison,c.Metric,c.Difference_pp,c.CI_low,c.CI_high,c.bootstrap_p_two_sided,c.BH_FDR_q_value_final21,c.Significant_after_BH_FDR_final21,'results/inferential_families/eigenplaces_original_component_BH21.csv'))
cl=pd.read_csv(out/'eigenplaces_conditional_LU_BH6.csv')
parts.append(frame('EP_original_conditional_LU_6','original_v6','EigenPlaces',cl.Dataset,'Full PWF - SU-only (High-SU/Low-LU)',cl.Metric,cl.Difference_pp,cl.CI_low,cl.CI_high,cl.bootstrap_p_two_sided,cl.BH_FDR_q_value,cl['Significant_after_BH_FDR_0.05'],'results/inferential_families/eigenplaces_conditional_LU_BH6.csv'))
e=pd.read_csv(out/'eigenplaces_fair_controls_BH12.csv')
parts.append(frame('EP_reviewer_fair_controls_12','reviewer_extension','EigenPlaces',e.dataset,'PWF - '+e.comparison,e.metric,e.diff_pp,e.CI_low,e.CI_high,e.p_raw,e.q_BH12,e.q_BH12<.05,'results/inferential_families/eigenplaces_fair_controls_BH12.csv'))
cp=pd.read_csv(out/'cosplace_controls_BH18.csv')
parts.append(frame('CP_reviewer_controls_18','reviewer_extension','CosPlace',cp.dataset,cp.comparison,cp.metric,cp.difference_pp,cp.CI_low,cp.CI_high,cp.p_raw,cp.BH_FDR_q_18,cp['significant_BH_0.05'],'results/inferential_families/cosplace_controls_BH18.csv'))
ci=pd.read_csv(out/'cosplace_LU_increment_BH6.csv')
parts.append(frame('CP_reviewer_LU_increment_6','reviewer_extension','CosPlace',ci.dataset,ci.comparison,ci.metric,ci.difference_pp,ci.CI_low,ci.CI_high,ci.p_raw,ci.BH_FDR_q_6,ci['significant_BH_0.05'],'results/inferential_families/cosplace_LU_increment_BH6.csv'))
all90=pd.concat(parts,ignore_index=True)
assert len(all90)==90
all90.to_csv(out/'all_confirmatory_tests_90.csv',index=False)
print('Built canonical families:', all90.groupby('family').size().to_dict())

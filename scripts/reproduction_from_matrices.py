#!/usr/bin/env python3
"""Reproduce Table 1 metrics from release asset.

Usage:
  python scripts/reproduction_from_matrices.py

The script uses NumPy stable sorting. See KNOWN_NOTES.md for the single EigenPlaces/
AmsterTime visual-only exact-tie difference relative to the historical auto_VPR/torch.topk result.
"""
from pathlib import Path
import argparse, sys, numpy as np, pandas as pd, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.pwf import topk_idx,pwf_retrieve,constant_top10,sigmoid_gated_top10,recalls

CONFIG=json.loads((ROOT/'configs/final_config.json').read_text())

def load(p): return np.load(p,allow_pickle=False)

def main(data):
    data=Path(data); split=load(data/'msls_calibration_split_indices.npz'); EVAL=split['evaluation_indices']
    rows=[]
    for bb in ['EigenPlaces','CosPlace']:
        key='eigenplaces' if bb=='EigenPlaces' else 'cosplace'
        cfg=CONFIG[bb]
        for ds in ['amstertime','msls','nordland']:
            V=load(data/f'{ds}_{key}_visual.npy')
            L=load(data/f'{ds}_language.npy')
            P=load(data/f'{ds}_positive.npy').astype(bool)
            if ds=='msls': V,L,P=V[EVAL],L[EVAL],P[EVAL]
            visual=topk_idx(V,10)
            const=constant_top10(V,L,cfg['constant_alpha'])
            su,a_su=pwf_retrieve(V,L,cfg['PWF']['rho'],cfg['PWF']['M_c'],su_only=True)
            pwf,a=pwf_retrieve(V,L,cfg['PWF']['rho'],cfg['PWF']['M_c'])
            sg,_=sigmoid_gated_top10(V,L,cfg['SG']['tau'],cfg['SG']['theta'])
            for name,ret in [('Visual-only',visual),('Source-tuned constant',const),('SU-only',su),('Full PWF',pwf),('Source-tuned SG',sg)]:
                rr=recalls(ret,P); rows.append([bb,ds,name,rr['R@1'],rr['R@5'],rr['R@10']])
    df=pd.DataFrame(rows,columns=['backbone','dataset','method','R1','R5','R10'])
    print(df.to_string(index=False))
    out=ROOT/'results/reproducibility/reproduced_table1_numpy_stable.csv'; df.to_csv(out,index=False)
    print('\nSaved:',out)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--data-dir',required=True); args=ap.parse_args(); main(args.data_dir)

'''
Created on Dec 23, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
from e_evaluator import config_3_eval_single

if __name__ == "__main__":

    hyp_path = './data/ixagroup_ehu_spaceeval/configuration3'
    gold_path = './data/gold'
    outpath = './results/utd/run3'

    config_3_eval_single(hyp_path, gold_path, outpath)

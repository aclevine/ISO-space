'''
Created on Dec 23, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
from e_evaluator import config_2_eval_single

if __name__ == "__main__":

    hyp_path = './data/ixagroup_ehu_spaceeval/Test.configuration2'
    gold_path = './data/gold'
    outpath = './results/ixa/'

    config_2_eval_single(hyp_path, gold_path, outpath)

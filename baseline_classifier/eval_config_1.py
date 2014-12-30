'''
Created on Dec 23, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
from e_evaluator import config_1_eval_single

if __name__ == "__main__":

    hyp_path = './data/baseline/configuration1/e'
    gold_path = './data/gold'
    outpath = './results/baseline/'

    config_1_eval_single(hyp_path, gold_path, outpath)

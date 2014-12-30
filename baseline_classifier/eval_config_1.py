'''
Created on Dec 23, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
from e_evaluator import config_1_eval_single

if __name__ == "__main__":

    hyp_path = './data/task8_hrijp_crf_vw_system_submission/configuration1/'
    gold_path = './data/gold'
    outpath = './results/hrijp_crf_vw/'

    config_1_eval_single(hyp_path, gold_path, outpath)

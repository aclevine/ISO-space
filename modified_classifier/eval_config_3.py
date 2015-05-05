#!/usr/bin/env python
"""
Created on Dec 23, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
"""
from util.e_evaluator import config_3_eval_single
import re

if __name__ == "__main__":

    # load paths
    with open('config.txt') as fo:
        text = fo.read()
    hyp_path = re.findall('CONFIG_3_EVAL_PATH = (.*)', text)[0]
    gold_path = re.findall('GOLD_PATH = (.*)', text)[0]
    outpath = re.findall('RESULT_PATH = (.*)', text)[0]

    # run evaluations    

    config_3_eval_single(hyp_path, gold_path, outpath)

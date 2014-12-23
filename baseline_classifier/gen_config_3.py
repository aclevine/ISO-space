'''
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

generate documents for configuration 3 tasks
'''
from util.iso_space_classifier import copy_folder
from util.d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks
import os, re

def generate_config_3_xml(config_path):
    # load config
    with open(config_path, 'r') as fo:
        config_data = fo.read()
        
    train_path = re.findall('TRAINING_PATH =\s+(.+)', config_data)[0]

    clean_path = re.findall('CONFIG_1_GEN_PATH =\s+(.+)', config_data)[0]
    
    # prepare output paths
    hyp_path_list = map(lambda x: os.path.join(clean_path, x), 
                    ['1', 'a', 'b', 'c', 'd', 'e'])
    for hyp_path in hyp_path_list:
        if not os.path.exists(hyp_path):
            os.makedirs(hyp_path)
    hyp_a, hyp_b = hyp_path_list

    # 2b + c
    copy_folder(clean_path, hyp_a)
    generate_qslinks(train_path, hyp_a, hyp_a)
    generate_olinks(train_path, hyp_a, hyp_a)
    generate_movelinks(train_path, hyp_a, hyp_a)

    copy_folder(hyp_a, hyp_b)


if __name__ == "__main__":
    
    generate_config_3_xml('config.txt')

 
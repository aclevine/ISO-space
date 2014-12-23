'''
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
from util.iso_space_classifier import copy_folder
from util.a_identify_spans import generate_elements
from util.b_identify_types import generate_tags
from util.d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks
from util.c_fill_tag_attrs import generate_attributes
import re, os

def generate_config_1_xml(config_path):

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
    hyp_1, hyp_a, hyp_b, hyp_c, hyp_d, hyp_e = hyp_path_list


    # pre-1a
    generate_elements(train_path, clean_path, hyp_1)

    # 1a + 1b
    generate_tags(train_path, hyp_1, clean_path, hyp_a)
    copy_folder(hyp_a, hyp_b)
     
    # 1c
    generate_attributes(train_path, hyp_c, hyp_c)
 
    #1d + e
    copy_folder(hyp_c, hyp_d)
    generate_qslinks(train_path, hyp_d, hyp_d)
    generate_olinks(train_path, hyp_d, hyp_d)
    generate_movelinks(train_path, hyp_d, hyp_d)
 
    copy_folder(hyp_d, hyp_e)

if __name__ == "__main__":

    generate_config_1_xml('config.txt')


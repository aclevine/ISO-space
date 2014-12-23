'''
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

generate documents for configuration 2 tasks
'''
from util.iso_space_classifier import copy_folder
from d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks
from c_fill_tag_attrs import generate_attributes

if __name__ == "__main__":
    
    train_path = './data/training'
    clean_path = './data/final/test/configuration2/0'
    hyp_a = './data/final/test/configuration2/a'
    hyp_b = './data/final/test/configuration2/b'
    hyp_c = './data/final/test/configuration2/c'
    
    # 2a
    copy_folder(clean_path, hyp_a)
    generate_attributes(train_path, hyp_a, hyp_a)
 
    # 2b + c
    copy_folder(hyp_a, hyp_b)
    generate_qslinks(train_path, hyp_b, hyp_b)
    generate_olinks(train_path, hyp_b, hyp_b)
    generate_movelinks(train_path, hyp_b, hyp_b)
 
    copy_folder(hyp_b, hyp_c)

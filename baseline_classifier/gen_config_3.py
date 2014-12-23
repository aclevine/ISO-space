'''
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

generate documents for configuration 3 tasks
'''
from util.iso_space_classifier import copy_folder
from util.d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks

if __name__ == "__main__":
    
    train_path = './data/training'
    clean_path = './data/final/test/configuration3/0'
    hyp_a = './data/final/test/configuration3/a'
    hyp_b = './data/final/test/configuration3/b'
    
    # 2b + c
    copy_folder(clean_path, hyp_a)
    generate_qslinks(train_path, hyp_a, hyp_a)
    generate_olinks(train_path, hyp_a, hyp_a)
    generate_movelinks(train_path, hyp_a, hyp_a)

    copy_folder(hyp_a, hyp_b)

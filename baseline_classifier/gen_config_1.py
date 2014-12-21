'''
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
from a_identify_spans import generate_elements
from util.demo import copy_folder
from b_identify_types import generate_tags
from d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks
from c_fill_tag_attrs import generate_attributes

if __name__ == "__main__":
    
    # pre-1a
    train_path = './data/training'
    clean_path = './data/final/test/configuration1/0'
    
    hyp_1 = './data/final/test/configuration1/1'
    hyp_a = './data/final/test/configuration1/a'    
    hyp_b = './data/final/test/configuration1/b'   
    hyp_c = './data/final/test/configuration1/c'   
    hyp_d = './data/final/test/configuration1/d'
    hyp_e = './data/final/test/configuration1/e'
        
    # 1a + 1b
    generate_elements(train_path, clean_path, hyp_1)
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

'''
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

generate documents for configuration 3 tasks
'''
from a_identify_spans import generate_elements
from util.demo import copy_folder
from b_identify_types import generate_tags
from d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks
from c_fill_tag_attrs import generate_attributes

if __name__ == "__main__":
    
    train_path = './data/training'
    clean_path = './data/final/test/configuration3/0'
    hyp_a = './data/final/test/configuration3/a'
    hyp_b = './data/final/test/configuration3/b'
    
    # 2b + c
    copy_folder(clean_path, hyp_b)
    generate_qslinks(train_path, hyp_a, hyp_a)
    generate_olinks(train_path, hyp_a, hyp_a)
    generate_movelinks(train_path, hyp_a, hyp_a)

    copy_folder(hyp_a, hyp_b)

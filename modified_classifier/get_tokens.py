'''
Created on Apr 21, 2015

@author: ACL73
'''
import os, re
from util.corpora.tokenizer import Tokenizer

if __name__ == "__main__":

    outpath = 'resources/tokens.txt'
    rootdir_list = ['data/training','data/gold']

    #clean out folder
    with open(outpath,'w+') as fw:
        fw.write(' ')

    #write text field for all files in folders
    for rootdir in rootdir_list:
        for folder, subs, files in os.walk(rootdir):
            for filename in files:
                in_path = os.path.abspath(os.path.join(folder, filename))
                start = False
                with open(in_path, 'r') as fr:
                    for line in fr:
                        if re.search('<TEXT><!\[CDATA\[', line):
                                start = True
                                continue
                        if re.search('</TEXT>', line):
                                start = False
                                break
                        if start:
                            t = Tokenizer(line.decode('utf8')) # Marc tokenizer
                            for s in t.tokenize_text().sentences:
                                sent = s.as_pairs()
                                for tok_lex in sent:
                                    tok, lex = tok_lex
                                    with open(outpath,'a+') as fw:
                                        fw.write(tok.lower().encode('utf8'))
                                        fw.write(' ')

'''
Created on Apr 24, 2015

@author: Aaron Levine
@email: aclevine@brandeis.edu

Wrapper to load resources into python environment
'''
import json, os

class Vectors():
    
    def __init__(self,path='vectors.sorted.txt'):
        self.path=path
        self.dict=self.make_dict()
        
    def make_dict(self):
        v_dict = {}
        with open(self.path,'r') as fo:
            for line in fo:
                vector = line.split()[:-1]
                if vector[0] in v_dict:
                    print "ERROR: overlapping values"
                v_dict[vector[0]] = vector[1:]
        return v_dict


class Clusters():
    
    def __init__(self,path='classes.sorted.txt'):
        self.path=path
        self.dict = self.make_dict()
        
    def make_dict(self):
        c_dict = {}
        with open(self.path,'r') as fo:
            for line in fo:
                vector = line.split()
                if vector[0] in c_dict:
                    print "ERROR: overlapping values"
                c_dict[vector[0]] = vector[1]
        return c_dict


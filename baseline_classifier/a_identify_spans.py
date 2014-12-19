'''
Created on Sep 19, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

a) Identify spans of spatial elements including locations, paths, events and other spatial entities.    
'''
#===============================================================================
from util.Corpora.corpus import Extent
import nltk
from util.demo import Demo
#===============================================================================

class Token(Extent):
    """pull labels and features for classifying tag extents using individual tokens"""
    # LABEL EXTRACT
    def unconsumed_tag(self):
        """does tag span multiple tokens?"""
        if int(self.tag.get("end", -1)) == self.lex[0].end:
            return True
        else:
            return False
    
    # FEATURE EXTRACT
    def upper_case(self):
        """ is token upper case"""
        if str.isupper(str(self.token[0][0].encode('utf-8'))):
            return {'upper_case':True}
        else:
            return {'upper_case':False}

    def next_upper_case(self):
        """ is next token upper case"""
        if self.next_tokens != [] and str.isupper(str(self.next_tokens[0][0].encode('utf-8'))):
            return {'next_upper_case':True}
        else:
            return {'next_upper_case':False}

    def prev_upper_case(self):
        """ is next token upper case"""
        if self.prev_tokens != [] and str.isupper(str(self.prev_tokens[-1][0].encode('utf-8'))):
            return {'prev_upper_case':True}
        else:
            return {'prev_upper_case':False}

    def pos_tag(self):
        tag = nltk.pos_tag(self.token[:1])[0][1]
        return {'pos_tag': tag}

    def next_pos_tag(self):
        if self.next_tokens != []:
            tag = nltk.pos_tag(self.next_tokens[0][:1])[0][1]
            return {'next_pos_tag': tag}
        return {'next_pos_tag': 'None'}

    def prev_pos_tag(self):
        if self.prev_tokens != []:
            tag = nltk.pos_tag(self.prev_tokens[-1][:1])[0][1]
            return {'prev_pos_tag': tag}
        return {'prev_pos_tag': 'None'}

    def simple_tag(self):
        tag = nltk.pos_tag(self.token[:1])[0][1]
        return {'simple_tag': tag[0]}

    def next_simple_tag(self):
        if self.next_tokens != []:
            tag = nltk.pos_tag(self.next_tokens[0][:1])[0][1]
            return {'next_simple_tag': tag[0]}
        return {'next_simple_tag': 'None'}

    def prev_simple_tag(self):
        if self.prev_tokens != []:
            tag = nltk.pos_tag(self.prev_tokens[-1][:1])[0][1]
            return {'prev_simple_tag': tag[0]}
        return {'prev_simple_tag': 'None'}

#===============================================================================
def get_token_indices(sentence, tag_dict):
    indices = []
    for i in range(len(sentence)):
        start = i
        end = i + 1
        indices.append((start, end))
    return indices

class Spans_Demo(Demo):
    def __init__(self, train_path='./training', test_path = ''):
        super(Spans_Demo, self).__init__(train_path = train_path, test_path = test_path)
        self.feature_functions = [
                                  lambda x: x.upper_case(),
                                  lambda x: x.next_upper_case(),
                                  lambda x: x.prev_upper_case(),
                                  lambda x: x.pos_tag(),
                                  lambda x: x.next_pos_tag(),
                                  lambda x: x.prev_pos_tag(),
                                  lambda x: x.simple_tag(),
                                  lambda x: x.next_simple_tag(),
                                  lambda x: x.prev_simple_tag()
                                 ] 
        self.label_function = lambda x: str(x.unconsumed_tag())
        self.indices_function = get_token_indices
        self.extent_class = Token

if __name__ == "__main__":
    
    # SINGLE STAGE
#     d = Spans_Demo(train_path = './test_dev', test_path = './test_dev')
#     pred, test_data = d.run_demo(2)
    
    # FULL RUNTHROUGH
    d = Spans_Demo(train_path = './test_dev', test_path = './test_dev')
    pred, test_data = d.run_demo()
    
    ongoing = False
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
        if pred[offsets] == 'True':
            if not ongoing:
                start = extent.lex[0].begin
                ongoing = True
        else:
            if ongoing:
                ongoing = False
            else:
                start = extent.lex[0].begin
            print extent.document.basename
            print start, extent.lex[-1].end
            SEND_TO_DOC = {'name': 'SPAN', 'start': start, 'end': extent.lex[-1].end}


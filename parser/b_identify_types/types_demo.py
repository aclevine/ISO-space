'''
Created on Oct 31, 2014

@author: ACL73
'''
#===============================================================================
#===============================================================================

# TESTING
def all_inst(instances):
    return instances

def tagged_inst(instances):
    data = []
    for x in instances:
        if x.tag != {}:
            data.append(x)    
    return data

def typing_demo(doc_path = './training', split=0.8, limit=all_inst):
    # select train/test data        
    c = Corpus(doc_path)
    extents = list(c.extents(get_tag_and_no_tag_indices, Tag))
    i = int(len(extents) * split)
    train_data = extents[:i]
    test_data = extents[i:]
 
    features = [lambda x: x.curr_token(),
                lambda x: x.prev_n_bag_of_words(100),
                lambda x: x.next_n_bag_of_words(100)]
    
    #features = [lambda x: x.bag_of_words(3)] #awful performance
    any_pred = ['False' for x in test_data]
    for type_name in ['PATH', 
                      'PLACE', 'MOTION', 'NONMOTION_EVENT', 
                      'SPATIAL_ENTITY', 'MOTION_SIGNAL' 'HAS_TAG']:
        label = lambda x: str(x.is_type(type_name))
       
        clf = SKClassifier(LogisticRegression(), label, features)
        clf.add_labels(['True', 'False']) #binary classifier
        try:
            clf.train(train_data)
           
            pred = clf.classify(test_data)    
            print '\n\n%s:' %(type_name)
            clf.evaluate(pred, [label(x) for x in test_data])
            for i, p in enumerate(pred):
                if p == 'True':
                    any_pred[i] = 'True'
        except:
            continue
    print '\n\n%s:' %('ANY')
    any_label = lambda x: str(x.is_type('HAS_TAG'))
    clf.evaluate(any_pred, [any_label(x) for x in test_data])


if __name__ == "__main__":
    typing_demo(limit=tagged_inst)

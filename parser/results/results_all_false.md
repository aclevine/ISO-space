Data:
21836 train tokens
5460 test tokens

label = lambda x: str(x.is_type(<TYPE>))

features = [lambda x: x.curr_token(),
            lambda x: x.prev_n_bag_of_words(9),
            lambda x: x.next_n_bag_of_words(9)]


PATH:
row = predicted, column = actual
      True False  
True  0.0  0.0    
False 98.0 5362.0 

========= True =========
Precision: nan 
Recall: 0.000000
F-measure nan
========= False =========
Precision: 0.982051 
Recall: 1.000000
F-measure 0.990944

Accuracy: 98.205128%


PLACE:
row = predicted, column = actual
      True  False  
True  0.0   0.0    
False 339.0 5121.0 

========= True =========
Precision: nan 
Recall: 0.000000
F-measure nan
========= False =========
Precision: 0.937912 
Recall: 1.000000
F-measure 0.967961

Accuracy: 93.791209%


MOTION:
row = predicted, column = actual
      True  False  
True  0.0   0.0    
False 158.0 5302.0 

========= True =========
Precision: nan 
Recall: 0.000000
F-measure nan
========= False =========
Precision: 0.971062 
Recall: 1.000000
F-measure 0.985319

Accuracy: 97.106227%


NONMOTION_EVENT:
row = predicted, column = actual
      True  False  
True  0.0   0.0    
False 377.0 5083.0 

========= True =========
Precision: nan 
Recall: 0.000000
F-measure nan
========= False =========
Precision: 0.930952 
Recall: 1.000000
F-measure 0.964242

Accuracy: 93.095238%


SPATIAL_ENTITY:
row = predicted, column = actual
      True  False  
True  0.0   0.0    
False 275.0 5185.0 

========= True =========
Precision: nan 
Recall: 0.000000
F-measure nan
========= False =========
Precision: 0.949634 
Recall: 1.000000
F-measure 0.974166

Accuracy: 94.963370%


Data:
21836 train tokens
5460 test tokens

label = lambda x: str(x.is_type(<TYPE>))

features = [lambda x: x.bag_of_words(3)]



PATH:
row = predicted, column = actual
      True  False  
True  1.0   6.0    
False 108.0 5345.0 

========= True =========
Precision: 0.142857 
Recall: 0.009174
F-measure 0.017241
========= False =========
Precision: 0.980194 
Recall: 0.998879
F-measure 0.989448

Accuracy: 97.912088%


PLACE:
row = predicted, column = actual
      True  False  
True  51.0  41.0   
False 373.0 4995.0 

========= True =========
Precision: 0.554348 
Recall: 0.120283
F-measure 0.197674
========= False =========
Precision: 0.930514 
Recall: 0.991859
F-measure 0.960208

Accuracy: 92.417582%


MOTION:
row = predicted, column = actual
      True  False  
True  1.0   5.0    
False 157.0 5297.0 

========= True =========
Precision: 0.166667 
Recall: 0.006329
F-measure 0.012195
========= False =========
Precision: 0.971214 
Recall: 0.999057
F-measure 0.984939

Accuracy: 97.032967%


NONMOTION_EVENT:
row = predicted, column = actual
      True  False  
True  23.0  42.0   
False 397.0 4998.0 

========= True =========
Precision: 0.353846 
Recall: 0.054762
F-measure 0.094845
========= False =========
Precision: 0.926413 
Recall: 0.991667
F-measure 0.957930

Accuracy: 91.959707%


SPATIAL_ENTITY:
row = predicted, column = actual
      True  False  
True  4.0   17.0   
False 277.0 5162.0 

========= True =========
Precision: 0.190476 
Recall: 0.014235
F-measure 0.026490
========= False =========
Precision: 0.949072 
Recall: 0.996718
F-measure 0.972311

Accuracy: 94.615385%


## are current and next token upper case:

upper_case(test_data)

row = predicted, column = actual
      True   False   
True  3.0    39.0    
False 5346.0 21908.0 

========= True =========
Precision: 0.071429 
Recall: 0.000561
F-measure 0.001113
========= False =========
Precision: 0.803845 
Recall: 0.998223
F-measure 0.890551

Accuracy: 80.271835%



## are next and current token nouns:

noun(test_data)

row = predicted, column = actual
      True   False   
True  296.0  1977.0  
False 5053.0 19970.0 

========= True =========
Precision: 0.130224 
Recall: 0.055337
F-measure 0.077670
========= False =========
Precision: 0.798066 
Recall: 0.909919
F-measure 0.850330

Accuracy: 74.245311%


## 
    features = [lambda x: x.upper_case(),
                lambda x: x.next_upper_case(),
                lambda x: x.prev_upper_case(),
                lambda x: x.pos_tag(),
                lambda x: x.next_pos_tag(),
                lambda x: x.prev_pos_tag(),
                lambda x: x.simple_tag(),
                lambda x: x.next_simple_tag(),
                lambda x: x.prev_simple_tag()]

				

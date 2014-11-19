## limit test set to only tagged items:

	limit = True

	label = lambda x: str(x.is_type(<TYPE>))

    features = [lambda x: x.curr_token(),
                lambda x: x.prev_n_bag_of_words(100),
                lambda x: x.next_n_bag_of_words(100)]


PATH:
row = predicted, column = actual
      True False  
True  15.0 1.0    
False 43.0 1014.0 

========= True =========
Precision: 0.937500 
Recall: 0.258621
F-measure 0.405405
========= False =========
Precision: 0.959319 
Recall: 0.999015
F-measure 0.978764

Accuracy: 95.899348%


PLACE:
row = predicted, column = actual
      True  False 
True  149.0 46.0  
False 120.0 758.0 

========= True =========
Precision: 0.764103 
Recall: 0.553903
F-measure 0.642241
========= False =========
Precision: 0.863326 
Recall: 0.942786
F-measure 0.901308

Accuracy: 84.529357%


MOTION:
row = predicted, column = actual
      True False 
True  56.0 17.0  
False 94.0 906.0 

========= True =========
Precision: 0.767123 
Recall: 0.373333
F-measure 0.502242
========= False =========
Precision: 0.906000 
Recall: 0.981582
F-measure 0.942278

Accuracy: 89.655172%


NONMOTION_EVENT:
row = predicted, column = actual
      True  False 
True  246.0 40.0  
False 106.0 681.0 

========= True =========
Precision: 0.860140 
Recall: 0.698864
F-measure 0.771160
========= False =========
Precision: 0.865311 
Recall: 0.944521
F-measure 0.903183

Accuracy: 86.393290%


SPATIAL_ENTITY:
row = predicted, column = actual
      True  False 
True  186.0 7.0   
False 88.0  792.0 

========= True =========
Precision: 0.963731 
Recall: 0.678832
F-measure 0.796574
========= False =========
Precision: 0.900000 
Recall: 0.991239
F-measure 0.943419

Accuracy: 91.146319%


COMBINED_ANY:
row = predicted, column = actual
      True  False 
True  564.0 0.0   
False 509.0 0.0   

========= True =========
Precision: 1.000000 
Recall: 0.525629
F-measure 0.689065
========= False =========
Precision: 0.000000 
Recall: nan
F-measure nan

Accuracy: 52.562908%
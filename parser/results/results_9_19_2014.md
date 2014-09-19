Data:
21836 train tokens
5460 test tokens

label = lambda x: str(x.is_type(<TYPE>))

features = [lambda x: x.curr_token(),
            lambda x: x.prev_n_bag_of_words(100),
            lambda x: x.next_n_bag_of_words(100)]




PATH:
row = predicted, column = actual
      True False  
True  31.0 4.0    
False 78.0 5347.0 

========= True =========
Precision: 0.885714 
Recall: 0.284404
F-measure 0.430556
========= False =========
Precision: 0.985622 
Recall: 0.999252
F-measure 0.992390

Accuracy: 98.498168%


PLACE:
row = predicted, column = actual
      True  False  
True  179.0 29.0   
False 245.0 5007.0 

========= True =========
Precision: 0.860577 
Recall: 0.422170
F-measure 0.566456
========= False =========
Precision: 0.953351 
Recall: 0.994241
F-measure 0.973367

Accuracy: 94.981685%


MOTION:
row = predicted, column = actual
      True  False  
True  23.0  1.0    
False 135.0 5301.0 

========= True =========
Precision: 0.958333 
Recall: 0.145570
F-measure 0.252747
========= False =========
Precision: 0.975166 
Recall: 0.999811
F-measure 0.987335

Accuracy: 97.509158%


NONMOTION_EVENT:
row = predicted, column = actual
      True  False  
True  191.0 28.0   
False 229.0 5012.0 

========= True =========
Precision: 0.872146 
Recall: 0.454762
F-measure 0.597809
========= False =========
Precision: 0.956306 
Recall: 0.994444
F-measure 0.975002

Accuracy: 95.293040%


SPATIAL_ENTITY:
row = predicted, column = actual
      True  False  
True  146.0 23.0   
False 135.0 5156.0 

========= True =========
Precision: 0.863905 
Recall: 0.519573
F-measure 0.648889
========= False =========
Precision: 0.974485 
Recall: 0.995559
F-measure 0.984909

Accuracy: 97.106227%


ANY:
row = predicted, column = actual
      True  False  
True  274.0 69.0   
False 812.0 3587.0 

========= True =========
Precision: 0.798834 
Recall: 0.252302
F-measure 0.383485
========= False =========
Precision: 0.815413 
Recall: 0.981127
F-measure 0.890627

Accuracy: 81.421341%
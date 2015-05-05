# TASK
http://alt.qcri.org/semeval2015/task8/


# MAIN MODULES

## EVALUATION MODULES

### config.txt

use this text file to set the paths for:

	GOLD_PATH: folders with gold-standard annotated xml documents
	
	CONFIG_1_EVAL_PATH: folders with computer annotated xml documents for task 1
	
	CONFIG_2_EVAL_PATH: folders with computer annotated xml documents for task 2
	
	CONFIG_3_EVAL_PATH: folders with computer annotated xml documents for task 3

	RESULT_PATH: folder to write metrics for a given evaluation task for 	

### eval_config_1.py
	
Writes text files "1a.txt", "1b.txt", ..., "1e.txt", with metrics for semeval tasks 1a to 1e
to the RESULT_PATH folder

### eval_config_2.py

Writes text files "2a.txt", "2b.txt", and "2c.txt", with metrics for semeval tasks 2a to 2c
to the RESULT_PATH folder

### eval_config_3.py

Writes text files "3a.txt" and "3b.txt", with metrics for semeval tasks 3a and 3b
to the RESULT_PATH folder


## GENERATE MODULES

### config.txt

use this text file to set the paths for:

	TRAINING_PATH: path with tagged XML data to train baseline classifiers
	
	CONFIG_1_GEN_PATH: path with clean XML data to generate tagged documents for configuration 1 task

	CONFIG_2_GEN_PATH: path with clean XML data to generate tagged documents for configuration 2 task

	CONFIG_3_GEN_PATH = path with clean XML data to generate tagged documents for configuration 3 task

### gen_config_1.py

Creates folders "1", "a", "b", "c", "d" and "e", each containing tagged versions 
of XML docs in <CONFIG_1_GEN_PATH>. Each folder coincides with that subtask in task 1. 
Folder e contains fully tagged documents.

### gen_config_2.py

Creates folders "a", "b", and "c", each containing tagged versions 
of XML docs in <CONFIG_2_GEN_PATH>. Each folder coincides with that subtask in task 2. 
Folder c contains fully tagged documents.

### gen_config_3.py

Creates folders "a" and "b", each containing tagged versions 
of XML docs in <CONFIG_3_GEN_PATH>. Each folder coincides with that subtask in task 3. 
Folder b contains fully tagged documents.



## UTIL

To test new feature and label functions:

	1) add <function> that returns a dictionary with <feature_name> : <feature_value> pairs 
		to top level Token / <tag_type>_Tag / etc. class
		
		ex:
			class MotionSignalTag(Tag):
				## LABEL EXTRACT
				def motion_signal_type(self):
					return self.tag['motion_signal_type']

				## FEATURE EXTRACT
				def curr_token(self):
					return {'curr_extent_' + ' '.join(self.token):True}

				def curr_pos_tags(self):
					return {'curr_tags_' + nltk.pos_tag(tok)[0][1]:True for tok in self.token}
					
	2) add <function> to <classifier_type>_Classifier as "lambda x: x.<function>()" in:
		-label function: as item returned by get_label_function()
		-if feature function: as item returned by get_feature_functions() list

		ex:
			class MotionSignalTypeClassifier(MotionSignalClassifier):
				def get_label_function(self):
					return lambda x: str(x.motion_signal_type())

				def get_feature_functions(self):
					return [
							lambda x: x.curr_token(),
							lambda x: x.curr_pos_tags()
						   ]


### util.a_identify_spans.py 

baseline maximum entropy model for chunking named entities.

	ex: [..., "Bavarian", "Alps", ...] => [..., "Bavarian Alps", ...]

	
### util.b_identify_types.py 

Set of 7 baseline maximum entropy models for identifying each chunk as
one or more of the 7 extent / spatial element tag types: PATH, PLACE, MOTION, 
NONMOTION_EVENT, SPATIAL_ENTITY, MOTION_SIGNAL, and SPATIAL_SIGNAL

	ex:  [..., "Scott", "runs", "the", "Bavarian Alps", ...] =>
		 [..., SPATIAL_ENTITY, MOTION, _, PLACE, ...]



### util.c_motion_signal.py + util.c_motion.py + util.c_nonmotion_event.py + util.c_path.py +
### util.c_place.py + util.c_spatial_entity.py + util.c_spatial_signal.py

7 sets of 5-10 baseline maximum entropy models for identifying attributes 
for each of the 7 extent / spatial element tag types. 
The number of models depends on the required attributes for a given tag type.

	ex:
		<MOTION id="m0" start="469" end="473" text="trip"/>
		<PLACE id="pl0" start="477" end="483" text="Munich"/>
		...

		=>

		<MOTION id="m0" start="469" end="473" text="trip" countable="TRUE" motion_class="REACH" motion_sense="LITERAL" motion_type="PATH"/>
		<PLACE id="pl0" start="477" end="483" text="Munich" countable="TRUE" dcl="FALSE" dimensionality="AREA" form="NAM"/>
		...
		
### util.d_move_link.py + util.d_olink.py + util.d_qs_link.py
		
3 sets of 5-10 baseline maximum entropy models for identifying spatial links
(potential relations between 2-3 previously tagged spatial elements in the same sentence) 
and their attributes. 3 link tag types are orientation links (olinks), 
qualitative spatial links (qs links) and movement links (movelink).
As before, The number of models depends on the required attributes for a given link tag type.

### util.e_evaluator.py

contains all the functions used by eval_config_1, eval_config_2, and eval_config_3



## UTIL.COPORA

### util.corpora.tokenizer.py + util.corpora.abbreviation.py

tokenizer written by Marc Verhagen to return both tokens and lexes, which contains
the start and ending offsets of a token in document being tokenized.
abbreviation.py contains resources for the tokenizer to deal with specialized constructions,
such as 1apostrophes.

### util.corpora.corpus.py

Classes for validating and parsing ISO-space XML documents.
Extent class handles preprocessing used by all feature extraction functions.



## UTIL.MODEL

### util.model.alphabet.py

two-way codebook for use by scikit-learn models in classifier.py

### util.model.evaluator.py

System for generating confusion matrix, recall, precision, f1 for a given classification task.
Built to be directly integrated with sk_classifier.py, so it can reuse a model's codebook for 
constructing a human readable confusion matrix.

### util.model.sk_classifier.py


### util.model.baseline_classifier.py

framework for splitting documents into test and training sets,
training and classifying the split data, and evaluating extent and link tags.


###


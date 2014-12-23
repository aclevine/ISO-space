# -*- coding: utf-8 -*-

"""A list of errors when using Sparser on ISO-Space document text.
"""

#an odd error with sparser
"""
/home/u/fall11/sdworman/iso-space/Tokenized++/CP/45_N_23_E.xml
Traceback (most recent call last):
  File "script.py", line 52, in <module>
    process.process(doc, golddir=args.source)
  File "/home/u/fall11/sdworman/iso-space/ISO-space/crf/process.py", line 148, in process
    edges = p(' '.join([x for x in tokens]), split=True)
  File "/home/u/fall11/sdworman/iso-space/ISO-space/crf/sparser/sparser.py", line 126, in p2edges
    new_edge = Edge(edgeStr)
  File "/home/u/fall11/sdworman/iso-space/ISO-space/crf/sparser/sparser.py", line 70, in __init__
    self.edges = [x for x in m.group('edge').split(' ') if x]
AttributeError: 'NoneType' object has no attribute 'group'
"""

#another odd error
#breaks on this sentence:
#Using field tracks we needed plenty of time to reach the village of Sinpetru German , where we met several very friendly women , who told us some interesting historical facts of their village .
#breaks at this spot on the word village/town: the [village] of Sinpetru German
"""
(p "(p "Using field tracks we needed plenty of time to reach the town of Sinpetru German , where we met several very friendly women , who told us some interesting historical facts of their town .")
/home/u/fall11/sdworman/iso-space/Tokenized++/CP/46_N_21_E.xml
> Break: Another case of a category for the region: #<ref-category VILLAGE>
> While executing: SPARSER::GIVE-KIND-ITS-NAME, in process toplevel(2).
"""

"""
/home/u/fall11/sdworman/iso-space/Tokenized++/CP/46_N_22_E.xml
> Break: Object passed in as 'individual' parameter is of
>        unexpected type: WORD
>        #<word "5">
> While executing: SPARSER::VALUE-OF, in process toplevel(2).
"""

#sparser parses this incorrectly
#edge: "gps '"
#which causes the string delimiter to overflow, making the xml formatted wrong
"""
The GPS 'said' that from here till the point we had 200 meters left (Point).
"""

#really?!
#26-Dec-2002 -- This confluence can be found 1,5 km to the west from Icafalau ( Ikafalva ) in Covasna county , Romania .
#sparser messes up on european style of measurements: x,y [measurement]
"""
/home/u/fall11/sdworman/iso-space/Tokenized++/CP/46_N_26_E.xml
> Break: Object passed in as 'individual' parameter is of
>        unexpected type: WORD
>        #<word "5">
> While executing: SPARSER::VALUE-OF, in process toplevel(2).
"""

#another error!
#the problem is here:
#( after printing some multimaps and a visit report or two ( always the optimist )
#there's an open paren inside but it has no matching close! haha
"""
Tokenized++/CP/47_N_25_E.xml
Fortunately Eastern Europe - even outside the EU is easy travelling for EU citizens and I was able to jump in the car ( after printing some multimaps and a visit report or two ( always the optimist ) and drive across Serbia , and Bulgaria to Romania with few hassles ( those there were concentrated on car insurance ) .
> Break: double parens
> While executing: MARK-OPEN-PAREN, in process listener(1).
> Type :GO to continue, :POP to abort, :R for a list of available restarts.
> If continued: Return from BREAK.
> Type :? for other options.
"""

"""
/home/u/fall11/sdworman/iso-space/Tokenized++/RFC/Bogota.xml
> Break: Another case of a category for the region: #<ref-category TOWN>
> While executing: SPARSER::GIVE-KIND-ITS-NAME, in process toplevel(2).
> Break: new case for :all-caps SINGLE-CAPITALIZED-LETTER
> While executing: SUBSUMING-VARIANT, in process listener(1).
> Type :GO to continue, :POP to abort, :R for a list of available restarts.
> If continued: Return from BREAK.
> Type :? for other options.
1 > :q
? (p "But , while most families I see seem to have good family and community lives , the health care is poor and they have nowhere near the options that or my friends have a $  minimum wage her is $ 200 a month .")
but , while [ most families][ i][ see seem] to [ have][ good family] and [ community][ lives] , [ the health care][ is poor] and [ they][ have nowhere] near [ the options][ that] or [ my friends][ have][ a $  minimum wage][ her][ is][ $ 200][ a month][ .]
"""

#another possible error:
#/home/u/fall11/sdworman/iso-space/Tokenized++/RFC/Durango.xml
#it breaks on this sentence:
#No , we are not racing , as the movie on the right suggests
#.(I say this only because it looks like they will beat me ) .
#it's not a sparser error, but rather ner error

#close paren error (again)
#error is single quotation around a NNP
#"I am now in Guerrero Negro , in the state of southern Baja California
#here: ( ' Baja California Sur ' ) ,
#where I have just washed my clothes and enjoyed a shower ."
"""
/home/u/fall11/sdworman/iso-space/Tokenized++/RFC/Ensenada.xml
> Break: new case for single-quote while looking to extend a capitalized sequence.
>        The next word is #<word CLOSE-PAREN> at position 21
> While executing: SPARSER::CHECKOUT-SINGLE-QUOTE-FOR-CAPSEQ, in process toplevel(2).
"""


#two errors:
#double quote mark
#a few reasons a $ " the end of the school year
#means I ca na$t give presentations
"""
/home/u/fall11/sdworman/iso-space/Tokenized++/RFC/LaPaz.xml
> Break: new case for :all-caps SINGLE-CAPITALIZED-LETTER
> While executing: SPARSER::SUBSUMING-VARIANT, in process toplevel(2).
"""

#another error
#it's this hyphen:
#(p "and the site of a major pre-Colombian city .")
"""
/home/u/fall11/sdworman/iso-space/Tokenized++/RFC/MexicoCity.xml
> Break: check args
> While executing: SPARSER::START-PRESERVE-SPACING-SECTION, in process toplevel(2).
"""

#another error (from test set)
#CP/48_N_10_E.xml
#broke on this sentence
#The GPS routed us through the village ' Rot an der Rot ' .
#because of the proper name in the single quotation marks
"""
> Break: new case for single-quote while looking to extend a capitalized sequence.
>        The next word is #<word PERIOD> at position 14
> While executing: SPARSER::CHECKOUT-SINGLE-QUOTE-FOR-CAPSEQ, in process toplevel(2).
"""

#yet another error
#here's the mistake
#Confluence-Point ' .
"""
/home/u/fall11/sdworman/iso-space/Test++/CP/48_N_8_E.xml
> Break: new case for single-quote while looking to extend a capitalized sequence.
>        The next word is #<word PERIOD> at position 5
> While executing: SPARSER::CHECKOUT-SINGLE-QUOTE-FOR-CAPSEQ, in process toplevel(2).
"""

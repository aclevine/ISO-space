This script computes Fleiss' Kappa to determine how well a group of raters/annotators
agree on the labels for a set of objects.  A score of 1.0 means perfect agreement, while
0.0 would suggest no agreement at all.  In general one can take a kappa >= 0.80 to suggest
strong agreement among raters.

The script has several flags to determine what it considers to be an object and what
it expects for input.  In general the script assumes that all XMLs in the same directory level
represent the same annotated document over different annotators.

By default the algorithm considers all tokens (from the Lexer) to be objects each annotator
has assigned a label.  The label is determined by whether that token is part of a tag extent.
Otherwise the rater has assigned it the 'None' category.

Computes Fleiss' Kappa for a single task, outputting the score.  It certainly does help most tokens are assigned 'None'
across all raters (spatial objects are 'sparse').

> python fleiss_main.py /path/to/Adjudication/47_N_27_E

0.805336480521

The -x flag tells the algorithm to only consider tag extents rather than tokens.  This results
in a much lower agreement, since if a tag extent differs even slightly from at least one other
annotator's, then it is considered its own object and hence brings down the score, as all other
annotators did not have that exact extent.

>python fleiss_main.py -x /users/sethmachine/desktop/Adjudication/47_N_27_E

0.657599059806

The -m flag tells the algorithm to only consider tag extents which matched exactly across
ALL raters.  The -m flag can be used with tokens, but it does not change the agreement, since
presumably all annotators have the exact same set of tokens.  This score is generally highest
of all, since if annotators have labeled the exact same text, they almost always agree on its
tag/label.

One use of this could be to determine if a distinction between a set of tags is very confusing /
ill-defined for the annotators.  If this score was exceptionally low, it could certainly imply
the categories in their current understanding are difficult to separate.

>python fleiss_main.py -m -x /users/sethmachine/desktop/Adjudication/47_N_27_E

0.886386837207

To deal with arbitrary amounts of XMLs / annotation tasks, the -r flag can be specified to inform
the script to search all directories exhausitvely and calculate the kappa for each such directory
found.  This flag will also print the average agreement over all tasks.

>python fleiss_main.py -r /users/sethmachine/desktop/Adjudication

46_N_21_E : 0.848039752399

48_N_27_E : 0.767482328789

...

47_N_22_E : 0.822032183289

48_N_8_E : 0.793415272094

Average: 0.799632416455

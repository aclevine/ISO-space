################################################################################
__author__ = "Zachary Yocum"
__email__ = "zyocum@brandeis.edu"
################################################################################
from collections import Counter
from itertools import chain
from operator import itemgetter
from tokenizer import *
from corpus import *

# Root directory containing the corpus data files
home = os.environ['HOME']
space_eval = os.path.join(home, 'Dropbox/ISO-Space/SemEval/')
# Corpus instances
train = Corpus(os.path.join(space_eval, 'Tokenized'))
test = Corpus(os.path.join(space_eval, 'Test', 'Test'))
anc = Corpus(os.path.join(space_eval, 'ANC'))
dcp = Corpus(os.path.join(space_eval, 'DCP'))
rfc = Corpus(os.path.join(space_eval, 'RFC'))
corpora = {
    'Train' : train,
    'Test' : test,
    'ANC' : anc,
    'DCP' : dcp,
    'RFC' : rfc
}

tag_types = (
    'MOTION',
    'MOTION_SIGNAL',
    'NONMOTION_EVENT',
    'PATH',
    'PLACE',
    'SPATIAL_ENTITY',
    'SPATIAL_SIGNAL',
    'MOVELINK',
    'OLINK',
    'QSLINK'
)

def main():
    for label, corpus in sorted(corpora.items()):
        document_count = 0
        sentence_count = 0
        token_counter = Counter()
        tag_counter = Counter()
        for document in corpus.documents():
            document_count += 1
            sentence_count += len(document.tokenizer.sentences)
            token_counter.update(token for _, _, token in document.tokenizer.lexes)
            tag_counter.update(
                tag.name for tag in document.tags(ttypes=tag_types)
            )
        token_count = len(list(token_counter.elements()))
        print label
        print '\t#documents : {}'.format(document_count)
        print '\t#sentences : {}'.format(sentence_count)
        print '\t#tokens : {}'.format(token_count)
        for tag_type, count in tag_counter.items():
            print '\t#{} : {}'.format(tag_type, count)

if __name__ == '__main__':
    main()

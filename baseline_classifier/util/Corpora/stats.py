################################################################################
__author__ = "Zachary Yocum"
__email__ = "zyocum@brandeis.edu"
################################################################################
from itertools import chain
from tokenizer import *
from corpus import *

# Root directory containing the corpus data files
home = os.environ['HOME']
space_eval_path = os.path.join(home, 'Dropbox/ISO-Space/SemEval/Training')
# Corpus instance
SpaceEval = Corpus(space_eval_path)
# Extract the texts from each document and tokenize them
texts = map(Document.text, SpaceEval.documents())
tokenizers = (Tokenizer(text) for text in texts)
tokenized_texts = map(Tokenizer.tokenize_text, tokenizers)
# Generate sentence tokens
sentences = chain(
    *list(tokenized_text.sentences for tokenized_text in tokenized_texts)
)
# Generate word tokens
words = (sentence.tokens for sentence in sentences)

def main():
    # Accumulators for word and sentence token counts
    word_count = 0
    sentence_count = 0
    # Iterate over all sentences
    for sentence in sentences:
        # Increment the counts
        word_count += len(sentence.tokens)
        sentence_count += 1
    # Print the total counts
    print '\n'.join([
        'Total # of word tokens : {0}',
        'Total # of sentence tokens : {1}'
    ]).format(word_count, sentence_count)
    # Print each text as a new-line separated list of tokens and sentence boundary markers
    for document, tokenized_text in zip(SpaceEval.documents(), tokenized_texts):
        out_file = document.name.split(os.sep)[-1].encode('utf-8')
        tokenized_text.print_as_xmlstring()

if __name__ == '__main__':
    main()

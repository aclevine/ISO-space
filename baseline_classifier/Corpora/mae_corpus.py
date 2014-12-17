from mae_document import *

class Corpus:
    """A collection of MAE annotation documents."""
    
    def __init__(self, directory, files):
        self.paths = [directory + file for file in files]
        self.documents = self.collect_documents()
        self.sentences = self.collect_sentences()
        self.tag_dictionary = self.tag_dict()
        self.tags = self.collect_tags()
        self.tag_types = self.tag_set()
    
    def collect_documents(self):
        """Returns a list of documents in the corpus."""
        documents = []
        ignored = []
        for path in self.paths:
            try:
                current_document = MAE_Document(path)
            except UnsupportedMIMETypeError as e:
                ignored.append(str(e))
            else:
                documents.append(current_document)
        if ignored:
            print "Some files were ignored:"
            for file in ignored:
                print "\t%s" % file
        return documents
    
    def collect_sentences(self):
        """Returns a list of all sentences in the corpus."""
        sentences = []
        for document in self.documents:
            for sentence_token in document.sentences:
                sentences.append(sentence_token)
        return sentences
    
    def collect_tags(self):
        """Returns a list of all tags in the corpus."""
        tags = []
        for document in self.documents:
            for tag_token in document.tags:
                tags.append(tag_token)
        return tags
    
    def tag_set(self):
        """Returns a set of tag types present in the corpus."""
        tag_set = set()
        for tag_token in self.tags:
            tag_set.add(tag_token['tag'])
        return tag_set
    
    def tag_dict(self):
        """Returns a dictionary of tag_type-tag key-value pairs."""
        tag_dict = dict()
        for document in self.documents:
            for tag in document.tags:
                tag_type = tag['tag']
                tag_dict[tag_type] = tag_dict.get(tag_type, []) + [tag]
        return tag_dict
    
    def tag_counts(self, types=[]):
        """Prints a list of tag counts from the tag dictionary"""
        if not types:
            types = self.tag_types
        for tag_type in types:
            print "\t%15s : %-10s" % (tag_type, len(self.tag_dictionary[tag_type]))

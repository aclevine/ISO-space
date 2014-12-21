"""Utility classes

Every class in here should be fully functional. 
You don't need to modify anything unless you want to.

"""
import json

class Alphabet(object):
    """Two way map for label/feature and label/feature index

    It is an essentially a code book for labels or features
    This class makes it convenient for us to use numpy.array
    instead of dictionary because it allows us to use index instead of
    label string. The implemention of classifiers uses label index space
    instead of label string space.
    """
    def __init__(self):
        self._index_to_label = {0: 'FALSE'}
        self._label_to_index = {'FALSE': 0}
        self.num_labels = 1

    def size(self):
        return self.num_labels

    def has_label(self, label):
        return label in self._label_to_index

    def get_label(self, index):
        """Get label from index"""
        if index >= self.num_labels:
            raise KeyError("There are %d labels but the index is %d" % (self.num_labels, index))
        return self._index_to_label[index]

    def get_index(self, label):
        """Get index from label"""
        if label in self._label_to_index:
            return self._label_to_index[label]
        else:
            return 

    def add(self, label):
        """Add an index for the label if it's a new label"""
        if label not in self._label_to_index:
            self._label_to_index[label] = self.num_labels
            self._index_to_label[self.num_labels] = label
            self.num_labels += 1

    def json_dumps(self):
        return json.dumps(self.to_dict())

    @classmethod
    def json_loads(cls, json_string):
        json_dict = json.loads(json_string)
        return Alphabet.from_dict(json_dict)

    def to_dict(self):
        return {
            '_label_to_index': self._label_to_index,
            '_index_to_label': self._index_to_label
            }

    @classmethod
    def from_dict(cls, alphabet_dictionary):
        """Create an Alphabet from dictionary

        alphabet_dictionary is a dictionary with only one field
        _label_to_index which is a map from label to index
        and should be created with to_dict method above.
        """
        alphabet = cls()
        alphabet._label_to_index = alphabet_dictionary['_label_to_index']
        for label, index in alphabet._label_to_index.items():
            alphabet._index_to_label[index] = label
        # making sure that the dimension agrees
        assert(len(alphabet._index_to_label) == len(alphabet._label_to_index))
        alphabet.num_labels = len(alphabet._index_to_label)
        return alphabet

    def __len__(self):
        return self.size()

    def __eq__(self, other):
        return self._index_to_label == other._index_to_label and \
            self._label_to_index == other._label_to_index and \
            self.num_labels == other.num_labels

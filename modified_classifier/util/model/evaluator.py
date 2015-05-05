#!/usr/bin/env python
"""
Created on May 29, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

class for calculating and printing
confusion matrix, recall, precision, f1 
for a given classification task.
"""
import numpy

class ConfusionMatrix(object):
    """Confusion matrix """

    def __init__(self, label_codebook):
        self.label_codebook = label_codebook
        num_classes = label_codebook.size()
        self.matrix = numpy.zeros((num_classes, num_classes))

    def add_data(self, prediction_list, true_answer_list):
        """take list of predicted labels and actual labels"""
        for prediction, true_answer in zip(prediction_list, true_answer_list): 
            self.matrix[prediction, true_answer] += 1

    def compute_precision(self):
        """Returns a numpy.array where precision[i] = precision for class i""" 
        precision = numpy.zeros(self.label_codebook.size())
        for i in xrange(self.label_codebook.size()):
            denominator = numpy.sum(self.matrix[i])
            if denominator != 0:
                precision[i] = self.matrix[i][i] / denominator
            else:
                precision[i] = 0
        return precision

    def compute_recall(self):
        """Returns a numpy.array where recall[i] = recall for class i""" 
        recall = numpy.zeros(self.label_codebook.size())
        for i in xrange(self.label_codebook.size()):
            # Denominator here is sum over y-axis, returning as many sums as x-dim so get ith element.
            denominator = numpy.sum(self.matrix, axis=0)[i]
            if denominator != 0:
                recall[i] = self.matrix[i][i] / denominator
            else:
                recall[i] = 0
        return recall

    def compute_f1(self):
        """Returns a numpy.array where f1[i] = F1 score for class i""" 
        f1 = numpy.zeros(self.label_codebook.size())
        precision = self.compute_precision()
        recall = self.compute_recall()
        for i in xrange(self.label_codebook.size()):
            denominator = (precision[i] + recall[i])
            if denominator != 0:
                f1[i] = precision[i] * recall[i] / denominator
            else:
                f1[i] = 0
        f1 *= 2
        return f1

    def compute_accuracy(self):
        """Return accuracy rate given the information in the matrix"""
        accuracy = 0.0
        for i in xrange(self.label_codebook.size()):
            accuracy += self.matrix[i][i]
        accuracy /= numpy.sum(self.matrix)
        return accuracy

    def print_out(self):
        """Print out confusion matrix along with Macro-F1 score """
        # header for the confusion matrix
        header = [' '] + [self.label_codebook.get_label(i) for i in xrange(self.label_codebook.size())]
        rows = []
        # putting labels to the first column of rhw matrix
        for i in xrange(self.label_codebook.size()):
            row = [self.label_codebook.get_label(i)] + [str(self.matrix[i, j]) for j in xrange(len(self.matrix[i, ]))]
            rows.append(row)
        print "row = predicted, column = actual"
        print matrix_to_string(rows, header)

        # computing precision, recall, and f1
        precision = self.compute_precision()
        recall = self.compute_recall()
        f1 = self.compute_f1()
        for i in xrange(self.label_codebook.size()):
            print "========= %s =========" % self.label_codebook.get_label(i).title()
            print 'Precision: %f \nRecall: %f\nF-measure %f' % (precision[i], recall[i], f1[i])
        print '\nAccuracy: %f%%' % (self.compute_accuracy() * 100)
    

def matrix_to_string(matrix, header=None):
    """
    Args:
        matrix - Matrix representation (list with n rows of m elements).
        header -  Optional tuple or list with header elements to be displayed.
    Returns:
        nicely formatted matrix string
    """

    if isinstance(header, list):
        header = tuple(header)
    lengths = []
    if header:
        lengths = [len(column) for column in header]

    # finding the max length of each column
    for row in matrix:
        for column in row:
            i = row.index(column)
            column = str(column)
            column_length = len(column)
            try:
                max_length = lengths[i]
                if column_length > max_length:
                    lengths[i] = column_length
            except IndexError:
                lengths.append(column_length)

    # use the lengths to derive a formatting string
    lengths = tuple(lengths)
    format_string = ""
    for length in lengths:
        format_string += "%-" + str(length) + "s "
    format_string += "\n"

    # applying formatting string to get matrix string
    matrix_str = ""
    if header:
        matrix_str += format_string % header
    for row in matrix:
        matrix_str += format_string % tuple(row)

    return matrix_str



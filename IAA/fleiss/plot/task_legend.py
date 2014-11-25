# -*- coding: utf-8 -*-

"""Object to create a pgfplot LaTeX line plot.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

TIKZ_BEGIN = """\\begin{tikzpicture}[baseline = {(0,-6)}]
                \\node [draw,fill=white,anchor=north east] at (rel axis cs: 0.99,0.99) {\\shortstack[l]{
             """
TIKZ_END = '\\end{tikzpicture}'



class Legend(object):
    """Companion legend to a line plot to identify its labels.

    """
    def __init__(self, labels, title):
        self.labels = labels
        self.labelCount = len(labels)
        self.labelKeys = ''
        self.tex = ''
        self.title = '{\\underline{' + title + '}}\\\\'

    def _set_labelKeys(self):
        for num, label in enumerate(self.labels):
            self.labelKeys += '{\\footnotesize ' + str(num) + ' = ' + label.replace('_', '\_') + '}'
            if num < self.labelCount - 1:
                self.labelKeys += '\\\\'
        self.labelKeys += '}};'

    def make_tex(self):
        self._set_labelKeys()
        self.tex += TIKZ_BEGIN
        self.tex += self.title
        self.tex += self.labelKeys
        self.tex += TIKZ_END
            
    
                
            
        
        

    
        
        

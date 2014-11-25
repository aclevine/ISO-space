# -*- coding: utf-8 -*-

"""Object to create a pgfplot LaTeX line plot.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import task_legend

TIKZ_BEGIN = '\\begin{tikzpicture}[baseline = {(0,-5.75)}]'
TIKZ_END = '\\end{tikzpicture}'

AXIS_BEGIN = """\\begin{axis}[enlargelimits=0.01,legend style={at={(0.5,-0.15)},
            anchor=north,legend columns=-1}, ylabel={Fleiss' Kappa ($\kappa$)},
             xtick=data, ymin = 0.4, ymax = 1, xticklabel style={font=\\tiny}]"""
AXIS_END = '\\end{axis}'

ADDPLOT_BEGIN = '\\addplot coordinates {'
ADDPLOT_END = ' };\n'

LEGEND_BEGIN = '\\legend{'

class Line_Plot(object):
    """Generates pgfplot LaTeX for a line plot.

    Args:
        labelValues: A dictionary where each key is a line plot label
            and each value is the list of (object, value) for that key.
        includeKey: A boolean that determines whether to include a task legend
            that gives a verbose description of each object.

    Attributes:
        labelValues: A dictionary where each key is a line plot label
            and each value is the list of (object, value) for that key
        labels: A list of strings which are the labelValues keys.  
        includeKey: A boolean that determines whether to include a task legend
            that gives a verbose description of each object.
        ylabel: A string for the name of the values on the y-axis.
        coordinates: A string representing the pgfplot coordinates.
        tex: The string representation for the LaTeX code generating this plot.

    """
    def __init__(self, labelValues, ylabel, includeKey=True):
        self.labelValues = labelValues
        self.labels = labelValues.keys()
        self.tasks = [task for task in labelValues[labelValues.keys()[0]].keys()]
        self.includeKey = includeKey
        self.ylabel = ylabel
        self.coordinates = ''
        self.legend = LEGEND_BEGIN
        self.tex = ''

    def _set_coordinates(self):
        """Generates the \addplot coordinates for a plot

        Coordinates are strings of the form
        '\addplot coordinates {(task1, value), ..., (taskn, value) };'
        
        """
        for label in self.labels:
            addplot = ADDPLOT_BEGIN
            for task, value in enumerate(self.labelValues[label]):
                addplot += '(' + str(task) + ',' + str(self.labelValues[label][value]) + ') '
            addplot += ADDPLOT_END
            self.coordinates += addplot
            self.legend += label + ','
        self.legend = self.legend[:-1] + '}'
            
    def make_tex(self):
        """Creates the LaTeX code to generate the plot

        """
        self._set_coordinates()
        self.tex += TIKZ_BEGIN + '\n'
        self.tex += AXIS_BEGIN + '\n'
        self.tex += self.coordinates + '\n'
        self.tex += self.legend
        self.tex += AXIS_END + '\n'
        self.tex += TIKZ_END
        if self.includeKey:
            lg = task_legend.Legend(self.tasks, 'Tasks Key')
            lg.make_tex()
            s = '\\begin{adjustwidth}{-5em}{-3em}'
            s += '\\begin{figure}'
            s += '\\subfloat[hi]{'
            s += self.tex
            s += '}'
            s += '\subfloat[yo]{'
            s += lg.tex
            s += '}'
            s += '\\end{figure}'
            s += '\\end{adjustwidth}'
        self.tex = s
            
        
                
            
        
        

    
        
        

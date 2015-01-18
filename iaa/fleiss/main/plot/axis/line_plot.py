# -*- coding: utf-8 -*-

"""Object to create a pgfplot LaTeX line plot axis.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

AXIS_BEGIN = """\\begin{axis}[enlargelimits=0.01,legend style={at={(0.5,-0.15)},
            anchor=north,legend columns=-1}, ylabel={Fleiss' Kappa ($\kappa$)},
             xtick=data, ymin = 0.4, ymax = 1, xticklabel style={font=\\tiny}]"""
AXIS_END = '\\end{axis}'

class Axis(object):
    """Generates pgfplot LaTeX axis for a line plot.

    """
    def __init__(self, axis=AXIS_BEGIN):
        self.axis = axis
        
                
            
        
        

    
        
        

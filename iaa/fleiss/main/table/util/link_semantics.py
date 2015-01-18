# -*- coding: utf-8 -*-

"""Provides dictionary for link semantics

Calculating Fleiss' Kappa for links is more difficult, since it is a
ordered pairing of relationships among objects to a single label.  ISO-Space
allows for coercion of tags to different roles, e.g. a figure that is a motion
or a ground that is a spatial named entity.  Rather than iterate over the
powerset of all possible relations of tags, we only permutate all semantically
possible relations, defined herein.  For example, a QSLINK is a 3-tuple
relation of (figure, ground, SPATIAL_SIGNAL).  The third tag is always a
SPATIAL_SIGNAL.  The definitions here provide the necessary semantics for
reducing the final table size.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

ISO_LINKS = ['QSLINK', 'OLINK', 'MOVELINK', 'MLINK', 'METALINK', 'NONE']
INT_LINKS = {} #intepretation function of a link

INT_LINKS['QSLINK'] = {}
INT_LINKS['QSLINK']['toID'] = ('PLACE', 'PATH', 'SPATIAL_ENTITY', 'SPATIAL_NE', 'MOTION', 'EVENT')
INT_LINKS['QSLINK']['fromID'] = ('PLACE', 'PATH', 'SPATIAL_ENTITY', 'SPATIAL_NE', 'MOTION', 'EVENT')
INT_LINKS['QSLINK']['trigger'] = ('SPATIAL_SIGNAL')

INT_LINKS['OLINK'] = {}
INT_LINKS['OLINK']['toID'] = ('PLACE', 'PATH', 'SPATIAL_ENTITY', 'SPATIAL_NE', 'MOTION', 'EVENT')
INT_LINKS['OLINK']['fromID'] = ('PLACE', 'PATH', 'SPATIAL_ENTITY', 'SPATIAL_NE', 'MOTION', 'EVENT')
INT_LINKS['OLINK']['trigger'] = ('SPATIAL_SIGNAL')

#worry about this one later
#int_links['MOVELINK'] =

INT_LINKS['MLINK'] = {}
INT_LINKS['MLINK']['toID'] = ('PLACE', 'PATH', 'SPATIAL_ENTITY', 'MOTION', 'EVENT')
INT_LINKS['MLINK']['fromID'] = ('PLACE', 'PATH', 'SPATIAL_ENTITY', 'MOTION', 'EVENT')
INT_LINKS['MLINK']['trigger'] = ('MEASURE')

INT_LINKS['METALINK'] = {}
INT_LINKS['METALINK']['toID'] = ('PLACE', 'PATH', 'SPATIAL_ENTITY', 'MOTION', 'EVENT')
INT_LINKS['METALINK']['fromID'] = ('PLACE', 'PATH', 'SPATIAL_ENTITY', 'MOTION','EVENT')


# -*- coding: utf-8 -*-

"""Matching functions for Lex tokens to Sparser edges.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""


def ledges(edges, tokens):
	l = []
	for token in tokens:
		for edge in edges:
			if token.lower() in edge.word.split(' '):
				l.append((token, edge))
				edges.remove(edge)
				break
	return l

def ledge(edges, token):
    for edge in edges:
        if token.lower() in edge.word.split(' '):
            edges.remove(edge)
            return edge

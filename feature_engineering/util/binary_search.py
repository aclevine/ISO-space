# -*- coding: utf-8 -*-

"""Perform binary search over extent based ISO tags

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

START = 0
END = 1

def binary_search(token, sorted_tags, counter=1):
    """A simple binary search to determine which tag contains the token.

    Performs a binary search across all sorted_tags, sorted by start spans
    from least to greatest.  A tag matches a given token if the token's
    start and end spans are within that tag's start/end spans.
    Takes at most log(len(sorted_tags)) iterations.

    Args:
        token: A lexer token of the form (start, end, word), where
            start is the index of where the token begins,
            end is the index of where the token ends,
            and word is the actual token string.
        sorted_tags: A list of sorted ET tags from an annotated xml.
            The tags are sorted by the value of their start span.
        counter: An integer keeping track of the number of iterations,
            primarily for debugging purposes,
            i.e. counter <= log(len(sorted_tags))

    Returns:
        The tag which contains that token,
        or None if there is no tag which has that token.

    """
    if not sorted_tags: #token isn't tagged in any extent
        return None
    size = len(sorted_tags)
    index = size / 2
    curr = sorted_tags[index]
    if token[START] >= int(curr.attrib['start']) and token[END] <= int(curr.attrib['end']):
        return curr
    if token[START] > int(curr.attrib['end']):
        return binary_search(token, sorted_tags[index + 1:size], counter + 1)
    elif token[END] < int(curr.attrib['start']):
        return binary_search(token, sorted_tags[0:index], counter + 1)
    else: #if we get here, the token somehow overlaps extents!
        return None

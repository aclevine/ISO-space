# -*- coding: utf-8 -*-

"""Module to create mirrored directory structure from old to new directory.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os

def getXmls(dirpath, recursive=True):
    files = []
    for f in os.listdir(dirpath):
        fpath = os.path.join(dirpath, f)
        if os.path.isfile(fpath):
            if f.endswith('.xml'):
                files.append(fpath)
        if recursive:
            if os.path.isdir(fpath):
                files += getXmls(fpath, recursive)
    return files

def mkparentdirs(path):
    """Creates mirrored parent directories at the newdir.

    If the path contains a hierarchical directory structure which does
    not exist yet in the path's target location, then this function
    will create each parent directory recursively to mirror the path's
    original directory structure.  E.g. "a/b/c/d.txt" would cause this function
    to create parent directories c, d if they did not exist from the top level
    directory a to the actual file d.txt.

    Args:
        path: The mirrored absolute path to the file.

    Returns:
        None.  Creates the directory structure of the path if it
            does not yet exist.
    
    """
    currdir = os.path.dirname(path)
    stack = []
    while not os.path.exists(currdir):
        stack.append(currdir)
        currdir = os.path.dirname(currdir)
    while stack:
        pop = stack.pop()
        if not os.path.exists(pop):
            os.mkdir(pop)

def setup_newdir(filepath, olddir, newdir='', suffix='++', renew=False):
    if not newdir:
        newdir = olddir + suffix
    if not os.path.exists(newdir):
        os.mkdir(newdir)
    path = newdir + filepath.replace(olddir, '')
    print path
    if not renew:
        if os.path.exists(path): #don't redo our existing work :]
            #print test(td.TagDoc(filepath), td.TagDoc(path))
            return
    return path

    

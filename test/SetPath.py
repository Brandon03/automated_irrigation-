import os
import sys
import pdb

def SetPath(directory):
    """
    SetPath(directory)

    SetPath - set up the intend path to import witin automated_irrigation directory
    @args:
        directory: str, the name of directory
    """
    # Guards
    try:
        assert "/" != directory[0]
    except AssertionError:
        return "ERROR:Remove '/' in first line of directory insert "

    l = os.getcwd().split("/")
    #l[l.index("automated_irrigation")+1:len(l)+1] = []
    s = "/".join(l)
    p = os.path.join(s, directory)
    print(p)

    return sys.path.insert(0, p)

def WhichPath(directory):
    """
    WhichPath(directory)

    WhichPath - to set up dir path.

    @args:
    """
    # Guards
    try:
        assert "/" != directory[0]
    except AssertionError:
        return "ERROR:Remove '/' in first line of directory insert "

    l = os.getcwd().split("/")
    l[l.index("automated_irrigation")+1:len(l)+1] = []
    s = "/".join(l)
    p = os.path.join(s, directory)
    return p

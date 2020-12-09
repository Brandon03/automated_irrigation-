import sys
import os
from os.path import expanduser, join
from pprint import pprint

path = join(expanduser("~"), "irricon_proj/automated_irrigation/")

p = join(path, "program")
sys.path.insert(0, p)

import SetPath

def test_WhichPath():
    expect = "/Users/brandontong/irricon_proj/automated_irrigation/config/config.yaml"
    actual = SetPath.WhichPath("config/config.yaml")
    assert expect == actual, f"Expect {expect} but {actual}"

if __name__ == "__main__":
    test_WhichPath()

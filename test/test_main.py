"""
This is to test main.py
"""
import sys

import SetPath

p = SetPath.WhichPath("program")
sys.path.insert(0, p)

import main
import config

# --READ CONFIG DATA ----------------------------------------------
# The system will only read one fixed config file.
config_file = "test_config.yaml" # config filename

#config.ReadFile(config_file)

# -------------------------
def test_config():
    pass

def test_start():
    pass

def test_run():
    main.run(config_file=config_file)

if __name__ == "__main__":
    test_run()

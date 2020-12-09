"""
This is to test main.py
"""
import sys
import os
import schedule
import time

import SetPath

p = SetPath.WhichPath("program")
sys.path.insert(0, p)

import run
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
    run.run(config_file=config_file)

if __name__ == "__main__":
    schedule.every(2).minutes.do(test_run)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        

""" This is to test scheduler.py"""

import sys
import os
from os.path import join, expanduser
from crontab import CronTab

import SetPath

p = SetPath.WhichPath("program")
sys.path.insert(0, p)

import config
import scheduler

# --READ CONFIG DATA ----------------------------------------------
# The system will only read one fixed config file.
config_file = "test_config.yaml" # config filename

config.ReadFile(config_file)

def test_WriteTab():
    """ this is to test write() """

    #“At minute 2 past hour 1, 3, and 5 on every 2 day, every month.”
    
    f = SetPath.WhichPath("test/test_main.py")
    call = f"python3 {f}"

    scheduler.WriTab(call, config_file=config_file)

def test_list():
    """ This is to test list() """

    l = scheduler.list()
    print(l)
    return l

def test_delete():
    """ This is to test remove() """

    #scheduler.delete(cmd="2 1,3,5 */2 * * python3 hello.py")
    scheduler.delete(job="python3 hello.py", config_file=config_file)

if __name__ == "__main__":
   test_WriteTab()
   #test_list()
   #test_delete() # test fail

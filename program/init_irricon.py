"""
This script is to run the system automated
"""
import time
import asyncio

from datetime import datetime

import config
import SetPath
import features
import db
import pdb


# --READ CONFIG DATA ----------------------------------------------
config_file = "config.yaml" # return config directory path
config_path = SetPath.WhichPath("config") # config dir

# return dbname, tbname
##db config
def config_file(mode, d=None, filename=config_file):
    """
    config(mode, d=None, filename=config_file)

    This function handles config file:
    1. Read config file
    2. write config file
    3. create config file

    @ args:
        mode: str, r for read, w for write, c for create.
        d: dict, config content if mode is w
        filename: str, config filename (default='config.yaml')

    @ return:
        if mode == "r", it returns dicts.
        if mode == "w", it returns None.
        if mode == "c", it returns None.
    """
    if mode == "r":
        config.ReadFile(config_file)
    elif mode    == "w":
        config.WriteFile(d, config_file)
    elif mode ==  "c":
        config.CreateFile(config_file)

def start(config_file=config_file):
    """
    start(config_file)

    This function start running schedule in order to run main program.
    """
    print(f"Irricon START at {datetime.now().strftime('%Y-%m-%d %H:%m')}")

    # Read the config file
    assert config_file in os.listdir(config_path), "No file exist !"
    d_conf = config.ReadFile(config_file)
    print(d)

    # Create or update DB and scheduler according to config:
    db.CreateTable(config_file)

    # run the cron here ? or set on settings. 
    print("schedule set") # Dummuy code

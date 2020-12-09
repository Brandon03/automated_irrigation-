import time
import asyncio

from datetime import datetime

import config
import SetPath
import features
import db
import pdb

import os
import schedule

from pprint import pprint

# --READ CONFIG DATA ----------------------------------------------
config_file = "test_config.yaml" # return config directory path
config_path = SetPath.WhichPath("config") # config dir
def run(config_file=config_file):
    """
    run(config_file=config_file)

    This function is called by initial ,
    it will helps arrange proper data structure from
    config file for processing on features.

    It expect 1 input to 1 output itm.

    l = [(input_dict, output_dict)]

    @args:

    @returns:
    """
    l_config = config.ReadFile(config_file)

    # This is to rearrange the bundle for features
    l_in = l_config["hardware"]["input"]
    l_out = l_config["hardware"]["output"]

    l_col = []
    for r in l_in:
            d_in = r["channel_address"]
            for _r in l_out:
                    d_out = _r["channel_address"]
                    if d_in == d_out:
                        l_col.append((r, _r))

    pprint(l_col)

    asyncio.run(features.automated_SoilSensor(l_col, config_file))

    # tuple both moist sensor and valve
    # sensor is "s"; valve is "v"


import sys
import os
from os.path import expanduser, join
from pprint import pprint

# import from program/config.py
import SetPath

p = SetPath.WhichPath("program")
sys.path.insert(0, p)

import config
import SetPath

# Config file
config_file = "test_config.yaml"
config_path = SetPath.WhichPath("config") # config dir
config_content = {
"authentication":
{
"user": "brandon",
"password": "abc123"
},
"hardware": {
    "output" : [
        {
        "id": 1,
        "hardware": "pump",
        "port": 21,
        "type": "Centrifugal",
        "channel_address": "p1"
        },
        {
        "id": 2,
        "hardware": "valve",
        "port": 20,
        "type":"nozzle",
        "channel_address": "p1/n1/p1"
        },
        {
        "id":3,
        "hardware": "valve",
        "port": 19,
        "type": "drip",
        "channel_address": "p1/n2/p1"
        }],
    "input" : [
        {
        "channel_address": "p1/n1/p1",
        "port": 17,
        "hardware" : "moist sensor",
        "id": 4,
        "type": "sensor",
        "callibrate_condition": 50
        },
        {
        "channel_address": "p1/n2/p1",
        "port": 15,
        "hardware" : "moist sensor",
        "id": 5,
        "type": "sensor",
        "callibrate_condition": 60
        }]
},
"db": {"name": "../test/test_db.db",
       "table" : [{
        "name" : "HW_reading",
        "fields": "id int PRIMARY KEY, channel_address text NOT NULL, datetimes text NOT NULL, readings float NOT NULL "
        }]},
"schedule": {
"minute": "*",
"hour": "0800, 1800",
"day": "*",
"week": "*",
"month": "*",
"year": "*"
}
}


def test_CreateFile(filename=config_file):
    """
    test_CreateFile functions
    """
    if filename in os.listdir(config_path):
        expect = "Error 0 : file exist"
        actual = config.CreateFile(filename)
        assert expect == actual, "Expect error message {} but {}".format(expect, actual)

    else:
        f = join(path, "config", config_file)
        expect = "{} is created.".format(f)
        actual = config.CreateFile(filename)
        assert expect == actual, "Expect success message '{}' but '{}''".format(expect, actual)

def test_WriteFile(filename=config_file):
    """
    test_WriteFile functions
    """

    config.WriteFile(config_content, filename)

    # to prove if writefile is working:
    expect = config_content

    actual = config.WriteFile(filename)

    #assert expect == actual, "test_WriteFile expect {} but {}".format(expect, actual)


def test_ReadFile(filename=config_file):
    """
    test_ReadFile functions
    """
    expect = config_content
    actual = config.ReadFile(filename)

    assert expect == actual, "test_ReadFile expect {} but {}".format(expect, actual)

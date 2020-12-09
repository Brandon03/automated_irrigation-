import sys
import os
import asyncio
from pprint import pprint

import SetPath

p = SetPath.WhichPath("program")
sys.path.insert(0, p)

import features
import config

config_file = "test_config.yaml"
print(config_file)

def test_automated_SoilSensor():
    l = [({'callibrate_condition': 30, 'channel_address': 'p1/n1/p1', 'hardware': 'moist sensor', 'id': 4, 'port': 0, 'type': 'sensor'},
          {'channel_address': 'p1/n1/p1', 'hardware': 'valve', 'id': 2, 'port': 21, 'type': 'nozzle'}),
         ({'callibrate_condition': 40, 'channel_address': 'p1/n2/p1', 'hardware': 'moist sensor', 'id': 5, 'port': 7, 'type': 'sensor'},
          {'channel_address': 'p1/n2/p1', 'hardware': 'valve', 'id': 3, 'port': 20, 'type': 'drip'})]
    asyncio.run(features.automated_SoilSensor(l, config_file))

def test_manual_SoilSensor():
    """ This is to test manual_SoilSensor() """
    r = manual_SoilSensor(filename=config_file, save_to_db=False)
    pprint(r)
    assert r != None, "manual_SoilSensor() has no value."

if __name__ == "__main__":
    test_automated_SoilSensor()

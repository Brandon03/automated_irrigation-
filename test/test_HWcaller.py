""" This is to test HWcaller.py"""

import sys
import time
import os
from os.path import expanduser, join
from pprint import pprint

import SetPath

p = SetPath.WhichPath("program")
sys.path.insert(0, p)

import HWcaller

def test_ReadSoilMoisture():
    """ This is to test ReadSoilMoisture() function """
    sm = HWcaller.SoilMoist(7)
    return sm.read()

def test_led():
    """ None """
    led = HWcaller.Led(21)
    led.on()
    time.sleep(2)
    led.off()

if __name__ == "__main__":
    print(test_ReadSoilMoisture())
    #test_led()

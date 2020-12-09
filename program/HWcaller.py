#!/usr/bin/python
from gpiozero import DigitalInputDevice
import RPi.GPIO as GPIO
import spidev # to communicatewith self.spi device.
from pprint import pprint
from statistics import mean
from datetime import datetime
from numpy import interp # To scale values
from time import sleep
import pdb

class Led():
    """
    This class handle LED lighting as indication

    @args:
	- channel: int, port number

    @returns:
    """
    def __init__(self, channel):
        self.cha = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.cha, GPIO.OUT)

    def on(self):
        return GPIO.output(self.cha, GPIO.HIGH)

    def off(self):
        return GPIO.output(self.cha, GPIO.LOW)

class SoilMoist():
    """
    This class handle soil moisture sensors.

    @args:
	    - channel: int, port number from MCP3008

    @returns:
    """

    def __init__(self, channel):
        self.cha = channel
        self.spi = spidev.SpiDev() # Created an object
        self.spi.open(0,0)
        
	# Read MCP3008 data
    def read(self):
        """
        This function does:
            - Connect and collect NUM READINGS sequentially from multiple soil moist sensors.

	    @args:
	       - self.cha, port number.

        @returns:
            - it returns [{ soil_moist port, timestamp, magnitude, error }]
        """
        
        
        def analogInput(channel):
            """
            """
            self.spi.max_speed_hz = 1350000
            adc = self.spi.xfer2([1,(8+channel)<<4,0])
            data = ((adc[1]&3) << 8) + adc[2]
            return data

        l = []
        for loop in range(0,5):
            output = analogInput(self.cha)
            output = interp(output, [0, 1023], [100, 0])
            output = int(output)
            l.append(output)
        value = mean(l)
        timestamp = datetime.today().strftime("%Y-%m-%d %H:%M")
	#d = {"port": port, "timestamp": timestamp, "value": value}
        d = {"Sensor":self.cha, "datetimes":timestamp, "readings":value}
        #print(d)

        return d["readings"]
    
        self.spi.close()

""" This is to run all lineitems """
import asyncio
import sys
import os
import time
from datetime import datetime
from pprint import pprint
import pdb

import config
import SetPath
import db
import HWcaller # originally soil_moist2.py

# return config directory path
config_file = "config.yaml"
table_name = "HW_reading"

# program -------------------

async def irricon(hw_port,
                    config_file=config_file,
                    sleep_secs=30,
                    timeout=300):
    """

    Valve function is replaced by LED as an indicator of
    output.

    @args:
        hw_port: tuple of dict,

    """
    # Read config_file.
    d_config = config.ReadFile(config_file)

    # initialize hardware.
    soil_moist = HWcaller.SoilMoist(hw_port[0]["port"]) # input
    led = HWcaller.Led(hw_port[1]["port"]) # output

    # hardware address
    sm_addr = hw_port[0]["channel_address"]
    led_addr = hw_port[1]["channel_address"]

    # insert into sql db
    def insert_sql(config_file,
                    channel_address,
                    value,
                    table_name=table_name,
                    ):
        """
        insert transaction into sqlite db
        """
        d = {
        "channel_address": channel_address,
        "datetimes": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "readings": value
        }
        print(d)
        db.db_insert(table_name,
                  config_file,
                  **d)

    # This is to measure start time.
    start_time = time.perf_counter()

    while True:
        value = soil_moist.read()

        # Write SoilMoist records into SQLite DB
        insert_sql(config_file, sm_addr, value)

        # Conditions
        if value > hw_port[0]["callibrate_condition"]:
            # insert LOGGING in future
            #insert_sql(config_file, sm_addr, value)
            print(f"valve {sm_addr} close")
            led.off()
            break

        # insert LOGGING in future.
        ### insert code here.
        #insert_sql(config_file, sm_addr, value)
        print(f"valve {sm_addr} open")
        led.on()

        # check TimeOut:
        end_time = time.perf_counter() - start_time
        if end_time >= timeout:
            print("Timeout !")
            led.off()
            break

        await asyncio.sleep(sleep_secs)


async def automated_SoilSensor(l, config_file=config_file):
    """
    This is an automated functions, it will run the entire work once call.
    it read lineitems from config file and read values from soil moist sensor.

    it reads list which consists collections of

    (input_dict, output_dict)

    @ arg:
        l: list of hardware, [(input_dict, output_dict),...]
        filename: str, the filename

    @ returns:
        return cell # will write the details.
        ErrorCode if error:
    """
    ## !
    await asyncio.gather(*(irricon(row, config_file) for row in l))

def manual_SoilSensor(port_list, filename=config_file, save_to_db=False):
    """
    This is to read soil sensor manually.
    """
    #pdb.set_trace()
    lineitems = config.ReadFile(filename)
    c = [id for cell in lineitems for id in cell["SoilMoist"]]

    l = []
    for sensor in port_list:
        if sensor in c:
            value = HWcaller.ReadSoilMoist([sensor])
            l += value
        else:
            s = " {} sensor does not exist ".format([sensor])
            print(s)

    if save_to_db is True:
        db.db_insert(*l)

    return l

# This is to test the concurremcy limits
import asyncio
import time
import random
import yaml

async def sim_irricon(idx,
                      sleep_secs=10,
                      timeout=300):
    """

    Valve function is replaced by LED as an indicator of
    output.

    @args:
        hw_port: tuple of dict,

    """
    # Read config_file.
    #d_config = config.ReadFile(config_file)

    # initialize hardware.
    #soil_moist = HWcaller.SoilMoist(hw_port[0]["port"]) # input
    #led = HWcaller.Led(hw_port[1]["port"]) # output

    # hardware address
    #sm_addr = hw_port[0]["channel_address"]
    #led_addr = hw_port[1]["channel_address"]

    # insert into sql db
    #def insert_sql(config_file,
     #               channel_address,
     #               value,
     #               table_name=table_name,
      #              ):
       # """
       # insert transaction into sqlite db
        #"""
       # d = {
       # "channel_address": channel_address,
        #"datetimes": datetime.now().strftime("%Y-%m-%d %H:%m"),
        #"readings": value
       # }
       # print(d)
        #db.db_insert(table_name,
         #         config_file,
         #         **d)
         
    def log_result(d):
        with open("hw_feature.yaml", "a+") as fle:
            fle.write(yaml.dump(d))

    # This is to measure start time.
    start_time = time.perf_counter()

    while True:
        value = random.randint(0, 100)

        # Write SoilMoist records into SQLite DB
        #insert_sql(config_file, sm_addr, value)

        # Conditions
        if value > 60: #hw_port[0]["callibrate_condition"]:
            # insert LOGGING in future
            #insert_sql(config_file, sm_addr, value)
            d = {"id": idx, "valve": 1, "sensor": value, "timeout":0}
            log_result(d)
            print(d)
            #print(f"valve close")
            #led.off()
            break

        # insert LOGGING in future.
        ### insert code here.
        #insert_sql(config_file, sm_addr, value)
        #print(f"valve open")
        d = {"id": idx, "valve": 0, "sensor": value, "timeout":0}
        #led.on()

        # check TimeOut:
        end_time = time.perf_counter() - start_time
        if end_time >= timeout:
            d = {"id": idx, "valve": 1, "sensor": value, "timeout":1}
            log_result(d)
            #print("Timeout !")
            #led.off()
            break

        await asyncio.sleep(sleep_secs)
            
async def automated_SoilSensor(l):
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
    await asyncio.gather(*(sim_irricon(row) for row in l))
    
if __name__ == "__main__":
    l = [idx for idx in range(1, 101)]
    asyncio.run(automated_SoilSensor(l))
"""
Event loop
"""
import asyncio
import random

import config

async def read_sensor(id):
    con = True
    while con == True:
        value = random.randint(1, 100)

        if value > 50:
            #syncio.gather.cancel()
            print(f"sensor {id} is {value}")
            print(f"valve is close")
            break
        else:
            print(f"sensor {id} is {value}")
            print("valve is open")

        await asyncio.sleep(0.1)

async def main(*args):
     #await asyncio.gather(*(twins(n) for n in args))
     await asyncio.gather(*(read_sensor(n["id"]) for n in args))

if __name__ == "__main__":

    args = [{"id":1},
            {"id":2},
            {"id":3},
            {"id":4},
            {"id":5}
            ]
    asyncio.run(main(*args))

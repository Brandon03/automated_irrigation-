'''
Tutorial for python3 click

Format : python3 file.py commands OPTIONS arguments

# commands usually refer to the name of the function
'''
import click
import features
import config
import db
import pdb
from os.path import expanduser, join
from pprint import pprint

@click.group() # just like click.command() but act as a "group leader"
def cli():
    ''' This is program for automated irricon '''
    pass

# SetUp ---------------------------------------

@cli.command()
@click.option("--f", default="config.yaml", help="config f")
def read_config(f):
    """ Read all lineitems from config file """
    l = config.ReadFile(f)
    pprint(l)


# Hardware management --------------------------
@cli.command()
@click.option("--f", default="config.yaml", help="config file")
def read_moist_sensors(f):
    """ Read all MoistSensors from config file """
    #pdb.set_trace()
    lineitems = config.ReadFile(f)
    l = []
    for cell in lineitems:
        for sensor in cell["SoilMoist"]:
            l.append(sensor)
    pprint(l)
    return l

@cli.command()
@click.option("--f", default="config.yaml", help="config file")
@click.argument("sensor", type=int)
def add_moist_sensors(f, sensor):
    """ This is to add soil sensors """
    lineitems = config.ReadFile(f)

    chnlID = lineitems[0]["chnlID"]
    SoilMoist = lineitems[0]["SoilMoist"]
    irriTyp = lineitems[0]["irriTyp"]
    valveID = lineitems[0]["valveID"]

    # To append soil moist sensor into it
    SoilMoist.append(sensor)

    config.UpdateFile(chnlID, irriTyp, valveID, SoilMoist, f)

@cli.command()
@click.option("--f", default="config.yaml", help="config file")
@click.argument("sensor")
def remove_moist_sensors(f, sensor):
    """ This is to add soil sensors """
    lineitems = config.ReadFile(f)

    chnlID = lineitems[0]["chnlID"]
    SoilMoist = lineitems[0]["SoilMoist"]
    irriTyp = lineitems[0]["irriTyp"]
    valveID = lineitems[0]["valveID"]

    # To append soil moist sensor into it
    SoilMoist.remove(int(sensor))

    config.UpdateFile(chnlID, irriTyp, valveID, SoilMoist, f)

@cli.command()
@click.option("--f", default="config.yaml", help="config file")
def activate_all_moist_sensor(f):
    """ Read Moist sensor now """
    lineitems = config.ReadFile(f)
    l = []
    for cell in lineitems:
        for sensor in cell["SoilMoist"]:
            l.append(sensor)

    features.manual_SoilSensor(l, f)

@cli.command()
@click.option("--f", default="config.yaml", help="config file")
@click.option("--w", help="write into db, True or False")
@click.argument("sensor", type=int)
def activate_moist_sensor(f, w, sensor):
    """ Read Moist sensor now """
    lineitems = config.ReadFile(f)
    if sensor in [s for cell in lineitems for s in cell["SoilMoist"]]:
        l = features.manual_SoilSensor([sensor], f)
        print(l)
    else:
        return "such sensor doesnt exist."

    # temporary argument for test purpose.
    if w:
        dbname = join(expanduser('~'), "Projects/automated_irri/test/test_db/test.db")
        db.db_insert(dbname, "moisture_level", *l)

    return l

# Check records ------------------------
@cli.command()
@click.argument("limits")
def records(limits):
    """ Read moisture records """
    dbname = join(expanduser("~"), "Projects/automated_irri/test/test_db/test.db")
    tblnm = "moisture_level"
    tflds = [("id", "int"), ("sensor", "text"), ("datetimes", "text"), ("Moisture", "text")]
    l = db.sql_query(dbname, tblnm, tflds, limit=limits)
    pprint(l)


cli.add_command(read_config)
cli.add_command(read_moist_sensors)
cli.add_command(add_moist_sensors)
cli.add_command(remove_moist_sensors)
cli.add_command(activate_all_moist_sensor)
cli.add_command(activate_moist_sensor)
if __name__ == '__main__':
    cli()

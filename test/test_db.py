import sys
from os.path import join, expanduser
from datetime import datetime

import SetPath

p = SetPath.WhichPath("program")
sys.path.insert(0, p)

import db
import config

# --READ CONFIG DATA ----------------------------------------------
# The system will only read one fixed config file.
config_file = "test_config.yaml" # config filename

config.ReadFile(config_file)

# DB  -------------------------------
#db_name = "test_db/test.db"
table_name = "HW_reading"

# --------------------
def test_CreateTable():
    ''' test make_table '''

    db.CreateTable(config_file)

def test_db_insert1():
    """ test db_insert() with **kwargs parameters """
    kwargs = {"id": 1,
              "channel_address": 'p1',
              'datetimes': f"{datetime.now():%Y-%m-%d %H:%m}",
              'readings': 32}
    print(db.db_insert(table_name, config_file, **kwargs))

def test_db_insert2():
    """ test db_insert() with *args parameters """
    l = [{"id": 2,
        "channel_address": 'p1/n1.1',
        'datetimes': f"{datetime.now():%Y-%m-%d %H:%m}",
        'readings': 50},
        {"id": 3,
        "channel_address": 'p1/n2.1',
        'datetimes': f"{datetime.now():%Y-%m-%d %H:%m}",
        'readings': 80}]
    print(db.db_insert(table_name, config_file, *l))

def test_sql_query():
    """ test sql_query() """
    tflds = [("id", "int"),
            ("channel_address", "text"),
            ("datetimes", "text"),
            ("readings", "float")]

    expect  = [{"id": 1,
              "channel_address": 'p1',
              'datetimes': f"{datetime.now():%Y-%m-%d %H:%m}",
              'readings': 32},
             {"id": 2,
             "channel_address": 'p1/n1.1',
             'datetimes': f"{datetime.now():%Y-%m-%d %H:%m}",
             'readings': 50},
              {"id": 3,
              "channel_address": 'p1/n2.1',
              'datetimes': f"{datetime.now():%Y-%m-%d %H:%m}",
              'readings': 80}]
    actual = db.sql_query(table_name, config_file)

    assert expect == actual, "expect {} but {}".format(expect, actual)

#def test_DropTable():
#   """ test drop_table """
#    db.DropTable(table_name, config_file)
#    db.DropTable(table_name, config_file)

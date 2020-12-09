#! /usr/bin/env python
# -*- encoding=utf-8 -*-
"""
"""
from pprint import pprint
from sys import argv
import os
import sqlite3
import SetPath
import pdb

# --READ CONFIG DATA ----------------------------------------------
import config
config_file = "config.yaml" # return config directory path

# --DB commands to be executed by Python-------------------
def CreateTable(config_file=config_file):
    '''
    CreateTable(db_name, d)

    make table at the requested database.
    @arg:
        config_file: str, config filename

    @ return:
        Null if OK
        ErrorCode if error: 0 - file not found, 1 - Permission error
    '''
    # Extract db name from config file.
    cf = config.ReadFile(config_file)
    db_name = cf["db"]["name"]
    l_tbname = cf["db"]["table"]

    for row in l_tbname:
        # get table name and fields from row
        table_name = row["name"]
        fields = row["fields"]

        # create table in database
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        s = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})"
        c.execute(s)
        conn.commit()
        conn.close()

def DropTable(table_name, config_file=config_file):
    '''
    DropTable(d)

    drop table on database.
    @arg:
        table_name: str, name of the table.

    @return:
        None
    '''
    cf = config.ReadFile(config_file)

    # check if table name exist in config filename
    ltb = [ r["name"] for r in cf["db"]["table"] ]
    assert table_name in ltb, "ERROR: No such table name exist !"

    # Extract db name from config file.
    db_name = cf["db"]["name"]

    # Remove table from database.
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    s = '''DROP TABLE {}'''.format(table_name)
    c.execute(s)
    conn.commit()
    conn.close()

def db_insert(table_name, config_file=config_file, *args, **kwargs):
    """
    db_insert(db_name, table_name, *args, **kwargs)

    This is to insert the values into the requested table.

    @args:
        config_file: str, config filename.
        table_name: str, name of the table.
        *args: list, list of insert values.
        **kwargs: dictionary, dict of insert values.

    @ return: Error code is not donw !!
        Null if OK
        ErrorCode if error: 0 - file not found, 1 - Permission error
    """
    cf = config.ReadFile(config_file)

    # check if table name exist in config filename
    #print(cf)
    ltb = [ r["name"] for r in cf["db"]["table"] ]
    assert table_name in ltb, "ERROR: No such table name exist !"

    # Extract db name from config file.
    db_name = cf["db"]["name"]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # for **kwargs
    ssql1 = '''INSERT INTO {table_name}{cols} VALUES {tvals}'''
    # for *args
    ssql2 = '''INSERT INTO {table_name}{cols} VALUES ({tvals})'''

    def qt_vals(**kwargs):
        _lvals = []
        for k,v in kwargs.items():
            if isinstance(v, (int, float)):
                retval = v
            elif isinstance(v, str):
                retval = '{}'.format(v)
            _lvals.append(retval)
            cols = tuple(kwargs.keys())
        return cols, tuple(_lvals)

    table_name = table_name
    if args:
        l =[]
        for num in range(0, len(args)):
            d = args[num]
            cols, tvals = qt_vals(**d)
            l.append(tvals)
        vals = ",".join('?'*len(tvals)) # what is this ?
        sqlstr = ssql2.format(table_name=table_name, cols=cols, tvals=vals)
        #print(sqlstr)
        #print(l)
        c.executemany(sqlstr, l)
    if kwargs:
        cols, tvals = qt_vals(**kwargs)
        sqlstr = ssql1.format(table_name=table_name, cols=cols, tvals=tvals)
        #print(sqlstr)
        c.execute(sqlstr)

    conn.commit()
    conn.close()
    # curs.execute(sqlstr, tvals)
    # curs.commit()

def sql_query(table_name, config_file=config_file, limit=10, offset=0,
                orderby='', **kwargs):
    """I return a SQL str to query the table and return
        limit defined LIMMIT lauuse of SQL,
        offset defines LIMIT Clause
        ret_obj  if True, returns instances, else a tuple, for each row
        kwargs defines the WHERE clause

    e.g. SELECT ... FROM nameaddr WHERE Suname like '%lee%';

    TTD:
        as a ClassMethod, have to pass in all sort of shit,
            table_name, tflds, ...

        maybe better to instantiate a an empty obj, e.g. User0  and
        lusers = User0.sql_quert(*kwargs)

    @args:
        table_name: str, table name in db.
        config_file: str, config filename.
        limit: int, Amount of rows to be read.
        offset: int, ignore the first few row.
        orderby: str, ascending order according field
        kwargs: ??

    @returns:
        list of dicts.
    """
    cf = config.ReadFile(config_file)

    # check if table name exist in config filename ------
    ltb = [ r["name"] for r in cf["db"]["table"] ]
    assert table_name in ltb, "ERROR: No such table name exist !"

    # Setting up tflds --------------
    idx = ltb.index(table_name)
    lflds = cf["db"]["table"][idx]["fields"].split(",")
    # Bellow code clear empty space in the front string
    _lflds = [ r[1:] if r[0] == " " else r for r in lflds]
    tflds = []
    for r in _lflds:
        lft = r.split(" ")
        tflds.append((lft[0], lft[1])) # append tuple into list
    print(tflds)

    # Extract db name from config file. ---------
    db_name = cf["db"]["name"]

    # ???
    assert table_name != '' and tflds != (),\
        "**ERROR** empty table_name: {} and/or tflds {}".format(table_name, tflds)

    # filter query args to col_names, and set the formattin for types
    dflds = dict(tflds)
    ttype = ((('int', 'integer', 'number'), '{}'),
                (('text', 'varchar', 'char'), "'{}'")
                )
    _f = lambda knm, val, T=ttype: [v.format(val) for k, v
                                    in T if dflds[knm][0] in k][0]

    sql_str_select = 'SELECT * FROM {}'.format(table_name)

    # --compose the WHERE clause from kwargs--
    if kwargs:
        sql_str_where = 'WHERE {}'
        _lkwargs = []
        for k, v in kwargs.items():
            if '%' in v:
                _sw = "{} like '{}'".format(k, v)
            else:
                _sw = '{}={}'.format(k, _f(k, v))
            _lkwargs.append(_sw)
        sql_str_where = 'WHERE {}'.format(' AND '.join(_lkwargs))

    else:  # empty WHERE clause
        sql_str_where = ''

    # --Process ORDER BY, LIMIT, OFFSET clauses--
    if 'orderby' in kwargs.keys():
        orderby = kwargs.pop('orderby')

    sql_str_orderby = 'ORDER BY {}'.format(orderby) if orderby else ''
    sql_str_limit = 'LIMIT {}'.format(limit) if limit else ''
    sql_str_offset = 'OFFSET {}'.format(offset * int(limit)) if offset else ''

    # assemble the sql string
    sqlstr = '{select} {where} {orderby} {limit} {offset}'.format(
            select=sql_str_select,
            where=sql_str_where,
            orderby=sql_str_orderby,
            limit=sql_str_limit,
            offset=sql_str_offset
        )
    pprint("\n...Querying: {}\n".format(sqlstr))
    c = sqlite3.connect(db_name)
    cur = c.cursor()
    cur.execute(sqlstr)
    all_rows = cur.fetchall()

    # pack this into a dict ##
    # convert tuples to dicts and instc a list of objs.
    drows = []
    for row in all_rows:
        _d = dict([(tflds[i][0], row[i]) for i in range(len(row))])
        drows.append(_d)

    return drows

"""
This is to run main.py according crontab
"""

from crontab import CronTab
from pprint import pprint


# --READ CONFIG DATA ----------------------------------------------
import config
config_file = "config.yaml" # return config directory path


def WriTab(job, cmt=None, config_file=config_file):
    """
    WriTab(cmd)

    WriTab - write into tab table.
    @arg:
        job : str, the path to run
        set : str, crontab expressions
        cmt : str, aka comment. default as None.
                   recommended unique ID for it

    @return:
        Null if ok
    """
    # Calling config file
    cf = config.ReadFile(config_file)
    user = cf["authentication"]["user"]
    d = cf["schedule"]
    l = [d["minute"],
        d["hour"],
        d["day"],
        d["month"],
        d["week"]]

    set = " ".join(l)

    cron = CronTab(user=user)
    job = cron.new(command=job, comment=cmt)
    job.setall(set)

    cron.write()

def list():
    """
    list()

    list - list all the schedule records at crontab

    @args:
        None

    @returns:
        l, list of crontab schedule
    """
    # Calling config file
    cf = config.ReadFile(config_file)
    user = cf["authentication"]["user"]

    l = []
    for job in cron:
        l.append(job)
    return l

def delete(job, cmt=None, config_file=config_file):
    """
    remove(s, cmt)

    remove - to remove the schedule records at crontab

    @args:
        job: str, the path to run.
        cmt : str, aka comment. default as None.
    @returns:
        Null if ok.
    """
    # Calling config file
    cf = config.ReadFile(config_file)
    user = cf["authentication"]["user"]

    cron = CronTab(user=user)
    cron.remove_all(job)
    cron.remove_all(comment=cmt)

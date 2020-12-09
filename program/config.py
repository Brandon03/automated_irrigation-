"""
This is to handle config file.
"""
import os
import yaml
import pdb
import SetPath

# --READ CONFIG DATA ----------------------------------------------
# The system will only read one fixed config file.
config_file = "config.yaml" # config filename
config_path = SetPath.WhichPath("config") # config dir

# Program ----------------------------
def CreateFile(filename=config_file):
    """
    CreateFile(filename)

    Create file - config file
    @ arg:
        filename: str, filename to create

    @ return:
        Null if ok
        ErrorCode if error 0 - file exist, 1 - Permission error
    """
    os.chdir(config_path)
    if filename not in os.listdir():
        # create file
        filename = os.path.join(config_path, filename)
        with open(filename, "w") as fle:
            pass
    else:
        return "Error 0 : file exist"
    return "{} is created.".format(filename)

def WriteFile(config_content, filename=config_file):
    """
    writeFile(config_content, filename=config_file)

    Write dicts into YAML config file.
    @ arg:
        config_content: dict, config contents for config file
        filename: str, config filename

    @ return:
        Null if OK
    """
    os.chdir(config_path)
    if filename not in os.listdir():
        return "error: 0 - file not found"

    with open(filename, "w") as fle:
        data = yaml.dump(config_content, fle)

def ReadFile(filename=config_file):
    """
    ReadFile(self, chnlID, flnm='cfg_file')

    Read all line items and convert into dict. Each line item is describe by
    channel ID
    @ arg:
        flnm: str, filename

    @ return :
        return as Dict if OK
        ErrorCode if error: 0 - file is not found, 1 - Permission error
    """
    os.chdir(config_path)
    if filename not in os.listdir():
        return f"error: 0 - {config_file} not found"

    #pdb.set_trace()
    with open(filename, "r") as fle:
        l = yaml.load_all(fle)
        try:
            l = next(l) # it extracts the entire yaml
        except StopIteration:
            l = []

    return l

def DeleteFile(flename='cfg_file'):
    """
    DeleteFile(self, chnlD, flnm='cfg_file')

    Delete line item according channel id.
    @ arg:
        flnm: str, filename.
    @ return:
        Null if OK
        ErrorCode if error: 0 - file not found, 1 - Permission error
    """
    os.chdir(config_path)
    if filename not in os.listdir():
        return "error: 0 - file not found"

    os.remove(filename)

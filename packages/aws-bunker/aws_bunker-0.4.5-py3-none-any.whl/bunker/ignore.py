#!/usr/bin/env python

"""add or remove file from ignores file"""

import configparser
import os
from os.path import expanduser
import subprocess

from .common import Bcolors, query_yes_no
Bcolors = Bcolors()

def ignore(ignores, yes=None, backup=None, listall=None):
    """add or remove file from ignores"""
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    config_exists = False
    if os.path.exists(bunker_config):
        config = configparser.ConfigParser()
        config.read(bunker_config)
        config_exists = True
        prefix = config['default']['prefix']
        ignore_file = config['default']['ignored']
    else:
        print(Bcolors.PALEYELLOW+"no config file found."+Bcolors.ENDC)
        print("please run: "+Bcolors.PINK+"bunker init"+Bcolors.ENDC)
        print()
        exit()
    if listall:
        # list all
        print(Bcolors.GREY+"=== ignored files ==="+Bcolors.ENDC)
        with open(prefix+ignore_file, 'r') as fin:
            print(fin.read())
        exit()
    if not listall and not ignores:
        print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"not enough arguments"+Bcolors.ENDC)
        print()
        exit()
    # read ignore file into array
    if os.path.exists(prefix+ignore_file):
        with open(prefix+ignore_file) as f:
            ignorefile_arr = f.readlines()
        ignorefile_arr = [x.strip() for x in ignorefile_arr]
    else:
        ignorefile_arr = []
    # loop sanitized list and add and remove items ass needed
    for r in ignores:
        if r in ignorefile_arr:
            if yes or query_yes_no("remove "+Bcolors.PALEYELLOW+r+Bcolors.ENDC+" from "+Bcolors.PALEBLUE+ignore_file+"?"+Bcolors.ENDC, default="yes"):
                ignorefile_arr.remove(r)
                print(Bcolors.FAIL+r+Bcolors.ENDC)
        else:
            ignorefile_arr.append(r)
            print(Bcolors.OKGREEN+r+Bcolors.ENDC)
    # finally, backup and over-write editted array to ignore file
    if backup:
        backup_ignore = prefix+ignore_file+".bak"
        print(Bcolors.PALEBLUE+"backing up ignore file to: "+Bcolors.PALEYELLOW+backup_ignore+Bcolors.ENDC)
        bcmd = "cp "+prefix+ignore_file+" "+backup_ignore
        subprocess.call(bcmd, shell=True)
    newif = ""
    print("---")
    print(Bcolors.OKGREEN+"over-writing "+ignore_file+Bcolors.ENDC)
    for r in ignorefile_arr:
        newif += r+"\n"
    f = open(prefix+ignore_file, "w+")
    f.write(newif)
    f.close()

if __name__ == "__main__":
    ignore()

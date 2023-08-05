#!/usr/bin/env python

"""add or remove file from repos file"""

import configparser
import os
from os.path import expanduser
import subprocess

from .common import Bcolors, query_yes_no
Bcolors = Bcolors()

def repo(repos, yes=None, backup=None, listall=None):
    """add or remove file from repos"""
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    config_exists = False
    if os.path.exists(bunker_config):
        config = configparser.ConfigParser()
        config.read(bunker_config)
        config_exists = True
        prefix = config['default']['prefix']
        repo_file = config['default']['repos']
    else:
        print(Bcolors.PALEYELLOW+"no config file found."+Bcolors.ENDC)
        print("please run: "+Bcolors.PINK+"bunker init"+Bcolors.ENDC)
        print()
        exit()
    # read repo file into array
    if listall:
        # list all repos
        print(Bcolors.GREY+"=== repositories ==="+Bcolors.ENDC)
        with open(prefix+repo_file, 'r') as fin:
            print(fin.read())
        exit()
    if not listall and not repos:
        print(Bcolors.FAIL+"ERROR: "+Bcolors.WARNING+"not enough arguments"+Bcolors.ENDC)
        print()
        exit()
    if os.path.exists(prefix+repo_file):
        with open(prefix+repo_file) as f:
            repofile_arr = f.readlines()
        nrf = []
        # strip chars and remove trailing /
        for x in repofile_arr:
            x = x.strip()
            if x[-1] == "/":
                x = x[:-1]
            nrf.append(x)
        repofile_arr = nrf
    else:
        repofile_arr = []
    newr = []
    for r in repos:
        if os.path.exists(r) and os.path.isdir(r):
            if os.path.isabs(r):
                if r[-1] == "/":
                    r = r[:-1]
                newr.append(r)
            else:
                r = os.path.abspath(r)
                if r[-1] == "/":
                    r = r[:-1]
                newr.append(r)
        else:
            print(Bcolors.WARNING+r+Bcolors.ORANGE+" does not exist, or isn't a directory."+Bcolors.ENDC)
            print(Bcolors.WARNING+"ignoring "+Bcolors.CYAN+r+Bcolors.ENDC)
    # loop sanitized list and add and remove items as needed
    for r in newr:
        if r in repofile_arr:
            if yes or query_yes_no("remove "+Bcolors.PALEYELLOW+r+Bcolors.ENDC+" from "+Bcolors.PALEBLUE+repo_file+"?"+Bcolors.ENDC, default="yes"):
                repofile_arr.remove(r)
                print(Bcolors.FAIL+r+Bcolors.ENDC)
        else:
            repofile_arr.append(r)
            print(Bcolors.OKGREEN+r+Bcolors.ENDC)
    # finally, backup and over-write editted array to repo file
    if backup:
        backup_repo = prefix+repo_file+".bak"
        print(Bcolors.PALEBLUE+"backing up repo file to: "+Bcolors.PALEYELLOW+backup_repo+Bcolors.ENDC)
        bcmd = "cp "+prefix+repo_file+" "+backup_repo
        subprocess.call(bcmd, shell=True)
    newrf = ""
    print("---")
    print(Bcolors.OKGREEN+"over-writing "+repo_file+Bcolors.ENDC)
    for r in repofile_arr:
        newrf += r+"\n"
    f = open(prefix+repo_file, "w+")
    f.write(newrf)
    f.close()

            

if __name__ == "__main__":
    repo()

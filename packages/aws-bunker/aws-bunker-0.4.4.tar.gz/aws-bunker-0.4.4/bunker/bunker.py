#!/usr/bin/env python

"""bunker is a command line program for setting up an ec2 in AWS for remote development or as a backup. It can clone your git repos, and transfer ignored files from your machine to the ec2."""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
import signal
import time
import os
from os.path import expanduser
from datetime import datetime
from pathlib import Path
import pkg_resources

from .init import init_bunker
from .install import install
from .prompt import prompt
from .buildbunker import buildbunker
from .repo import repo
from .ignore import ignore
from .common import Bcolors

def signal_handler(sig, frame):
    """handle control c"""
    print(Bcolors.WARNING+"\nExit with "+Bcolors.FAIL+"Control C\n"+Bcolors.ENDC)
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

Bcolors=Bcolors()

def bunker():
    """bunker is a command line program for setting up an ec2 in AWS for remote development or as a backup. It can clone your git repos, and transfer ignored files from your machine to the ec2."""
    version = pkg_resources.require("aws-bunker")[0].version
    parser = argparse.ArgumentParser(
        description='bunker is a command line program for setting up an ec2 in AWS for remote development or as a backup. It can clone your git repos, and transfer ignored files from your machine to the ec2.',
        prog='bunker',
        formatter_class=rawtxt
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    
    subparsers = parser.add_subparsers(title='subcommands', required=True, dest="subcommand", help="""for more info: type `bunker subcommand -h`

the """+Bcolors.PINK+"""install"""+Bcolors.ENDC+""", """+Bcolors.PINK+"""extra """+Bcolors.ENDC+"""and """+Bcolors.PINK+"""prompt """+Bcolors.ENDC+"""subcommands require custom bash scripts to exist on your EC2. The scripts also need to be executable.
for example scripts please visit the project homepage:
"""+Bcolors.GOLD+"""https://gitlab.com/shindagger/bunker **"""+Bcolors.ENDC)
    #parser.print_help()
    
    parser_init = subparsers.add_parser('init', formatter_class=argparse.RawTextHelpFormatter, help='init bunker by writing ~/.config-bunker', description="init bunker by writing ~/.config-bunker")
    parser_init.set_defaults(func=init_bunker)
    parser_install = subparsers.add_parser('install', formatter_class=argparse.RawTextHelpFormatter, help="""install essential software
"""+Bcolors.GOLD+"""default: `install-essentials.sh`"""+Bcolors.ENDC, description="""install essential software
default: """+Bcolors.GOLD+"""`install-essentials.sh`"""+Bcolors.ENDC+""" on the EC2.
if the file is not executable use the """+Bcolors.OKGREEN+"""[-e]"""+Bcolors.ENDC+""" flag.
for example files please visit: """+Bcolors.PALEBLUE+"""https://gitlab.com/shindagger/bunker"""+Bcolors.ENDC)
    parser_install.add_argument('-y', '--yes', action='store_true', help='auto approve installing essentials.')
    parser_install.add_argument('-s', action='store_true', help='startup EC2 first.')
    parser_install.add_argument('run', nargs='?', default='/home/ubuntu/install-essentials.sh', help='run provided shell script. please use absolute paths. default: '+Bcolors.PALEBLUE+'`/home/ubuntu/install-essentials.sh`'+Bcolors.ENDC)
    parser_install.add_argument('-e', action='store_true', help='make shell script executable first.')
    parser_install.add_argument('-b', '--bucket', nargs=3, metavar=('BUCKET','REGION','PREFIX'), default=['none', 'none', 'none'], help='save standard out to an s3 bucket (for trouble-shooting). takes 3 arguments: '+Bcolors.PALEBLUE+'bucket, region, and prefix'+Bcolors.ENDC+'\nexample: '+Bcolors.PALEYELLOW+'bunker install /home/ubuntu/script.sh -b bucketname us-east-1 ssm-test'+Bcolors.ENDC)
    parser_install.set_defaults(func=install)
    parser_prompt = subparsers.add_parser('prompt', formatter_class=argparse.RawTextHelpFormatter, help="""source file in /home/ubuntu/.profile
"""+Bcolors.GOLD+"""default: `/home/ubuntu/.prompt.sh`"""+Bcolors.ENDC, description="""source file in /home/ubuntu/.profile
default: """+Bcolors.GOLD+"""`/home/ubuntu/.prompt.sh`"""+Bcolors.ENDC+"""
for an example file please visit: """+Bcolors.PALEBLUE+"""https://gitlab.com/shindagger/bunker"""+Bcolors.ENDC)
    parser_prompt.add_argument('file', nargs='?', default='/home/ubuntu/.prompt.sh', help='source provided file. please use absolute paths. default: '+Bcolors.PALEBLUE+'`/home/ubuntu/.prompt.sh`'+Bcolors.ENDC)
    parser_prompt.add_argument('-y', '--yes', action='store_true', help='auto approve customizing bash prompt.')
    parser_prompt.add_argument('-b', '--bucket', nargs=3, metavar=('BUCKET','REGION','PREFIX'), default=['none', 'none', 'none'], help='save standard out to an s3 bucket (for trouble-shooting). takes 3 arguments: '+Bcolors.PALEBLUE+'bucket, region, and prefix'+Bcolors.ENDC+'\nexample: '+Bcolors.PALEYELLOW+'bunker prompt /home/ubuntu/custom-bash-prompt.sh -b bucketname us-east-1 ssm-test'+Bcolors.ENDC)
    parser_prompt.add_argument('-s', action='store_true', help='startup EC2 first.')
    parser_prompt.set_defaults(func=prompt)
    parser_repo = subparsers.add_parser('repo', aliases=['r'], formatter_class=argparse.RawTextHelpFormatter, help="""add or remove repos to/from the repo file.
if the repo is in the file it will remove the repo.
if the repo is not in the file, it will be added.
"""+Bcolors.PALEBLUE+"""both relative and absolute paths will work."""+Bcolors.ENDC, description="""add or remove repos to/from the repo file.
if the repo is in the file it will be removed.
if the repo is not in the file, it will be added.
"""+Bcolors.PALEBLUE+"""both relative and absolute paths will work."""+Bcolors.ENDC)
    parser_repo.add_argument('repos', nargs='*', help='a list of repos to add or remove to/from the repo file. requires at least one repo.')
    parser_repo.add_argument('-y', '--yes', action='store_true', help='approve all prompts as yes.')
    parser_repo.add_argument('-b', '--backup', action='store_true', help='backup repo file before over-writing.')
    parser_repo.add_argument('-l', '--list', action='store_true', help='list current repo file.')
    parser_repo.set_defaults(func=repo)
    parser_ignore = subparsers.add_parser('ignore', formatter_class=argparse.RawTextHelpFormatter, help="""add or remove filenames to/from the ignore file.
if the filename is in the ignore file it will be removed.
if the filename is not in the ignore file, it will be added.""", description="""add or remove filename to/from the ignore file.
if the filename is in the ignore file it will be removed.
if the filename is not in the ignore file, it will be added.""")
    parser_ignore.add_argument('ignores', aliases=['i'], nargs='*', help='a list of filenames to add or remove to/from the ignore file. requires at least one file to ignore.')
    parser_ignore.add_argument('-y', '--yes', action='store_true', help='approve all prompts as yes.')
    parser_ignore.add_argument('-b', '--backup', action='store_true', help='backup ignore file before over-writing.')
    parser_ignore.add_argument('-l', '--list', action='store_true', help='list current ignore file.')
    parser_ignore.set_defaults(func=ignore)
    parser_build = subparsers.add_parser('build', help='clone git repos and copy over ignored files', description="clone git repos and copy over ignored files")
    parser_build.add_argument('-y', '--yes', action='store_true', help='auto approve cloning repos and backing up files.')
    parser_build.add_argument('-S', action='store_true', help='stop EC2 after running.')
    parser_build.add_argument('-s', action='store_true', help='startup EC2 first.')
    parser_build.add_argument('-r', '--repo', nargs='?', default=None, help='Source directory to be duplicated to remote bunker')
    parser_build.set_defaults(func=buildbunker)
    args = parser.parse_args()
    # error checking
    if args.subcommand != 'init':
        home = expanduser('~')
        bunker_config = os.path.join(home, ".config-bunker.ini")
        if not os.path.isfile(bunker_config):
            print(Bcolors.WARNING+"no configuration file exists at: "+Bcolors.ORANGE+bunker_config+Bcolors.ENDC)
            print("please run:")
            print()
            print(Bcolors.PINK+"   bunker init"+Bcolors.ENDC)
            print()
            time.sleep(1)
            print(Bcolors.GREY+"... bunker --help ..."+Bcolors.ENDC)
            time.sleep(1)
            parser.print_help()
            exit()
    # auf gehts
    if args.subcommand == 'build':
        yes = args.yes
        running = args.S
        dostart = args.s
        source = args.repo
        args.func(running, dostart, source, yes)
    elif args.subcommand == 'install':
        yes = args.yes
        dostart = args.s
        run = args.run
        execute = args.e
        bucket_info = args.bucket
        args.func(dostart=dostart, yes=yes, run=run, execute=execute, bucket_info=bucket_info)
    elif args.subcommand == 'prompt':
        yes = args.yes
        dostart = args.s
        run = args.file
        bucket_info = args.bucket
        args.func(dostart=dostart, yes=yes, run=run, bucket_info=bucket_info)
    elif args.subcommand == 'repo':
        yes = args.yes
        repos = args.repos
        backup = args.backup
        listall = args.list
        args.func(repos, yes, backup, listall)
    elif args.subcommand == 'ignore':
        yes = args.yes
        ignores = args.ignores
        backup = args.backup
        listall = args.list
        args.func(ignores, yes, backup, listall)
    else:
        args.func()

if __name__ == "__main__":
    bunker()

import sys
import time
import paramiko
from tqdm import tqdm

""" common functions """

def tqdmWrapViewBar(*args, **kwargs):
    pbar = tqdm(*args, **kwargs)  # make a progressbar
    last = [0]  # last known iteration, start at 0
    def viewBar2(a, b):
        pbar.total = int(b)
        pbar.update(int(a - last[0]))  # update pbar with increment
        last[0] = a  # update last known iteration
    return viewBar2, pbar  # return callback, tqdmInstance

def sftp_mkdir_p(sftp, remote_directory):
    dirs_exist = remote_directory.split('/')
    dirs_make = []
    # find level where dir doesn't exist
    while len(dirs_exist) > 0:
        try:
            sftp.listdir('/'.join(dirs_exist))
            break
        except IOError:
            value = dirs_exist.pop()
            if value == '':
                continue
            dirs_make.append(value)
        else:
            return False
    # ...and create dirs starting from that level
    for mdir in dirs_make[::-1]:
        dirs_exist.append(mdir)
        sftp.mkdir('/'.join(dirs_exist))

def progbar(ip_address, username, pem, source, destination, permissions=None):
    """upload a file to ec2 and display a progress bar."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip_address, username=username, key_filename=pem)
    sftp = client.open_sftp()
    cbk, pbar = tqdmWrapViewBar(ascii=False, unit='b', unit_scale=True)
    dest_arr = destination.split("/")
    dest_wo_file = ""
    x = 1
    for part in dest_arr:
        if x != len(dest_arr):
            dest_wo_file += part+"/"
        x += 1
    sftp_mkdir_p(sftp, dest_wo_file)
    sftp.put(source,destination,callback=cbk)
    if permissions is not None:
        sftp.chmod(destination, permissions)
    pbar.close()
    client.close()

#progbar("54.91.190.120", "ubuntu", "/Users/neolaura/shindagger.pem", "/Users/neolaura/cubed-api/portalbearing/1.jpg", "/home/ubuntu/1.jpg")
def query_yes_no(question, default="yes"):
    '''confirm or decline'''
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '': 
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("\nPlease respond with 'yes' or 'no' (or 'y' or 'n').\n")

def countdown(num):
    while num > 0:
        fmtnum = str(num)
        if num < 10: 
            fmtnum = "0"+str(num)
        print(fmtnum, end="\r", flush=True)
        num -= 1
        time.sleep(1)
    return

class Bcolors:
    """console colors"""
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;212m'
    PALEYELLOW = '\033[38;5;228m'
    PALEBLUE = '\033[38;5;111m'
    GOLD = '\033[38;5;178m'

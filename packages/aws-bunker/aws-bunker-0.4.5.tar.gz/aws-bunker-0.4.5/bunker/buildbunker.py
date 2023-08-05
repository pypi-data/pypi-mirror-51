#!/usr/bin/env python

"""buildbunker uses boto3/ssm to clone all your git repos and then rsync up dot files and configs"""

import configparser
import os
from os.path import expanduser
import time
import subprocess
import boto3

from .common import Bcolors, query_yes_no, countdown, progbar
Bcolors = Bcolors()

def buildbunker(running=None, dostart=None, source=None, yes=None):
    """clone git repos on ec2, then copy over ignored files"""
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    config = configparser.ConfigParser()
    config.read(bunker_config)
    prefix = config['default']['prefix']
    repos = prefix+config['default']['repos']
    ignored = prefix+config['default']['ignored']
    pem = config['default']['pem']
    instance_id = config['default']['instance_id']
    username = config['default']['username']
    gitkeys = config['default']['gitkeys']
    gitkeys_arr = []
    keycount = gitkeys.count(', ')
    if keycount > 0:
        gitkeys_arr = config['default']['gitkeys'].split(", ")
    else:
        gitkeys_arr.append(config['default']['gitkeys'])
    # ec2 ssm client
    client = boto3.client('ec2')
    ssm_client = boto3.client('ssm')
    # start up if necessary
    if dostart:
        print(Bcolors.ENDC+"starting ec2 and waiting for \"running\" state...")
        client.start_instances(InstanceIds=[instance_id])
        waiter = client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        countdown(20)
        print("instance up: "+str(instance_id))
    # get ip address
    instance_ip = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text", shell=True, stdout=subprocess.PIPE)
    instance_ip = instance_ip.stdout.decode('utf-8')
    instance_ip = instance_ip.strip(' \t\n\r')
    # get instance state
    state = 0
    state = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].State.Code' --output text", shell=True, stdout=subprocess.PIPE)
    state = state.stdout.decode('utf-8')
    try:
        state = int(state)
    except ValueError:
        print(Bcolors.RED+"instance does not seem to exist..."+Bcolors.ENDC)
        print("ensure everything is set correctly by running: "+Bcolors.PINK+"bunker init"+Bcolors.ENDC)
        print()
        exit()
    state = int(state)
    if state != 16:
        print(Bcolors.RED+"instance is not running."+Bcolors.ENDC)
        if not running:
            stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
        exit()
    # INSTANCE READY FOR WORK, DO STUFF
    #
    # auf gehts
    dirs = []
    diffs = []
    similarities = []
    if not os.path.isfile(repos) or os.stat(repos).st_size == 0:
        print(Bcolors.WARNING+"WARNING: "+Bcolors.GOLD+"you do not currently have any repos configured."+Bcolors.ENDC)
        print("it is recommended that you add a few repos to your repo file so bunker can determine a base path.")
        print("bunker removes this base path when it clones your repos on the EC2.")
        print("to add a repo to the repo file: "+Bcolors.PINK+"bunker repo path/to/repo"+Bcolors.ENDC)
        print(Bcolors.PALEBLUE+"NOTE: both relative and absolute paths will work."+Bcolors.ENDC)
    else:
        with open(repos, 'r') as f:
            x = 0
            for line in f:
                repo = line.strip()
                if len(repo) > 0:
                    if repo[-1] == "/":
                        repo = repo[:-1]
                    dirs.append(repo)
                    exploded_repo = repo.split("/")
                    for directory in exploded_repo:
                        if x == 0 and directory != "":
                            diffs.append(directory)
                        else:
                            if directory in diffs and directory not in similarities:
                                similarities.append(directory)
                x += 1
    if yes or query_yes_no("ready to transfer to "+instance_ip+"?", "yes"):
        addrepo = False
        if source:
            if not os.path.isdir(source):
                print(Bcolors.WARNING+"please use a valid directory"+Bcolors.ENDC)
                exit()
            if not os.path.isabs(source):
                source = os.path.abspath(source)
            if source[-1] == "/":
                source = source[:-1]
            if source not in dirs:
                addrepo = True
            dirs = []
            dirs.append(source)

        # check for known_hosts
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['ls /home/'+username+'/.ssh/known_hosts']}, )
        check_id = response['Command']['CommandId']
        time.sleep(1)
        checkoutput = ssm_client.get_command_invocation(
            CommandId=check_id,
            InstanceId=instance_id,
        )   
        while checkoutput['Status'] != "Success" and checkoutput['Status'] != "Failed":
            time.sleep(1)
            checkoutput = ssm_client.get_command_invocation(
                CommandId=check_id,
                InstanceId=instance_id,
            )   
        if checkoutput['Status'] != "Success":
            print(Bcolors.WARNING+"no "+Bcolors.ORANGE+"known_hosts"+Bcolors.WARNING+" in /home/"+username+"/.ssh/"+Bcolors.ENDC)
            print("copy local known_hosts to EC2")
            if os.path.isfile(os.path.join(home, ".ssh", "known_hosts")):
                known_hosts = os.path.join(home, ".ssh", "known_hosts")
                #cmd = "scp -i "+pem+" "+known_hosts+" "+username+"@"+instance_ip+":/home/"+username+"/.ssh/"
                print("copy "+Bcolors.ORANGE+"~/.ssh/knownhosts"+Bcolors.ENDC+" to "+Bcolors.CYAN+instance_ip+Bcolors.ENDC)
                dest = "/home/"+username+"/.ssh/known_hosts"
                progbar(instance_ip, username, pem, known_hosts, dest, 0o644)
                #subprocess.call(cmd, shell=True)
            else:
                print(Bcolors.WARNING+"no known_hosts in ~/.ssh/"+Bcolors.ENDC)
                print("please configure your local ssh to connect to your git providers before using bunker.")
                print()
                exit()

        # check for config
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['ls /home/'+username+'/.ssh/config']}, )
        check_id = response['Command']['CommandId']
        time.sleep(1)
        checkoutput = ssm_client.get_command_invocation(
            CommandId=check_id,
            InstanceId=instance_id,
        )
        while checkoutput['Status'] != "Success" and checkoutput['Status'] != "Failed":
            time.sleep(1)
            checkoutput = ssm_client.get_command_invocation(
                CommandId=check_id,
                InstanceId=instance_id,
            )
        if checkoutput['Status'] != "Success":
            print(Bcolors.WARNING+"no "+Bcolors.ORANGE+"config"+Bcolors.WARNING+" in /home/"+username+"/.ssh/"+Bcolors.ENDC)
            print("copy local config to EC2")
            if os.path.isfile(os.path.join(home, ".ssh", "config")):
                sshconfig = os.path.join(home, ".ssh", "config")
                #cmd = "scp -i "+pem+" "+sshconfig+" "+username+"@"+instance_ip+":/home/"+username+"/.ssh/"
                print("copy "+Bcolors.ORANGE+"~/.ssh/config"+Bcolors.ENDC+" to "+Bcolors.CYAN+instance_ip+Bcolors.ENDC)
                dest = "/home/"+username+"/.ssh/config"
                progbar(instance_ip, username, pem, sshconfig, dest, 0o644)
                #subprocess.call(cmd, shell=True)
            else:
                print(Bcolors.WARNING+"no config in ~/.ssh/"+Bcolors.ENDC)
                print("please configure your local ssh to connect to your git providers before using bunker.")
                print()
                exit()

        # check for .ssh/keys
        if gitkeys_arr[0] != "":
            for keyfile in gitkeys_arr:
                exploded = keyfile.split("/")
                kf = exploded[-1]
                response = ssm_client.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': ['ls /home/'+username+'/.ssh/'+kf]}, )
                check_id = response['Command']['CommandId']
                time.sleep(1)
                checkoutput = ssm_client.get_command_invocation(
                    CommandId=check_id,
                    InstanceId=instance_id,
                )
                while checkoutput['Status'] != "Success" and checkoutput['Status'] != "Failed":
                    time.sleep(1)
                    checkoutput = ssm_client.get_command_invocation(
                        CommandId=check_id,
                        InstanceId=instance_id,
                    )
                if checkoutput['Status'] != "Success":
                    print(Bcolors.WARNING+"no "+Bcolors.ORANGE+kf+Bcolors.WARNING+" in /home/"+username+"/.ssh/"+Bcolors.ENDC)
                    print("copy local "+kf+" to EC2")
                    #cmd = "scp -i "+pem+" "+keyfile+" "+username+"@"+instance_ip+":/home/"+username+"/.ssh/"
                    print("copy "+Bcolors.ORANGE+"~/.ssh/"+kf+Bcolors.ENDC+" to "+Bcolors.CYAN+instance_ip+Bcolors.ENDC)
                    dest = "/home/"+username+"/.ssh/"+kf
                    progbar(instance_ip, username, pem, keyfile, dest, 0o600)
                    #subprocess.call(cmd, shell=True)

        # declare outputs dict
        outputs = {}
        for d in dirs:
            # loop thru repos (d), check if repo dir exists, then attempt to clone
            gitconfig = d+"/.git/config"
            catcher = False
            # getting repo url from .git/config
            with open(gitconfig, 'r') as gconfig:
                for line in gconfig:
                    if catcher:
                        repourl = line
                        break
                    if "[remote \"origin\"]" in line:
                        catcher = True
            repourl = repourl.strip(' \t\n\r')
            repoarr = repourl.split(" = ")
            repourl = repoarr[1]
            if "https://" in  repourl:
                repourl_arr = repourl.split("/")
                newrepourl = ""
                repo_trigger = False
                for part in repourl_arr:
                    if repo_trigger or ".com" in part or ".org" in part:
                        if "@" in part:
                            exp = part.split("@")
                            part = exp[1]
                        if ".com" in part or ".org" in part:
                            newrepourl += part+":"
                        else:
                            newrepourl += part+"/"
                        repo_trigger = True
                repourl = "git@"+newrepourl[:-1]

            exploded_d = d.split("/")
            newd = ""
            for thing in exploded_d:
                if thing not in similarities:
                    newd += thing+"/"
            if newd[0] != "/":
                newd = "/"+newd
            displayd = newd[1:]
            displayd_ex = displayd.split("/")
            displayd = displayd_ex[0]
            # asdf
            response = ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': ['ls /home/'+username+newd]}, )
            check_id = response['Command']['CommandId']
            # wait for response
            time.sleep(1)
            checkoutput = ssm_client.get_command_invocation(
                CommandId=check_id,
                InstanceId=instance_id,
            )
            while checkoutput['Status'] != "Success" and checkoutput['Status'] != "Failed":
                time.sleep(1)
                checkoutput = ssm_client.get_command_invocation(
                    CommandId=check_id,
                    InstanceId=instance_id,
                )
            if checkoutput['Status'] != "Success":
                response = ssm_client.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunShellScript",
                    Parameters={'commands': ['sudo -u '+username+' git clone '+repourl+' /home/'+username+newd, 'chown -R '+username+':'+username+' /home/'+username+newd]}, )
                command_id = response['Command']['CommandId']
                outputs[command_id] = 'sudo -u '+username+' git clone '+repourl+' /home/'+username+newd, 'chown -R '+username+':'+username+' /home/'+username+newd
                print(Bcolors.YELLOW+"cloning repo: "+d+Bcolors.ENDC)
                time.sleep(1)
            else:
                print(Bcolors.OKGREEN+"repo exists: "+displayd+Bcolors.ENDC)
        if len(dirs) < 5:
            print(Bcolors.PALEYELLOW+"waiting for clone."+Bcolors.ENDC)
            countdown(10)
        # loop thru output and print any errors
        for key, value in outputs.items():
            cmdoutput = ssm_client.get_command_invocation(
                CommandId=key,
                InstanceId=instance_id,
            )
            if cmdoutput['Status'] != "Success":
                print(Bcolors.RED+"Warning - "+Bcolors.YELLOW+str(value)+Bcolors.ENDC)
                print(Bcolors.RED+"Command output ===\n"+Bcolors.YELLOW+cmdoutput['StandardErrorContent']+Bcolors.ENDC)
                print(Bcolors.RED+'===\nCloning Repo: '+cmdoutput['Status']+". "+Bcolors.YELLOW+"We will still attemp to rsync files"+Bcolors.ENDC)
        #
        #
        # backup hidden files and configs below
        #
        #
        print("cleaning up...")
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['chown -R '+username+':'+username+' /home/'+username]}, )
        command_id = response['Command']['CommandId']
        time.sleep(1)
        files = []
        with open(ignored, 'r') as f:
            for line in f:
                ignore = line.strip()
                files.append(ignore)
        print(Bcolors.PALEYELLOW+"copying over ignored files"+Bcolors.ENDC)
        for d in dirs:
            os.chdir(d)
            exploded_d = d.split("/")
            newd = ""
            for thing in exploded_d:
                if thing not in similarities:
                    newd += thing+"/"
            if newd[0] != "/":
                newd = "/"+newd
            displayd = newd[1:]
            displayd_ex = displayd.split("/")
            displayd = displayd_ex[0]
            print(Bcolors.BOLD+Bcolors.OKGREEN+"== "+displayd+" =="+Bcolors.ENDC)
            for i in files:
                exists = subprocess.run("find . -name '"+i+"'", shell=True, stdout=subprocess.PIPE)
                exists = exists.stdout.decode('utf-8')
                if len(exists) > 1:
                    print(Bcolors.BOLD+Bcolors.YELLOW+i+Bcolors.ENDC)
                    output = subprocess.check_output("find . -name \""+i+"\"", shell=True)
                    output = output.decode('utf-8')
                    output_arr = output.split("\n")
                    z = 1
                    for p in output_arr:
                        if z != len(output_arr):
                            abs_f = os.path.abspath(p)
                            mode = oct(os.stat(abs_f).st_mode & 0o777)
                            mode = int(mode, 8)
                            exploded_d = abs_f.split("/")
                            wo_sims = ""
                            for thing in exploded_d:
                                if thing not in similarities:
                                    wo_sims += thing+"/"
                            wo_sims = wo_sims[1:]
                            wo_sims = wo_sims[:-1]
                            print(Bcolors.PINK+wo_sims+Bcolors.ENDC)
                            dest = "/home/"+username+"/"+wo_sims
                            progbar(instance_ip, username, pem, abs_f, dest, mode)
                        z += 1
        if addrepo:
            if query_yes_no("would you like to add "+Bcolors.GOLD+dirs[0]+Bcolors.ENDC+" to your repos file?", "yes"): 
                with open(repos, "a") as myfile:
                    myfile.write(dirs[0]+"\n")
    else:
        if running:
            stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
            print("\nshutting down")
        else:
            print("\nleaving ec2 running")
        exit()
    
    if running:
        stop = subprocess.run("aws ec2 stop-instances --instance-ids "+instance_id, shell=True, stdout=subprocess.PIPE)
        print(Bcolors.CYAN+"\nshutting down: "+instance_ip+Bcolors.ENDC)
    else:
        print(Bcolors.CYAN+"\nleaving "+instance_ip+" running"+Bcolors.ENDC)
    return

if __name__ == "__main__":
    buildbunker()

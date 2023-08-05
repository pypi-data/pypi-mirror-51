#!/usr/bin/env python

"""install essentials"""

import configparser
import os
from os.path import expanduser
import json
import time
import subprocess
import boto3

from .common import Bcolors, query_yes_no, countdown
Bcolors = Bcolors()

def install(instance_id=None, dostart=None, yes=None, run=None, execute=None, bucket_info=None):
    #config here
    home = expanduser('~')
    bunker_config = os.path.join(home, ".config-bunker.ini")
    config = configparser.ConfigParser()
    config.read(bunker_config)

    prefix = config['default']['prefix']
    pem = prefix+config['default']['pem']
    if instance_id is None:
        instance_id = config['default']['instance_id']
    username = config['default']['username']
    client = boto3.client('ec2')
    ssm_client = boto3.client('ssm')
    if dostart:
        print(Bcolors.ENDC+"starting ec2 and waiting for "+Bcolors.OKGREEN+"\"running\""+Bcolors.ENDC+" state...")
        client.start_instances(InstanceIds=[instance_id])
        waiter = client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        countdown(20)
        print("instance up: "+str(instance_id))
    instance_ip = subprocess.run("aws ec2 describe-instances --instance-ids "+instance_id+" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text", shell=True, stdout=subprocess.PIPE)
    instance_ip = instance_ip.stdout.decode('utf-8')
    instance_ip = instance_ip.strip(' \t\n\r')
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
    if state != 16:
        print(Bcolors.RED+"instance is not running."+Bcolors.ENDC)
        print("did you mean?: "+Bcolors.PINK+"   bunker install -s"+Bcolors.ENDC)
        print()
        exit()
    if run is None:
        print("no script!")
        exit()
    else:
        if not os.path.isabs(run):
            print(Bcolors.PALEYELLOW+"Please use absolute paths to the location of the script on the EC2"+Bcolors.ENDC)
            print("example: "+Bcolors.PALEBLUE+"/home/ubuntu/install-essentials.sh"+Bcolors.ENDC)
            exit()
    # INSTANCE READY FOR WORK, DO STUFF
    if yes or query_yes_no("run script on: "+instance_ip+"?", "yes"):
        run_exploded = run.split("/")
        rel_run = run_exploded[-1]
        if execute:
            # making file executable
            cmd = "aws ssm send-command --instance-ids \""+instance_id+"\" --document-name \"AWS-RunShellScript\" --parameters commands=\"chmod a+x "+run+"\""
            ran_command = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            ran_command = json.loads(ran_command)
            command_id = ran_command["Command"]["CommandId"]
            install_status = "InProgress"
            start_time = time.time()
            print(Bcolors.GOLD+bytes.decode(b'\xE2\x8F\xB3', 'utf8')+" chmod a+x "+rel_run+Bcolors.ENDC)
            while install_status == "InProgress":
                elapsed_time = time.time() - start_time
                elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                elapsed_time = str(elapsed_time)
                cmd = "aws ssm list-command-invocations --command-id \""+command_id+"\" --details" 
                ran_command = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                ran_command = json.loads(ran_command)
                install_status = ran_command["CommandInvocations"][0]["Status"]
                if install_status == "InProgress":
                    print(Bcolors.WARNING+install_status+Bcolors.GREY+" Time Elapsed: "+Bcolors.ENDC+elapsed_time+"     ", end="\r")
                else:
                    if install_status != "Success":
                        color = Bcolors.FAIL
                    else:
                        color = Bcolors.OKGREEN
                    print(color+install_status+Bcolors.GREY+" Time Elapsed: "+Bcolors.ENDC+elapsed_time+"     ")


            cmdoutput = ssm_client.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id,
            )
            if cmdoutput['Status'] != "Success":
                time.sleep(1)
                print(Bcolors.GOLD+"running chmod a+x "+rel_run+" returned the following "+Bcolors.FAIL+"error:\n"+Bcolors.WARNING+cmdoutput['StandardErrorContent']+Bcolors.ENDC)
        # RUN SCRIPT
        print(Bcolors.GOLD+bytes.decode(b'\xE2\x8F\xB3', 'utf8')+" running "+rel_run+Bcolors.ENDC)
        # aws ssm send-command --instance-ids "instance ID" --document-name "AWS-RunShellScript" --comment "IP config" --parameters commands=ifconfig --output text
        if bucket_info != ['none', 'none', 'none'] and bucket_info is not None:
            print(Bcolors.CYAN+"will save output to: "+Bcolors.GOLD+bucket_info[0]+Bcolors.ENDC)
            cmd = "aws ssm send-command --instance-ids \""+instance_id+"\" --document-name \"AWS-RunShellScript\" --output-s3-bucket-name \""+bucket_info[0]+"\" --output-s3-region \""+bucket_info[1]+"\" --output-s3-key-prefix \""+bucket_info[2]+"\" --parameters commands=\""+run+"\""
        else:
            cmd = "aws ssm send-command --instance-ids \""+instance_id+"\" --document-name \"AWS-RunShellScript\" --parameters commands=\""+run+"\""
        ran_command = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        ran_command = json.loads(ran_command)
        command_id = ran_command["Command"]["CommandId"]
        install_status = "InProgress"
        start_time = time.time()
        while install_status == "InProgress":
            elapsed_time = time.time() - start_time
            elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            elapsed_time = str(elapsed_time)
            cmd = "aws ssm list-command-invocations --command-id \""+command_id+"\" --details" 
            ran_command = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            ran_command = json.loads(ran_command)
            install_status = ran_command["CommandInvocations"][0]["Status"]
            if install_status == "InProgress":
                print(Bcolors.WARNING+install_status+Bcolors.GREY+" Time Elapsed: "+Bcolors.ENDC+elapsed_time+"     ", end="\r")
            else:
                if install_status != "Success":
                    color = Bcolors.FAIL
                else:
                    color = Bcolors.OKGREEN
                print(color+install_status+Bcolors.GREY+" Time Elapsed: "+Bcolors.ENDC+elapsed_time+"     ")


        cmdoutput = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )   
        if cmdoutput['Status'] != "Success":
            print(Bcolors.GOLD+"running "+rel_run+" returned the following "+Bcolors.FAIL+"error:\n"+Bcolors.WARNING+cmdoutput['StandardErrorContent']+Bcolors.ENDC)


    complete = "complete"
    return complete

if __name__ == "__main__":
    install()

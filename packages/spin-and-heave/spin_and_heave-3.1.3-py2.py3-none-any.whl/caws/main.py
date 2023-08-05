#!/usr/bin/env python

"""configure AWS responsibly using profile names."""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
import signal
import os
from os.path import expanduser
import shutil
import json
import subprocess
from datetime import datetime
from pathlib import Path
import pkg_resources

def signal_handler(sig, frame):
    """handle control c"""
    print('\nuser cancelled')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

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

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None

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
    ORANGE = '\033[38;5;208m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PINK = '\033[35m'
    PALEYELLOW = '\033[38;5;228m'
    PALEBLUE = '\033[38;5;111m'

def rewrite_creds(creds, awsconfig, profile):
    """rewrite aws creds and config"""
    f = open(creds, "r")
    oldcreds = []
    defaultp = []
    profilep = []
    default_counter = 0
    profile_counter = 0
    for line in f:
        if "[default]" in line or default_counter > 0:
            if default_counter < 3:
                defaultp.append(line)
            default_counter+=1
        if "["+profile+"]" in line or profile_counter > 0:
            if profile_counter < 3:
                profilep.append(line)
            profile_counter+=1
        oldcreds.append(line)
    #print(Bcolors.ORANGE+"oldcreds:"+Bcolors.ENDC, oldcreds)
    #print(Bcolors.ORANGE+"default:"+Bcolors.ENDC, defaultp)
    #print(Bcolors.ORANGE+"profile:"+Bcolors.ENDC, profilep)
    f = open(awsconfig, "r")
    oldconfig = []
    defaultc = []
    profilec = []
    cdefault_counter = 0
    cprofile_counter = 0
    for line in f:
        if "[default]" in line or cdefault_counter > 0:
            if cdefault_counter < 3:
                defaultc.append(line)
            cdefault_counter+=1
        if "[profile "+profile+"]" in line or cprofile_counter > 0:
            if cprofile_counter < 3:
                profilec.append(line)
            cprofile_counter+=1
        oldconfig.append(line)
    #print(Bcolors.ORANGE+"oldconfig:"+Bcolors.ENDC, oldconfig)
    #print(Bcolors.ORANGE+"default:"+Bcolors.ENDC, defaultc)
    #print(Bcolors.ORANGE+"profile:"+Bcolors.ENDC, profilec)
    w = 0
    backup_creds = creds+".caws.bak"
    print(Bcolors.PALEBLUE+"backing up credentials to: "+Bcolors.PALEYELLOW+backup_creds+Bcolors.ENDC)
    backup_config = awsconfig+".caws.bak"
    print(Bcolors.PALEBLUE+"backing up config to: "+Bcolors.PALEYELLOW+backup_config+Bcolors.ENDC)
    bcmd = "cp "+creds+" "+backup_creds
    subprocess.call(bcmd, shell=True)
    bcmd = "cp "+awsconfig+" "+backup_config
    # yikes!!!
    os.remove(creds)
    os.remove(awsconfig)
    with open(creds, 'a') as the_file:
        for line in oldcreds:
            if w == 1 or w == 2:
                the_file.write(profilep[w])
            else:
                the_file.write(line)
            w+=1
    # new config
    newconfig = "[default]\n"
    w = 0
    for line in profilec:
        if w > 0:
            newconfig += line
        w += 1
    newconfig += "\n"
    write = False
    for line in oldconfig:
        if "[profile " in line:
            write = True
        if write is True:
            newconfig += line
    with open(awsconfig, 'a') as the_file: 
        the_file.write(newconfig)
    return

def main():
    '''configure AWS responsibly using profile names and environment vars.'''
    version = pkg_resources.require("caws")[0].version
    parser = argparse.ArgumentParser(
        description="""configure AWS responsibly using profile names and environment vars.
`caws` will write to an RC file setting AWS_DEFAULT_PROFILE to the profile name.
if you do not have the rc file `caws` will create it for you.
"""+Bcolors.PINK+"""you'll need to add `. .cawsrc` to your RC file (using bash: .bashrc or .bash_profile)"""+Bcolors.ENDC+"""
add new profiles using `$ aws configure --profile newname`

usage:
$ caws User1 # change AWS_DEFAULT_PROFILE to User1
$ caws User1 --withcreds # """+Bcolors.ORANGE+"""not recommended."""+Bcolors.ENDC+""" also edit the contents of ~/.aws/credentials and ~/.aws/config and set the [default] profile.""",
        prog='caws',
        formatter_class=rawtxt
    )
    
    #
    # COMMAND LINE ARGUMENTS
    #parser.print_help()
    #
    parser.add_argument(
        "profile",
        help="""the name of a named profile in ~/.aws/credentials. ex: [user1]:
$ caws user1
where `user1` is the profile""",
        nargs='?',
        default='none'
    )
    parser.add_argument('--withcreds', action='store_true', help='update the default profile in credentials.\n'+Bcolors.FAIL+'Warning!'+Bcolors.ORANGE+' for most applications this is unnecessary.'+Bcolors.ENDC)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)


    args = parser.parse_args()
    profile = args.profile
    withcreds = args.withcreds
    caws_rc = """export AWS_DEFAULT_PROFILE={}"""
    if profile == "none":
        parser.print_help()
        exit()
    else:
        home = expanduser('~')        
        rcfile = os.path.join(home, ".cawsrc")
        if not os.path.isfile(rcfile):
            print(Bcolors.WARNING+"no rc file found, creating..."+Bcolors.ENDC)
            f = open(rcfile, "x")
            f.write(caws_rc.format("default"))
            f.close()
            print(Bcolors.OKGREEN+"created: {}".format(rcfile)+Bcolors.ENDC)
        creds = os.path.join(home, ".aws", "credentials")
        awsconfig = os.path.join(home, ".aws", "config")
        if not os.path.isfile(creds) or not os.path.isfile(awsconfig):
            print(Bcolors.WARNING+"you must have aws cli installed and configured."+Bcolors.ENDC)
            exit()
        f = open(creds)
        line = f.readline()
        exists = False
        while line:
            if profile in line:
                exists = True
            line = f.readline()
        f.close()
        if not exists:
            print(Bcolors.WARNING+"no profile exists with the name {}".format(profile)+Bcolors.ENDC)
            exit()
        if withcreds:
            #
            # !! withcreds is set
            # updating ~/.aws/credentials and ~/.aws/config
            #
            #
            print(Bcolors.ORANGE+"warning: "+Bcolors.WARNING+"editing ~/.aws/credentials and ~/.aws/config"+Bcolors.ENDC)
            print(Bcolors.WARNING+"changing "+Bcolors.ORANGE+"[default]"+Bcolors.WARNING+" to "+Bcolors.MAGENTA+profile+"'s"+Bcolors.WARNING+" ID and KEY"+Bcolors.ENDC)
            rewrite_creds(creds, awsconfig, profile)
        f = open(rcfile, "w")
        f.write(caws_rc.format(profile))
        f.close()

        print(Bcolors.OKGREEN+"changed "+Bcolors.WARNING+"AWS_DEFAULT_PROFILE"+Bcolors.OKGREEN+" to "+Bcolors.PINK+"{}".format(profile)+Bcolors.ENDC)
        print("")
        print("   please run this command: "+Bcolors.WARNING+". "+rcfile+Bcolors.ENDC)
        print("")
    exit()

if __name__ == "__main__":
    main()

#!/usr/bin/env python

"""deploy lambda then terraform"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
import signal
import subprocess
import os
import time
import pkg_resources

def signal_handler(sig, frame):
    """handle control c"""
    print('\nuser cancelled')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

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

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None

def get_script_path(script_name):
    """get the path of the installed build script"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(dir_path, "scripts/%s" % script_name)
    return script_path

def spin_and_heave_intro():
    """show a little message"""
    #bytes.decode(b'\xF0\x9F\x9A\xA7', 'utf8')
    version = pkg_resources.require("spin-and-heave")[0].version
    final = bytes.decode(b'\xF0\x9F\x9A\xA7', 'utf8')+Bcolors.PALEYELLOW+" work in progress. version: {} ".format(version)+Bcolors.ENDC+bytes.decode(b'\xF0\x9F\x9A\xA7', 'utf8')
    sah = ['SPIN', 'AND ', 'HEAVE']
    colors = [Bcolors.CYAN, Bcolors.MAGENTA, Bcolors.WARNING]
    x = 0
    for word in sah:
        print(colors[x]+word+Bcolors.ENDC, end="\r")
        time.sleep(.3)
        x += 1
    print(final)

def main():
    '''deploy lambda then terraform.'''
    spin_and_heave_intro()
    version = pkg_resources.require("spin-and-heave")[0].version
    parser = argparse.ArgumentParser(
        description='run build script to zip lambda package then run terraform apply',
        prog='spin-and-heave',
        formatter_class=rawtxt
    )

    #parser.print_help()
    parser.add_argument(
        "source",
        help="""the directory with your lambda code in it
$ spin-and-heave lambda
where `lambda` is the dir including the python lambda code and requirements
"""+Bcolors.PALEBLUE+"""for more information: """+Bcolors.PALEYELLOW+"""https://gitlab.com/shindagger/spin-and-heave"""+Bcolors.ENDC,
        nargs='?',
        default='none'
    ) 
    parser.add_argument('-r', '--runtime', help="""optional. define a runtime.
"""+Bcolors.PINK+"""defaults:
python: `python3.6`
nodejs: `nodejs10.x` with the """+Bcolors.ORANGE+"""--node [-js]"""+Bcolors.PINK+""" flag"""+Bcolors.ENDC, default="python3.6")
    parser.add_argument('-bc', '--build', help="""optional. define a build command.
"""+Bcolors.PINK+"""defaults:
python: `pip install --progress-bar off -r requirements.txt -t .`
nodejs: `npm install --production` with the """+Bcolors.ORANGE+"""--node [-js]"""+Bcolors.PINK+""" flag"""+Bcolors.ENDC, default="pip install --progress-bar off -r requirements.txt -t .")
    parser.add_argument('-x', '--exclude', action='append', help="""optional. exclude files and directories from the zip file.
uses zip command -x flag conventions.
"""+Bcolors.PINK+"""example: `spin-and-heave lambda -x file.jpg -x docker/\*`"""+Bcolors.ENDC)
    parser.add_argument('-js', '--node', action='store_true', help='deploy node.')
    parser.add_argument('-s', '--skip', action='store_true', help='skip terraform apply.')
    parser.add_argument('-i', '--init', action='store_true', help='init terraform before running apply.')
    parser.add_argument('-a', '--approve', action='store_true', help='run terraform apply with `auto-approve` flag')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    source = args.source
    node = args.node
    skip = args.skip
    init_tf = args.init
    auto_approve = args.approve
    bc = args.build
    excludes = args.exclude
    if node:
        runtime = "nodejs10.x"
        bc = "npm install --production"
    else:
        runtime = args.runtime
        if "nodejs" in runtime:
            node = True
            if bc == "pip install --progress-bar off -r requirements.txt -t .":
                bc = "npm install --production"
    # ERROR CHECKING
    if "nodejs" not in runtime and "python" not in runtime and  bc == "pip install --progress-bar off -r requirements.txt -t .":
        print(Bcolors.WARNING+"currently, spin and heave only has default build commands for python and nodejs.")
        print("if you'd like to build a different runtime, please also include a build command with the "+Bcolors.ORANGE+"--build [-bc]"+Bcolors.WARNING+" flag"+Bcolors.ENDC)
        print()
        parser.print_help()
        exit()
    if source == "none":
        print(Bcolors.WARNING+"please include a source directory"+Bcolors.ENDC)
        print()
        parser.print_help()
        exit()
    if not is_tool("docker"):
        print(Bcolors.ORANGE+"this package uses docker to build dependencies and zip"+Bcolors.ENDC)
        print(Bcolors.WARNING+"please install docker"+Bcolors.ENDC)
        print(Bcolors.MAGENTA+"see the following link for more info: "+Bcolors.ENDC+"https://docs.docker.com/install/")
        print()
        parser.print_help()
        exit()
    if not skip and not is_tool("terraform"):
         print(Bcolors.ORANGE+"spin and heave runs `terraform apply` by default.")
         print(Bcolors.WARNING+"if you would like to skip this behaviour please include the "+Bcolors.ORANGE+"--skip [-s]"+Bcolors.WARNING+" flag")
         print("otherwise, you must have terraform installed."+Bcolors.ENDC)
         print(Bcolors.MAGENTA+"see the following link for more info: "+Bcolors.ENDC+"https://learn.hashicorp.com/terraform/getting-started/install.html")
         print()
         parser.print_help()
         exit()
    if not os.path.isdir(source):
        print(Bcolors.ORANGE+source+Bcolors.WARNING+" is not a directory!"+Bcolors.ENDC)
        print()
        parser.print_help()
        exit()

    source = source.strip("/")
    nexcludes = ""
    if excludes:
        nexcludes += "-x "
        for exc in excludes:
            nexcludes += exc+" "
    excludes = nexcludes[:-1]
    excludes = excludes.replace("/*", "/\\*") # directories workaround
    cwd = os.getcwd()
    swd = os.path.join(cwd, source)
    ###############
    # SWITCH FOR LOCAL DEV TESTING 
    # CHANGE buildit BELOW ACCORDINGLY
    #
    buildit = get_script_path("build.sh") # production
    #buildit = os.path.join(cwd, "scripts", "build.sh") # dev
    print(Bcolors.OKGREEN+"building {} in docker".format(source)+Bcolors.ENDC)
    print(Bcolors.PINK+"this will build dependencies and package the zip file"+Bcolors.ENDC)
    if excludes:
        cmd = buildit+" "+swd+" "+runtime+" "+cwd+" "+source+" \""+bc+"\" \""+excludes+"\""
    else:
        cmd = buildit+" "+swd+" "+runtime+" "+cwd+" "+source+" \""+bc+"\""
    os.system(cmd)
    try:
        # TAKING DOGMATIC LIBERTIES
        zipfile = os.path.join(cwd, source+".zip")
        zipsize = os.path.getsize(zipfile) >> 20
        if zipsize <= 4:
            zipsize = Bcolors.OKGREEN+str(zipsize)+"MB"+Bcolors.ENDC
            zipmsg = Bcolors.OKGREEN+"GOOD"+Bcolors.ENDC+" filesize below 4MB"
        elif zipsize <= 10:
            zipsize = Bcolors.WARNING+str(zipsize)+"MB"+Bcolors.ENDC
            zipmsg = Bcolors.WARNING+"MODERATE"+Bcolors.ENDC+" filesize below 10MB"
        else:
            zipsize = Bcolors.FAIL+str(zipsize)+"MB"+Bcolors.ENDC
            zipmsg = Bcolors.FAIL+"EXCESSIVE"+Bcolors.ENDC+" filesize above 10MB"+Bcolors.GREY+"\nconsidering trimming down your dependencies for faster uploads"+Bcolors.ENDC
        print(Bcolors.OKGREEN+"created "+Bcolors.ORANGE+source+".zip "+zipsize)
        print(zipmsg)
    except Exception as e:
        print(e)
        exit()

    if init_tf:
        print(Bcolors.PALEBLUE+"terraform init"+Bcolors.ENDC)
        subprocess.call("terraform init", shell=True)

    if not skip:
        if auto_approve:
            print(Bcolors.PALEBLUE+"terraform apply -auto-approve"+Bcolors.ENDC)
            subprocess.call("terraform apply -auto-approve", shell=True)
        else:
            print(Bcolors.PALEBLUE+"terraform apply"+Bcolors.ENDC)
            subprocess.call("terraform apply", shell=True)
    exit()

if __name__ == "__main__":
    main()

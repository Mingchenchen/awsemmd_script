#!/usr/bin/env python3
import os
import sys
import random
import time
from random import seed, randint
import argparse
import platform
from datetime import datetime
import imp
from myPersonalFunctions import *
import glob
import numpy
# Useful codes
# os.system("awk '{print $NF}' all_wham.dat > e_total")
# tr " " "\n"
# sed 1d
# sort -u -k 3
# sed -e 's/+T//'
mypath = os.environ["PATH"]
os.environ["PATH"] = "/home/wl45/python/bin:/home/wl45/opt:" + mypath
my_env = os.environ.copy()

parser = argparse.ArgumentParser(description="This is my playground for current project")

# parser.add_argument("protein", help="the name of protein")
# parser.add_argument("template", help="the name of template file")
parser.add_argument("-t", "--test", help="test ", action="store_true", default=False)
parser.add_argument("--plot", action="store_true", default=False)
parser.add_argument("-d", "--debug", action="store_true", default=False)
parser.add_argument("--protein", default="2xov")
parser.add_argument("--dimension", type=int, default=1)
args = parser.parse_args()


if(args.debug):
    do = print
    cd = print
else:
    do = os.system
    cd = os.chdir


if(args.plot):
    do("plotcontour.py pmf-400.dat -xmax 1")


if(args.test):
    force_list = [1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
    for force in force_list:
        do("mkdir {}".format(force))
        cd("{}".format(force))
        do("cp ../freeEnergy.slurm .")
        do("cp ../metadatafile .")
        do(
            "sed -i.bak 's/FORCE/" +
            str(force) +
            "/g' freeEnergy.slurm")
        do("sbatch freeEnergy.slurm")
        cd("..")
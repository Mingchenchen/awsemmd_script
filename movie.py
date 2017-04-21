#!/usr/bin/env python3
import os
import argparse
import sys
from time import sleep
import subprocess
import imp
parser = argparse.ArgumentParser(
        description="written by Wei Lu."
)
parser.add_argument("protein", help="The name of the protein")
parser.add_argument("-p", "--plot", help="only plot mode",
                    action="store_true")
parser.add_argument("-n", "--number", help="number of frames", type=int, default=-1)
parser.add_argument("-d", "--debug", action="store_true", default=False)
args = parser.parse_args()

if(args.debug):
    do = print
    cd = print
else:
    do = os.system
    cd = os.chdir

protein_name = args.protein.split('.')[0]
if(args.number == -1):
    # do("cp ~/opt/pulling/2xov.seq .")
    if(not args.plot):
        os.system("python2 ~/opt/script/BuildAllAtomsFromLammps_seq.py dump.lammpstrj movie "+protein_name+".seq")
        # os.system(
        #     "python2 ~/opt/script/BuildAllAtomsFromLammps.py \
        #     dump.lammpstrj movie")
else:
    os.system("ghead -n 399648 dump.lammpstrj > part_dump")
    if(not args.plot):
        os.system("python2 ~/opt/script/BuildAllAtomsFromLammps_seq.py dump.lammpstrj movie "+protein_name+".seq")
        # os.system(
        #     "python2 ~/opt/script/BuildAllAtomsFromLammps.py \
        #     part_dump movie")
os.system("cp ~/opt/plot_scripts/*.tcl .")

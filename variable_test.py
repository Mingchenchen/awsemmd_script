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
import numpy as np
import fileinput
# from run_parameter import *
parser = argparse.ArgumentParser(
    description="This is a python3 script to\
    do see the difference variable make \
    run simulation")

parser.add_argument("template", help="the name of template file")
parser.add_argument("-d", "--debug", action="store_true", default=False)
parser.add_argument("--rerun",
                    type=int, default=1)
parser.add_argument("-m", "--mode", type=int, default=2)
args = parser.parse_args()
protein_name = args.template.strip('/')

if(args.debug):
    do = print
    cd = print
else:
    do = os.system
    cd = os.chdir

fileName = "2xov_multi.in"
if args.rerun == 0:
    start_from = "read_data data.2xov"
if args.rerun == 1:
    start_from = "read_restart restart.extended"


# simulation_steps = 5e7


def variable_test(force_ramp_rate=[1],
                  memb_k_list=[1],
                  force_list=["ramp"],
                  rg_list=[0.08],
                  repeat=2,
                  start_from_mode=0):
    for force_ramp_rate in force_ramp_rate_list:
        for memb_k in memb_k_list:
            for force in force_list:
                for rg in rg_list:
                    folder_name = "memb_{}_force_{}_rg_{}".format(memb_k, force, rg)
                    # folder_name = "rate_{}".format(force_ramp_rate)
                    # folder_name = "force_{}".format(force)
                    # if memb_k == 0 and rg == 0:
                    #     continue
                    print(folder_name)

                    do("mkdir "+folder_name)
                    do("cp -r 2xov " + folder_name + "/")
                    cd(folder_name + "/2xov")
                    fixFile = "fix_backbone_coeff_go.data"
                    # fixFile = "fix_backbone_coeff_single.data"
                    with fileinput.FileInput(fixFile, inplace=True, backup='.bak') as file:
                        for line in file:
                            print(line.replace("MY_MEMB_K", str(memb_k)), end='')
                    with fileinput.FileInput(fileName, inplace=True, backup='.bak') as file:
                        for line in file:
                            tmp = line
                            tmp = tmp.replace("MY_FORCE", str(force))
                            tmp = tmp.replace("MY_RG", str(rg))
                            tmp = tmp.replace("RATE", str(force_ramp_rate))
                            tmp = tmp.replace("SIMULATION_STEPS", str(int(simulation_steps/force_ramp_rate)))
                            print(tmp, end='')
                    cd("..")
                    do("run.py -m 2 2xov --start extended -n {}".format(repeat))
                    cd("..")
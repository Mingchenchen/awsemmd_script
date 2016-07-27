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
# from run_parameter import *
parser = argparse.ArgumentParser(
        description="This is a python3 script to\
        automatic copy the template file, \
        run simulation and analysis")

parser.add_argument("template", help="the name of template file")
parser.add_argument("-n", "--number", type=int, default=20,
                    help="Number of simulation run")
parser.add_argument("-s", "--steps", type=int, default=8,
                    help="Simulation steps in unit of million,\
                    default is 8 million, -1 means test run")
parser.add_argument("-r", "--read", help="Read from config file",
                    action="store_true")
parser.add_argument("-ws", "--warmSteps", type=int, default=20,
                    help="Warmup Simulation steps in unit of hundred thousand,\
                    default is 2 million")
parser.add_argument("-t", "--test", help="test mode",
                    action="store_true")
args = parser.parse_args()
# TODO:
# add clean command.
# test analysis, and fullfill missing anaylsis.

# protein_name = args.template.split('_', 1)[-1].strip('/')
n = args.number
protein_name = args.template.strip('/')
if args.steps == -1:  # smallest run for debug.
    simulation_steps = 10**4
    warm_up_steps = 10**3
    n = 1  # also set
elif args.test:  # test run
    simulation_steps = 50 * 10**3
    warm_up_steps = 50 * 10**3
else:
    simulation_steps = args.steps * 10**6
    warm_up_steps = args.warmSteps * 10**5

warm_up_steps = 10**5
simulation_steps = 10**6

config = open('config.py', 'w')
config.write("number_of_run = %d\nsimulation_steps = %d\n\
warm_up_steps = %d\n" % (n, simulation_steps, warm_up_steps))
config.close()
for temp in range(200, 250, 50):
    # print(temp)
    seed(datetime.now())
# simulation set up
    os.system("mkdir -p simulation/"+str(temp))

    os.chdir("simulation/"+str(temp))

    for q0_percent in range(10, 95, 5):
        q0 = q0_percent/100.0
        os.system("mkdir -p "+str(q0))
        os.system("cp -r ../../"+args.template+"* "+str(q0))
        os.chdir(str(q0))
        os.system(  # replace TEMPERATURE with specific steps
            "sed -i.bak 's/Q0/'" +
            str(q0) +
            "'/g' fix_qbias_coeff.data")
        os.system(  # replace TEMPERATURE with specific steps
            "sed -i.bak 's/TEMPERATURE/'" +
            str(temp) +
            "'/g' "+protein_name+".in")
        os.system(  # replace SIMULATION_STEPS with specific steps
            "sed -i.bak 's/WARM_UP_STEPS/'" +
            str(warm_up_steps) +
            "'/g' "+protein_name+".in")
        os.system(  # replace RANDOM with a radnom number
                "sed -i.bak 's/RANDOM/'" +
                str(randint(1, 10**6)) +
                "'/g' "+protein_name+".in")
        os.system(  # replace SIMULATION_STEPS with specific steps
                "sed -i.bak 's/SIMULATION_STEPS/'" +
                str(simulation_steps) +
                "'/g' "+protein_name+".in")
        if(platform.system() == 'Darwin'):
            os.system("/Users/weilu/Documents/lammps-9Oct12_modified/src/lmp_serial \
            < "+protein_name+".in")
        elif(platform.system() == 'Linux'):
            os.system("cp ~/opt/run.slurm .")
            os.system(  # replace PROTEIN with pdb name
                    "sed -i.bak 's/PROTEIN/'" +
                    protein_name +
                    "'/g' run.slurm")
            os.system("sbatch run.slurm")
        else:
            print("system unkown")
        os.chdir("..")
    os.chdir("../..")

sys.exit(0)


# print("hello world")
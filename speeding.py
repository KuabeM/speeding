#!/usr/bin/env python3

# define docopt string
"""Speeding: Small utility to perform speedtests periodically.

Usage:
    speeding.py [--iter=<iter>] [--delay=<delay>]
    speeding.py (-h | --help)
    speeding.py (-v | --version)

Options:
    -h --help   Show this screen
    -v --version    Show version
    --iter=<iter>   Set number of iterations    [default: 10]
    --delay=<delay> Set time delay between speedtests   [default: 30]

"""
from docopt import docopt
import datetime
import time
import subprocess
import sys

arguments = docopt(__doc__, version='Speeding 0.1.1')

# handle command line args
if not arguments.get('--iter') == False:
    iterations = int(arguments.get('--iter'))
    print("Running for " + str(iterations) + " iterations")
else:
    iterations = 10
    print("Running for " + str(iterations) + " iterations")

if not arguments.get('--delay') == False:
    delay = int(arguments.get('--delay'))   
    print("with a delay of " + str(delay) + "s")
else:
    delay = 30
    print("with a delay of " + str(delay) + "s")


# get current time
now = datetime.datetime.now()

# open file handle
file  = open("log_" + str(now.day) + "." + str(now.month) + "." + str(now.year) + ".md" , "a+")
# write daily header
file.write("\n## log of " + str(now.day) + "." + str(now.month) + "." + str(now.year) + "\n")
file.write("|   Time   |   Download    |    Upload    |\n")
file.write("|----------|---------------|--------------|\n")
file.close()

i = 0
while i < iterations:
    # write time column
    now = datetime.datetime.now()
    file  = open("log_" + str(now.day) + "." + str(now.month) + "." + str(now.year) + ".md" , "a+")
    file.write("| " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + ":" + str(now.second).zfill(2) + " | ")
    # run speedtest
    speed_cmd = subprocess.run( ["speedtest"], stdout= subprocess.PIPE)
    speed_out = speed_cmd.stdout.decode("utf-8")
    # get relevant part of ouput
    speed_out = speed_out.split("\n")
    download = speed_out[6]
    upload = speed_out[8]
    # print to stdout
    print("Iteration " + str(i+1).zfill(2) + ": " + download + ", " + upload)
    # write to file
    file.write( download[10:] + " | " + upload[8:] + " |\n")
    # wait some time
    time.sleep(int(delay))
    file.close()

    i = i+1

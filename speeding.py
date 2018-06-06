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

arguments = docopt(__doc__, version='Speeding 0.1.0')

# handle command line args
if not arguments.get('--iter') == False:
    iterations = int(arguments.get('--iter'))
    print("iterations: " + str(iterations))
else:
    iterations = 10
    print("iterations: " + str(iterations))

if not arguments.get('--delay') == False:
    delay = int(arguments.get('--delay'))   
    print("delay: " + str(delay))
else:
    delay = 30
    print("delay: " + str(delay))


# get current time
now = datetime.datetime.now()

# open file handle
file  = open("log_" + str(now.day) + "." + str(now.month) + "." + str(now.year) + ".md" , "a+")
# write daily header
file.write("## log of " + str(now.day) + "." + str(now.month) + "." + str(now.year) + "\n")
file.write("|   Time   |   Download    |    Upload    |\n")
file.write("|----------|---------------|--------------|\n")

i = 0
while i < iterations:
    # write time column
    now = datetime.datetime.now()
    file.write("| " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + ":" + str(now.second) + " | ")
    # run speedtest
    speed_cmd = subprocess.run( ["speedtest"], stdout= subprocess.PIPE)
    speed_out = speed_cmd.stdout.decode("utf-8")
    # get relevant part of ouput
    speed_out = speed_out.split("\n")
    download = speed_out[6]
    upload = speed_out[8]
    # print to stdout
    print("Iteration " + str(i+1) + ": " + download + ", " + upload)
    # write to file
    file.write( download[10:] + " | " + upload[8:] + " |\n")
    # wait some time
    time.sleep(int(delay))

    i = i+1

# close file
file.write("\n")
file.close()

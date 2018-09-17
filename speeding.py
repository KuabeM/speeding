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
import json


def magnitude(val):
    if val > 1000*1000:
        val = val/(1000*1000)
        return (val,'M')
    elif val > 1000:
        val = val/1000
        return (val,'k')
    else:
        return (val,'  ')
    return;

def main():
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
    file.write("\n## logging " + str(now.hour) + ":" + str(now.minute) + ", " + str(now.day) + "." + str(now.month) + "." + str(now.year) + "\n")
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
        speed_cmd = subprocess.run( ["speedtest", "--json"], stdout= subprocess.PIPE)
        speed_out = speed_cmd.stdout.decode("utf-8")
        # parse the json
        out_json = json.loads(speed_out)
        download = out_json["download"]
        upload = out_json["upload"]
        # get magnitude
        (download, mag_down) = magnitude(download)
        (upload, mag_up) = magnitude(upload)
        
        # get relevant part of ouput
        # speed_out = speed_out.split("\n")
        # download = speed_out[6]
        # upload = speed_out[8]
        down_str = "{0:6.2f} ".format(download)
        up_str = "{0:5.2f} ".format(upload)
        # print to stdout
        print("Iteration "  + str(i+1).zfill(2) + ": " + down_str + str(mag_down) + "bit/s, " + up_str + str(mag_up) + "bit/s")
        
        # write to file
        file.write( down_str + str(mag_down) + "bit/s" + " | " + up_str + str(mag_up) + "bit/s"  + " |\n")
        # wait some time
        time.sleep(int(delay))
        file.close()

        i = i+1

# call main function
main()  
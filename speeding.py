
import datetime
import time
import subprocess
import sys

# handle command line args
if len(sys.argv) > 1:
    iterations = int(sys.argv[1])
    print("iterations: " + str(iterations))
else:
    iterations = 10

if len(sys.argv) == 3:
    delay = int(sys.argv[2])
    print("delay: " + str(delay))
else:
    delay = 30


# open file handle
file  = open("log.md", "a+")

# get current time
now = datetime.datetime.now()
# write daily header
file.write("## log of " + str(now.day) + "." + str(now.month) + "." + str(now.year) + "\n")
file.write("|   Time   |   Download    |    Upload    |\n")
file.write("|----------|---------------|--------------|\n")

i = 0
while i < iterations:
    # write time column
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

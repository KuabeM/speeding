
import datetime
import time
import subprocess
import sys

def main():
    file  = open("log.md", "a+")
    
    # get current time
    now = datetime.datetime.now()
    # write daily header
    file.write("# log of " + str(now.day) + "." + str(now.month) + "." + str(now.year) + "\n")

    i = 0
    while i < 60:
        # write test header
        file.write("## time: " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second))
        # run speedtest
        speed_cmd = subprocess.run( ["speedtest"], stdout= subprocess.PIPE)
        speed_out = speed_cmd.stdout.decode("utf-8")
        speed_out = speed_out.split("................................................................................")
        download = speed_out[1]
        upload = speed_out[2]
        
        file.write(download[:24] + ", " + upload[23:])
        time.sleep(30)

        i = i+1

    file.close()

if __name__== "__main__":
    main()
# This is the main script that will run indefinitely on a Raspberry Pi Model 4B with the all of the additionally required hardware.
# Every timeframe, it will call the security_camera.py script which posts the current occupancy and noise level of the room to a server
# for analysis.

from time import sleep
import subprocess

timeframe = 300 # 300 seconds = 5 minutes
def call_script():
    subprocess.run(["python3", "security_camera.py"])
    return

def main():
    while True:
        call_script()
        sleep(timeframe)
        
if __name__ == "__main__":
    main()
        


import time
import RPi.GPIO as GPIO

# Constants
nbPCAServo=16 

#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[360, 360, 360, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]

def init_servo():
    #Objects
    from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/
    pca = ServoKit(channels=16)
    return pca
pca = init_servo()

pca.servo[0].set_pulse_width_range(MIN_IMP[0] , MAX_IMP[0])
pca.servo[1].set_pulse_width_range(MIN_IMP[0] , MAX_IMP[0])


MID = 77
MID1 = 93
MAX_TILT = 30
pca.servo[0].angle = MID
pca.servo[1].angle = MID1
# pca.servo[2].angle = MID

lag = 0.005


def tilt_left(MID, servoId):
    for j in range(MID, MID - MAX_TILT,-1):
        pca.servo[servoId].angle = j
        time.sleep(lag)
    time.sleep(1)
    for j in range(MID-MAX_TILT, MID, 1):
        pca.servo[servoId].angle = j
        time.sleep(lag)


def tilt_right(MID, servoId):
    for j in range(MID,MID + MAX_TILT,1):
        pca.servo[servoId].angle = j
        time.sleep(lag)
    time.sleep(1)

    for j in range(MID + MAX_TILT, MID,-1):
        pca.servo[servoId].angle = j
        time.sleep(lag)

def tilt_plastic():
    tilt_left(MID, 0)

def tilt_can():
    tilt_right(MID1, 1)

def tilt_paper():
    tilt_right(MID, 0)
    
def tilt_general():
    tilt_left(MID1, 1)
    
if __name__ == "__main__":
    while True:
        inp = int(input("0 paper 1 plastic 2 metal 3 general\n"))
        if inp == 0:
            tilt_paper()
        elif inp == 1:
            tilt_plastic()
        elif inp == 2:
            tilt_can()
        elif inp == 3:
            tilt_general()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Libraries
import time    #https://docs.python.org/fr/3/library/time.html
from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/

#Constants
nbPCAServo=16 

#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[360, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]

#Objects
pca = ServoKit(channels=16)

# function init 
def init():

    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])


# function main 
def main():

    pcaScenario()


# function pcaScenario 
def pcaScenario():
    """Scenario to test servo"""
    # ratio = (170/180)
    MID = 75
    MAX_TILT = 15

    pca.servo[0].angle = MID
    # while(True):
    #     m = int(input("Enter 0 or 1:"))
    #     pca.servo[0].angle = m
        
    
    # # # pca.servo[0].angle = 0
    while (True):

        m = int(input("Enter 0 or 1:"))
        # pca.servo[0].angle = m
        if (m == 0) :
            for j in range(MID, MID - MAX_TILT,-1):
                pca.servo[0].angle = j
                time.sleep(0.05)
            time.sleep(1)
            for j in range(MID-MAX_TILT, MID, 1):
                pca.servo[0].angle = j
                time.sleep(0.05)
        else:
            for j in range(MID,MID + MAX_TILT,1):
                pca.servo[0].angle = j
                time.sleep(0.05)
            time.sleep(1)

            for j in range(MID + MAX_TILT, MID,-1):
                pca.servo[0].angle = j
                time.sleep(0.05)


if __name__ == '__main__':
    init()
    main()
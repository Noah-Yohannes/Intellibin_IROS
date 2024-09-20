import time
import RPi.GPIO as GPIO
 
#sensor GPIO pins
# def setPins():
#     GPIO.setmode(GPIO.BCM)
#     GPIO_TRIGGER = 15
#     GPIO_ECHO = 24
#     GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
#     GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO_TRIGGER = 17
GPIO_ECHO = 23
def setPins():
    #set pins
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # # Set trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # # Set trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

def distance():
    
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # # Set trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # # Set trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)



    start_time = time.time()
    stop_time = time.time()
    # Save start time
    while GPIO.input(GPIO_ECHO) == 0:
        # print("yo")
        start_time = time.time()

    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Time difference between start and arrival
    time_elapsed = stop_time - start_time

    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (time_elapsed * 34300) / 2

    return distance
# distance()

if  __name__ == "__main__":
    start = time.time()
    # setPins()
    while True:
        end = time.time()
        if (end - start > 1.0):
            print(f"{distance()}")
            start = end
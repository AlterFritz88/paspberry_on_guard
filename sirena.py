from datetime import timedelta, datetime
import RPi.GPIO as GPIO
time_set = datetime.now()
gpio = 0
def initial():
    global gpio
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT, initial = 0)
    gpio = 0
    
def start_sirena():
    global time_set
    global gpio 
    GPIO.output(40, 1)
    time_set = datetime.now()
    gpio = 1
    print(gpio)
    
def is_sirena_stop():
    global gpio
    global time_set
    if time_set + timedelta(minutes=1) <= datetime.now():  # work for 1 min
        gpio = 0
        GPIO.output(40, 0)
        print(gpio)
    else:
        print(gpio)

def close_sirena():
    GPIO.cleanup()
    

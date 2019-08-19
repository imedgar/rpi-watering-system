# External module imp
import RPi.GPIO as GPIO
import datetime
import time

init = False
fileName = "last_watered.txt"
GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)

def clean_gpio():
    GPIO.cleanup() # cleanup all GPI
    GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

def get_last_watered():
    """ Shows when was the last time the plant was watered."""
    try:
        f = open(fileName, "r")
        return f.readline()
    except:
        return "file_does_not_exist"

def set_last_watered():
    f = open(fileName, "w")
    f.write("Last watered {}".format(datetime.datetime.now()))
    f.close()        
      
def get_status(pin = 8):
    """ Gets the pin 8 signal. Soil moisture sensor"""
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)
        
def low_high_delay(pin, delay):
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(pump_pin, GPIO.HIGH)

def auto_water(delay = 5, pump_pin = 7, water_sensor_pin = 8):
    consecutive_water_count = 0
    init_output(pump_pin)
    print("Auto water is on...! Press CTRL+C to exit")
    try:
        while 1 and consecutive_water_count < 10:
            time.sleep(delay)
            wet = get_status(pin = water_sensor_pin) == 0
            if not wet:
                if consecutive_water_count < 5:
                    pump_on(pump_pin, 1)
                consecutive_water_count += 1
            else:
                consecutive_water_count = 0
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

def pump_on(pump_pin = 7, delay = 1):
    init_output(pump_pin)
    set_last_watered()
    low_high_delay(pump_pin, delay)

def pump_on_if_needed(pump_pin = 7, delay = 1):
    if get_status() == 0:
        init_output(pump_pin)
        set_last_watered()
        low_high_delay(pump_pin, delay)    
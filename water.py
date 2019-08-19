# External module imp
import RPi.GPIO as GPIO
import datetime
import time

init = False
GPIO.setmode(GPIO.BOARD)  # Broadcom pin-numbering scheme
fileName = "last_watered.txt"


def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)


def clean_gpio():
    GPIO.cleanup()  # cleanup all GPI
    GPIO.setmode(GPIO.BOARD)  # Broadcom pin-numbering scheme


def get_last_watered():
    """ Shows when was the last time the plant was watered."""
    try:
        f = open(fileName, "r")
        return f.readline()
    except IOError:
        return "file_does_not_exist"


def set_last_watered():
    f = open(fileName, "w")
    f.write("Last watered {}".format(datetime.datetime.now()))
    f.close()


def get_status(pin=8):
    """ Gets the pin 8 signal. Soil moisture sensor"""
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)


def low_high_delay(pin, delay):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(pin, GPIO.HIGH)


def pump_on(pump_pin=7, delay=1):
    init_output(pump_pin)
    set_last_watered()
    low_high_delay(pump_pin, delay)


def pump_on_if_needed(pump_pin=7, delay=1):
    if get_status() == 0:
        pump_on(pump_pin, delay)

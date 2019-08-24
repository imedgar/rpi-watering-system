# External module imp
import RPi.GPIO as GPIO
from datetime import datetime
import time

init = False
GPIO.setmode(GPIO.BOARD)  # Broadcom pin-numbering scheme
last_watered_file = "last_watered.txt"
auto_watering_file = "auto_watering.txt"
datetime_format = "%b %d %Y %H:%M:%S"
water_flow = 3


def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)


def clean_gpio():
    GPIO.cleanup()  # cleanup all GPI
    GPIO.setmode(GPIO.BOARD)  # Broadcom pin-numbering scheme


def get_last_watered(file):
    """ Shows when was the last time the plant was watered."""
    try:
        f = open(last_watered_file if file == 0 else auto_watering_file , "r")
        return f.readline()
    except IOError:
        return "file_does_not_exist"


def set_last_watered():
    f = open(last_watered_file, "w")
    f.write("Plant was watered @ {}".format(datetime.now().strftime(datetime_format)))
    f.close()


def get_status(pin=8):
    """ Gets the pin 8 signal. Soil moisture sensor"""
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)


def low_high_delay(pin, delay):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(pin, GPIO.HIGH)


def pump_on(pump_pin=7, delay=water_flow):
    init_output(pump_pin)
    set_last_watered()
    low_high_delay(pump_pin, delay)


def pump_on_if_needed(pump_pin=7, delay=water_flow):
    f = open(auto_watering_file, "w")
    if get_status() == 0:
        pump_on(pump_pin, delay)
        f.write("HUE checked and watered the plant @ {}".format(datetime.now().strftime(datetime_format)))
    else:
        f.write("HUE checked and NOT watered the plant @ {}".format(datetime.now().strftime(datetime_format)))
    f.close()
    GPIO.cleanup()  # cleanup all GPI

def time_diff(last_watered):
    last_watered_dt = datetime.strptime(last_watered.strip()[24:], "%b %d %Y %H:%M:%S")
    diff = last_watered_dt - datetime.now()
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return last_watered + ' ( It''s been {}h {}min )'.format(abs(hours), minutes)
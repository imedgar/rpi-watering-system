# External module imp
import RPi.GPIO as GPIO
from datetime import datetime
import time
from dict_en import dict_en


init = False
GPIO.setmode(GPIO.BOARD)  # Broadcom pin-numbering scheme
last_watered_file = "last_watered.txt"
auto_watering_file = "auto_watering.txt"
IOError_msg = "file_does_not_exist"
datetime_format = "%b %d %Y %H:%M:%S"
water_flow = 3


def clean_gpio():
    """ Resets the GPIO board."""
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)


def read_file(file):
    """ Read files, 0 for last_watered and 1 for auto_watering"""
    try:
        return open(last_watered_file if file == 0 else auto_watering_file, "r").readline()
    except IOError:
        return IOError_msg


def write_file(file, content):
    """ Write on files, 0 for last_watered and 1 for auto_watering"""
    f = open(last_watered_file if file == 0 else auto_watering_file, "w")
    f.write(content)
    f.close()


def get_status(pin=8):
    """ Gets the pin 8 signal. Soil moisture sensor"""
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)


def pump_on(pump_pin=7, delay=water_flow):
    """ Pumps water for delay seconds. """
    # avoid accidentally clicking or several request
    if time_diff()['minutes'] > 0 or time_diff()['seconds'] >= 10:
        # init the output
        GPIO.setup(pump_pin, GPIO.OUT)
        GPIO.output(pump_pin, GPIO.LOW)
        GPIO.output(pump_pin, GPIO.HIGH)
        write_file(0, datetime_now_str())
        # pump on with for x sec
        GPIO.output(pump_pin, GPIO.LOW)
        time.sleep(delay)
        GPIO.output(pump_pin, GPIO.HIGH)
        return 0
    else:
        return 1


def pump_on_if_needed():
    """ Pumps water for delay seconds only if needed. """
    if get_status() == 0:
        pump_on()
        write_file(1, dict_en['HUE_checked'].format(datetime_now_str()))
    else:
        write_file(1, dict_en['HUE_checked_and_not'].format(datetime_now_str()))
    GPIO.cleanup()


def time_diff():
    """" Time difference between NOW and last time watered """
    diff = datetime.now() - datetime.strptime(read_file(0).strip(), datetime_format)
    hours = diff.days * 24 + diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    seconds = diff.seconds % 60
    return {
        'hours': abs(hours),
        'minutes': minutes,
        'seconds': seconds
    }


def datetime_now_str():
    return datetime.now().strftime(datetime_format)

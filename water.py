# External module imp
import RPi.GPIO as GPIO
from datetime import datetime
import time
from configparser import ConfigParser
from dict_en import dict_en


init = False
GPIO.setmode(GPIO.BOARD)  # Broadcom pin-numbering scheme
last_watered_file = "last_watered.txt"
auto_watering_file = "auto_watering.txt"
IOError_msg = "file_does_not_exist"
datetime_format = "%b %d %Y %H:%M:%S"


def clean_gpio():
    """ Resets the GPIO board."""
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)


def time_diff(last_watered):
    """" Time difference between NOW and last time watered """
    diff = datetime.now() - datetime.strptime(last_watered.strip(), datetime_format)
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
